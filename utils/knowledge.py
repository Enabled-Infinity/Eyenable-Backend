from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
client= OpenAI()

st.set_page_config(page_title="Smart  Assistant", layout="centered")
st.title("🔍 KnowledgeBase Assistant with Tools")

st.markdown("This assistant uses **web search**, **code interpreter**, and **file search** to help answer your questions.")

query = st.text_input("Ask your question:", placeholder="e.g. Summarize latest trends in AI hiring...")

if st.button("Get Response") and query:
    with st.spinner("Thinking..."):
        try:
            response = client.responses.create(
                model="gpt-4o",
                tools=[
                    {"type": "web_search_preview"},
                    {
                        "type": "code_interpreter",
                        "container": {"type": "auto"}
                    },
                    {
                        "type": "file_search",
                        "vector_store_ids": ["vs_685164a170c88191a9378518cdfed08d"]
                    }
                ],
                input=[
                    {
                        "role": "developer",
                        "content": "You are a helpful assistant that guides users and answers questions using context from tools like web search, code interpreter, and file search."
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ]
            )
            st.markdown("### 💬 Response")
            st.write(response.output_text)
        except Exception as e:
            st.error(f"An error occurred: {e}")