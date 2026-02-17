"""
Use the Foundational Model API exposed on local device to query with Python Langchain and recieved a streamed output.
"""

from langchain_core.messages.human import HumanMessage

from model.client import LocalLLM

llm = LocalLLM()
model = llm.get_model()

while True:
    user_input = input("\nPrompt: ")
    if user_input.lower() in ["quit", "exit"]:
        break
    print("Generating...")

    messages = [HumanMessage(content=user_input)]

    for chunk in model.stream(messages):
        print(chunk.content, end="", flush=True)
    print()
