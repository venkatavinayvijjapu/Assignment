# Chatbot with pdf and web url using API

## Overview
This project is a chatbot that allows user to ask questions about a particular pdf file or web url. The chatbot uses a combination of LLM's and vector database to store and retrieve information. We have created a custom API using fastapi framework where we store the collection in chromadb with chat_id as collection name and use the same chat_id to retrive the particular chunk from the collection based on the user query. Upon retrival of chunk we have used openai model to generate the response for the user query.

## Prerequisites

- Python 3.8 or above

## Installation
```bash
pip install -r requirements.txt
```
## Setup Instructions

### Step 1: Clone or download the Repository (if emailed)

```bash
git clone https://github.com/venkatavinayvijjapu/Assignment.git
cd Hygwell Assignment-1
```
### Step 2: Set Up a Virtual Environment

You can use `venv` or `conda` to create an isolated environment for this project.
#### Using `venv`

```bash
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

#### Using `conda`

```bash
conda create --name project_env python=3.8
conda activate project_env
```

## Step 4: Set Up Environment Variables

Create a `.env` file in the root directory and add your OpenAI API keys in a way it can be accessed in the app.

### step 5: Run the API 
```bash
python -m uvicorn api:app --reload
```

### step 6: Run the Streamlit app

```bash
python -m streamlit run app.py
```

### Step 7: Open the Application

Open your web browser and go to `http://localhost:8501`. You can now add you pdf and url and interact with the system by entering your query and selecting the type pdf pr url in select box.

## Project Structure

- **api**: Routes for all the api endpoints i.e pdf_api,web_api,search_api
- **pdf_api**: Contains the endpoint to process the pdf and generate the chat_id and to store the documents contents into chromadb.
- **web_api**: Contains the endpoint to process the web url and generate the chat_id and to store the url data into chromadb.
- **search_api**: Contains the endpoint to search the query in the vector database based on the chat_id generated and retrive the relevant chunks from the database and pass it to the LLM model to generate the response.
- **app.py**: Contains the streamlit code for the front end and interaction with the user.
- **.env**: Stores API keys (make sure this file is not included in version control).
- **requirements.txt**: Lists the project dependencies.

## Video Prototype:
You can watch the demo video [here](https://www.veed.io/view/14b05136-f531-4029-99af-f4cc62bbb843?panel=share).
