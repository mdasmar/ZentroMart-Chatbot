from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import AIMessage
from src.agent import agent

thread_id="5"

embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

vecstore = Chroma(
    collection_name="zentromart_kb",
    persist_directory="chroma_db",
    embedding_function=embedding
)

def retrieve_context(question):
    documents = vecstore.max_marginal_relevance_search(
        question,
        k=5,
        fetch_k=15,
        lambda_mult=0.7,
    )

    if not documents:
        return "No relevant knowledge was found."

    context_parts = []

    for index,document in enumerate(documents, start=1):
        metadata = document.metadata
        section_id = metadata.get("section_id")

        context_parts.append(
            f"""
            SOURCE {index}
            Section ID: {section_id}
            Source file: {metadata.get("source_file")}

            CONTENT:
            {document.page_content}
            """
        )

    return "\n".join(context_parts)

def get_final_answer(result):
    for message in reversed(result["messages"]):
        if isinstance(message, AIMessage):
            if not message.tool_calls:
                return message.content
    return "I could not generate a response."

def respond(question):
    context=retrieve_context(question)

    user_message = f"""
        Customer question:
        {question}

        Relevant knowledge-base context:
        {context}

        Answer the customer using the context above.
        Use tools when required.
        """

    config = {"configurable":{"thread_id": thread_id}}

    result=agent.invoke({
            "messages":[
                {
                    "role": "user",
                    "content": user_message,
                }
            ]
        },
        config=config,
    )
    return {"answer": get_final_answer(result)}