"""
Use the Foundational Model API exposed on local device to query with Python Langchain and recieve a standard output.
"""

from model.client import LocalLLM

llm = LocalLLM()
model = llm.get_model()

while True:
    user_input = input("\nPrompt: ")
    print("Generating...")

    if user_input.lower() in ["quit", "q", "exit"]:
        break

    response = model.invoke(f"{user_input}")
    print("Answer: ", response.content)
