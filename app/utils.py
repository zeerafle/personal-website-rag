from langchain_core.messages import AIMessage


def extract_agent_response(result: dict) -> str:
    """
    Extract the agent's response from LangChain agent result.

    Args:
        result: The result dict from agent.ainvoke()

    Returns:
        The agent's text response
    """
    last_message = result["messages"][-1]

    # check that the last response is AIMessage
    if not isinstance(last_message, AIMessage):
        return ""

    # Handle different content formats
    if isinstance(last_message.content, str):
        return last_message.content
    elif isinstance(last_message.content, list):
        # Extract text from content blocks
        return "".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in last_message.content
        )
    else:
        return str(last_message.content)
