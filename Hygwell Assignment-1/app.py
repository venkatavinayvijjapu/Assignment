import streamlit as st
from dotenv import load_dotenv
import os
import requests

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from pydantic_models import QueryRequest
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent
from langchain.agents import AgentExecutor



load_dotenv()



# Setup API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Google Search Tool

# uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])
# url = st.sidebar.text_input("Enter URL")

with st.sidebar:
    file_uploader=st.file_uploader("Upload your file:", type=["pdf"])
    url=st.text_input("Enter URL")
    if file_uploader is not None and "pdf" not in st.session_state:
    # Send the uploaded file to the new API endpoint
        response = requests.post(
            "http://127.0.0.1:8000/process_pdf/",
            files={"file": file_uploader},
        )
        
        # Handle the API response
        if response.status_code == 200:
            # Extract chat_id from the response if needed
            chat_id = response.json().get("chat_id")
            st.success(f"PDF processed successfully with Chat ID: {chat_id}")
            st.session_state.pdf = chat_id
        else:
            # Display error message from the response
            error_message = response.json().get("error", "An error occurred while processing the PDF.")
            st.error(error_message)

    elif url and "url" not in st.session_state:
        # url='https://blog.futuresmart.ai/guide-to-langsmith'
        # file_path = './handbook.pdf'

        # with open(file_path, 'rb') as file:
        if not url.startswith(('http://', 'https://')):
            st.error("Invalid URL format. Please ensure the URL starts with 'http://' or 'https://'.")
        else:
            # Send the URL to the new API endpoint
            response = requests.post(
                "http://127.0.0.1:8000/process_url/",
                json={"url": url}
            )

            # Handle the API response
            if response.status_code == 200:
                # Extract chat_id from the response if needed
                url_chat_id = response.json().get("chat_id")
                st.success(f"Blog extracted successfully with Chat ID: {url_chat_id}")
                st.session_state.url = url_chat_id
            else:
                # Display error message from the response
                error_message = response.json().get("error", "An error occurred while processing the URL.")
                st.error(error_message)

if "messages" not in st.session_state:
   st.session_state.messages = []


if (file_uploader is None)and (url is None or url==""):
    st.info("please upload your pdf and url")
elif (url is None or url=="") and (file_uploader is not None):
    st.info("please upload your url")
elif (url is not None or url!="") and (file_uploader is None):
    st.info("please upload your pdf")
else:
    option = st.selectbox(
    "what do you wanna connect with?",
    ("PDF","URL"),
    index=None,
    placeholder="Select Your Application.."
)
    if option=="PDF":
        code=st.session_state.pdf
    else:
        code=st.session_state.url

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown (message["content"])

    if "prompt" not in st.session_state:
        # chat = ChatGroq(temperature=0, groq_api_key="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", model_name="mixtral-8x7b-32768")
        chat = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0, api_key=OPENAI_API_KEY)
        system = "You are a helpful assistant, you are provided the content{content} from my vector database based on query, you need to structure the response as per the query{input}"
        human = "{input},{content}"
        prompt = ChatPromptTemplate.from_messages(
            [("system", system), 
            ("human", human)]
            )
        st.session_state.chain = prompt | chat
        st.session_state.prompt="Existing"
    
    if query:=st.chat_input("Enter your query"):
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)
        try:
            response = requests.post(
                "http://127.0.0.1:8000/search_query/",
                json={"chat_id": code, "query": query}
            )

            # Handling the response from the server
            if response.status_code == 200:
                extracted_data = response.json()  # Expecting a string response
                st.success("Query executed successfully!")
                # st.write("**Extracted Content:**")
                with st.expander("**Extracted Content:**"):
                    st.write(extracted_data)
            else:
                error_message = response.json().get("detail", "An error occurred during the search.")
                st.error(f"Error: {error_message}")

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred while connecting to the server: {str(e)}")

        with st.spinner("Generating response..."):
            with st.chat_message("assistant"):
                messages = st.session_state.messages
                messages_str = ""
                for message in messages:
                    if message["role"] == "user":
                        messages_str += f"User: {message['content']}///"
                    elif message["role"] == "assistant":
                        messages_str += f"Assistant: {message['content']}///"
                print(messages_str)
                # refined_prompt=get_query_refiner_prompt(messages_str,query)
                # with st.expander("Refined_Prompt"):
                #     st.write(refined_prompt)
                
                result = st.session_state.chain.invoke({"input": query,"content":extracted_data})
                st.markdown(result.content)
                st.session_state.messages.append({"role": "assistant", "content": result.content})
                # st.write(result['output'])



# if "prompt" not in st.session_state:
#     st.session_state.prompt=get_prompt()

# # Create the LangChain agent

# if "agent_executor" not in st.session_state:
#     llm = ChatOpenAI(api_key=OPENAI_API_KEY)
#     agent = create_openai_tools_agent(llm, [st.session_state.google_tool, st.session_state.pdf_tool, st.session_state.web_tool],st.session_state.prompt)
#     st.session_state.agent_executor = AgentExecutor(agent=agent, tools=[st.session_state.google_tool,st.session_state.pdf_tool, st.session_state.web_tool], verbose=True, handle_parsing_errors=True, max_iterations=5)
#     # st.session_state.agent="available"
# # Streamlit interface





# if query := st.chat_input("Enter your query:"):
#     st.session_state.messages.append({"role": "user", "content": query})
#     with st.chat_message("user"):
#         st.markdown(query)
#     with st.spinner("Generating response..."):
#         with st.chat_message("assistant"):
#             messages = st.session_state.messages
#             messages_str = ""
#             for message in messages:
#                 if message["role"] == "user":
#                     messages_str += f"User: {message['content']}///"
#                 elif message["role"] == "assistant":
#                     messages_str += f"Assistant: {message['content']}///"
#             print(messages_str)
#             # refined_prompt=get_query_refiner_prompt(messages_str,query)
#             # with st.expander("Refined_Prompt"):
#             #     st.write(refined_prompt)
            
#             result = st.session_state.agent_executor.invoke({"input": query})
#             st.markdown(result['output'])
#             st.session_state.messages.append({"role": "assistant", "content": result['output']})
#             # st.write(result['output'])

