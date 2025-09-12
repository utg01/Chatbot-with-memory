from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage,AIMessage
from dotenv import load_dotenv
load_dotenv()
model=ChatGoogleGenerativeAI(model='gemini-2.0-flash')

# Chat template 

chat_template=ChatPromptTemplate([
    ('system','You are a helpful ai assistant'),
    MessagesPlaceholder(variable_name='chat_history_all'),
    ('human','{query}')
])

chat_history_all=[]
try:
    with open("chat_history.txt",'r') as f:
        for line in f:
            if line.startswith("HUMAN:"):
                chat_history_all.append(HumanMessage(content=line.replace("HUMAN:","").strip()))
            elif line.startswith("AI:"):
                chat_history_all.append(AIMessage(content=line.replace("AI:","").strip()))
except FileNotFoundError:
    pass
while True:
    
    with open("chat_history.txt","a+") as file:

    
        user_input=input("you:")
        chat_history_all.append(HumanMessage(content=user_input.strip()))
        
        
        if user_input.lower()=="exit":
                        break
        
        prompt=chat_template.invoke({
            'chat_history_all' : chat_history_all ,
            'query':user_input
        })

        result=model.invoke(prompt)
        one_line = result.content.replace("\n", " ").strip()
        chat_history_all.append(AIMessage(content=one_line.strip()))
        file.write("HUMAN:"+ user_input + "\n")
        file.write("AI:"+ one_line + "\n")
        print("AI:",result.content)

