import requests
import streamlit as st
import os


API_URL = os.getenv(
    "API_URL",
    st.secrets.get(
        "API_URL",
        "http://127.0.0.1:8000/ask"
    )
)


st.set_page_config(
    page_title="InterviewIQ",
    page_icon="🤖",
    layout="wide"
)


st.title("🤖 InterviewIQ")
#st.caption("AI Engineer Interview Assistant")
st.subheader("AI Engineer Interview Assistant")

st.write(
    "Ask questions about Python, Machine Learning, "
    "RAG, Databases, DSA, and AI Engineering."
)


# -----------------------------
# Initialize chat history
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# Display previous messages
# -----------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            sources = message.get("sources", [])

            if sources:

                with st.expander("📚 Sources"):

                    for source in sources:
                        st.write(f"- `{source}`")


# -----------------------------
# Chat input
# -----------------------------

question = st.chat_input(
    "Ask an AI Engineering question..."
)


if question:

    # Display user message
    with st.chat_message("user"):
        st.markdown(question)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # Build conversation history
    history = [
        {
            "role": message["role"],
            "content": message["content"]
        }
        for message in st.session_state.messages[:-1]
    ]


    # Call FastAPI
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = requests.post(
                    API_URL,
                    json={
                        "question": question,
                        "history": history
                    },
                    timeout=60
                )

                response.raise_for_status()

                data = response.json()

                answer = data["answer"]

                st.markdown(answer)


                sources = data.get("sources", [])

                if sources:

                    with st.expander("📚 Sources"):

                        for source in sources:
                            st.write(
                                f"- `{source}`"
                            )


                # Store assistant response

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    }
                )


            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to FastAPI. "
                    "Make sure Uvicorn is running."
                )

            except requests.exceptions.RequestException as e:

                st.error(
                    f"API request failed: {e}"
                )