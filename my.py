# LangGraph coding project
# my_agent.py
import asyncio

from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
load_dotenv()


def create_canvas_graph(tools):
    # 1. LLM that can reason about tools
    llm = ChatOpenAI(model="gpt-4.1-mini").bind_tools(tools)

    # Node: run the LLM on the current messages
    def agent_node(state: MessagesState):
        # state["messages"] is the full chat history
        response = llm.invoke(state["messages"])
        # With MessagesState, we return ONLY new messages
        return {"messages": [response]}

    # Node: actually call tools the LLM requested
    tool_node = ToolNode(tools)

    # 2. Build the graph
    graph = StateGraph(MessagesState)
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)

    # 3. Wiring / edges
    graph.add_edge(START, "agent")

    # Use LangGraph's built-in tool routing:
    # if the last LLM message has tool_calls → go to "tools", else END.
    graph.add_conditional_edges("agent", tools_condition)
    graph.add_edge("tools", "agent")  # after tools, go back to agent

    return graph.compile()


async def main():
    # 1. Connect to your MCP server
    client = MultiServerMCPClient(
        {
            "canvas": {
                "transport": "stdio",
                "command": "python3",
                "args": ["canvas_mcp.py"],
            }
        }
    )

    # 2. Load tools
    tools = await client.get_tools()

    # 3. Build graph
    graph = create_canvas_graph(tools)

    print("✅ Canvas LangGraph agent ready. Type 'exit' to leave conversation.\n")

    # ---- THIS IS THE FIX ----
    history = []  # full chat history across turns

    while True:
        user_input = input("You: ")

        if user_input.strip().lower() in {"quit", "exit"}:
            break

        # add newest user message to conversation
        history.append(HumanMessage(content=user_input))

        # run the graph on the ENTIRE history
        result = await graph.ainvoke({"messages": history})

        # MessagesState returns ALL messages this turn (assistant + tool msgs)
        history = result["messages"]

        # print the final assistant message
        final_msg = history[-1]
        print(f"\nTutor: {final_msg.content}\n")

    # no close() needed on the new client




if __name__ == "__main__":
    asyncio.run(main())

