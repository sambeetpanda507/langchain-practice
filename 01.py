from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Define the prompt template
prompt = ChatPromptTemplate(
    [
        (
            "system",
            "You are helpful assistant. "
            "Give answer to the user's query in a friendly tone. \n\n"
            "NOTE: Give answer only in {length} words",
        ),
        ("human", "Explain the topic: {topic}"),
    ]
)


# Define the model
model = init_chat_model(model="gpt-oss:latest", model_provider="ollama", temperature=0)

# Prompt -> model -> string output
chain = prompt | model | StrOutputParser()

while True:
    print("Enter your query\n\n")
    query = input("User: ")
    if query in ["end", "exit", "quit"]:
        break

    print(f"AI: You want to know about '{query}'")
    try:
        length = int(input("How many words you want to answer to be: "))
    except:
        length = 100

    stream = chain.stream({"topic": query, "length": length})
    print("AI: ", end=" ")
    for chunk in stream:
        if chunk:
            print(chunk, end="", flush=True)
