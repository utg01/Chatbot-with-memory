import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

# Load environment
load_dotenv()
model = ChatGoogleGenerativeAI(model='gemini-2.0-flash')

# Chat template 
chat_template = ChatPromptTemplate([
    ('system','You are a helpful ai assistant'),
    MessagesPlaceholder(variable_name='chat_history_all'),
    ('human','{query}')
])

# Initialize chat history in session state
if "chat_history_all" not in st.session_state:
    st.session_state.chat_history_all = []

st.title("💬 AI Chatbot")

# Restore history from file only once (like your try block)
if "loaded_history" not in st.session_state:
    try:
        with open("chat_history.txt",'r') as f:
            for line in f:
                if line.startswith("HUMAN:"):
                    st.session_state.chat_history_all.append(HumanMessage(content=line.replace("HUMAN:","").strip()))
                elif line.startswith("AI:"):
                    st.session_state.chat_history_all.append(AIMessage(content=line.replace("AI:","").strip()))
    except FileNotFoundError:
        pass
    st.session_state.loaded_history = True

# User input box
user_input = st.text_input("You:", "")

# Send button
if st.button("Send") and user_input.strip() != "":
    with open("chat_history.txt","a+") as file:
        # Add Human message
        st.session_state.chat_history_all.append(HumanMessage(content=user_input.strip()))
        file.write("HUMAN:" + user_input + "\n")

        # Exit condition
        if user_input.lower() != "exit":
            prompt = chat_template.invoke({
                'chat_history_all' : st.session_state.chat_history_all ,
                'query':user_input
            })

            result = model.invoke(prompt)
            one_line = result.content.replace("\n", " ").strip()

            # Add AI message
            st.session_state.chat_history_all.append(AIMessage(content=one_line.strip()))
            file.write("AI:" + one_line + "\n")

            # Show latest AI output
            st.markdown(f"**AI:** {result.content}")

# Display full conversation
st.subheader("Conversation History")
for msg in st.session_state.chat_history_all:
    if isinstance(msg, HumanMessage):
        st.markdown(f"**You:** {msg.content}")
    elif isinstance(msg, AIMessage):
        st.markdown(f"**AI:** {msg.content}")
