from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from medical_assistant.prompts.chabot import template
from medical_assistant.config import model


chain = template | model

store = {}

def get_sess_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()

    return store[session_id]


chatbot = RunnableWithMessageHistory(
    chain,
    get_sess_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)

def run_chatbot(analysis, comparison, msg):
    return chain.invoke({
        "analysis": analysis,
        "comparison": comparison,
        "chat_history": [],
        "human_msg": msg
    })


# session_id = "user_123"

# while True:
#     user_input = input("YOU: ")
#     if user_input.lower() in ["break", "exit"]:
#         print("chat ended")
#         break

#     res = chain.invoke({
#         "analysis": "Metadata:{Rahul Sharma | Age: 32 | UHID: LAB-2026-89412}, Summary : Worsening microcytic hypochromic anemia along with escalating bacterial infection and reactive thrombocytosis over a 2-month period.",
#         "comparison": "the user health is v badd and his anemia is getting worse",
#         "chat_history": [],
#         "human_msg": user_input
#     })

#     print("bot: ", res.content)