import streamlit as st
from srcflipkart.data_ingestion import DataIngestor
from srcflipkart.rag_agent import RAGAgentBuilder
import uuid

# Load vector store and build RAG agent
vector_store = DataIngestor().ingest(load_existing=True)
rag_agent = RAGAgentBuilder(vector_store).build_agent()

# Streamlit app config
st.set_page_config(page_title="Flipkart Product Recommender Chatbot", layout="centered")
st.title("Flipkart Product Recommender Chatbot")

# Persistent thread_id for the session
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Persistent chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history in chat bubbles
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# Chat input
if prompt := st.chat_input("Ask me about Flipkart products:"):
    # Display user's message immediately
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    try:
        # Get bot response
        response = rag_agent.invoke(
            {"messages": [{"role": "user", "content": prompt}]},
            config={"thread_id": st.session_state.thread_id}
        )
        # AIMessage object handling
        last_msg = response.get("messages", [])[-1] if response.get("messages") else None
        answer = getattr(last_msg, "content", "Sorry, I couldn't find an answer.") if last_msg else "Sorry, I couldn't find an answer."

        # Display bot response
        st.chat_message("assistant").markdown(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

    except Exception as e:
        st.chat_message("assistant").markdown(f"Error: {e}")
        st.session_state.chat_history.append({"role": "assistant", "content": f"Error: {e}"})

# Health check sidebar
st.sidebar.header("Health Check")
st.sidebar.write("Status: Healthy")
