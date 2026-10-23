from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from tools.tools import lookup_order, create_ticket
from src.llm import llm
from src.prompt import SYSTEM_PROMPT


tools=[lookup_order,create_ticket]
memory=InMemorySaver()

agent=create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=memory
)