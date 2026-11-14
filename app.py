
import streamlit as st
import time
from pathlib import Path

from modules.retrieval import FAQRetriever
from modules.database import (
    initialize_db,
    save_chat,
    save_feedback,
    get_statistics
)

# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent
FAQ_PATH = BASE_DIR / "data" / "faqs.csv"

st.set_page_config(
    page_title="Customer Support Assistant",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------------
# CUSTOM STYLING
# -----------------------------------

st.markdown("""
<style>
.main-title {
    font-size: 30px;
    font-weight: 700;
}
.subtitle {
    color: #888888;
    font-size: 14px;
}
.stChatMessage {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# INITIALIZE DATABASE
# -----------------------------------

initialize_db()

# -----------------------------------
# LOAD FAQ RETRIEVER
# -----------------------------------

@st.cache_resource
def load_retriever():
    return FAQRetriever(str(FAQ_PATH))


if not FAQ_PATH.exists():
    st.error("FAQ dataset not found. Check data/faqs.csv")
    st.stop()

try:
    retriever = load_retriever()
except Exception as error:
    st.error(f"Unable to load FAQ engine: {error}")
    st.stop()

# -----------------------------------
# SESSION STATE
# -----------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "feedback_submitted" not in st.session_state:
    st.session_state.feedback_submitted = set()

# -----------------------------------
# SIDEBAR
# -----------------------------------

with st.sidebar:

    st.title("🤖 FAQ Assistant")

    st.caption("AI-Powered Customer Support")

    st.divider()

    st.subheader("Knowledge Base")

    st.metric(
        "Available FAQs",
        len(retriever.faqs)
    )

    categories = sorted(
        retriever.faqs["category"].unique().tolist()
    )

    st.write("FAQ Categories")

    for category in categories:
        st.write(f"• {category}")

    st.divider()

    st.subheader("Matching Settings")

    threshold = st.slider(
        "Confidence threshold",
        min_value=0.05,
        max_value=0.90,
        value=0.25,
        step=0.05
    )

    st.caption(
        "Higher thresholds make the assistant more selective."
    )

    if st.button("🔄 Reload FAQ Dataset", use_container_width=True):
        st.cache_resource.clear()
        st.rerun()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.caption("Powered by Python, Scikit-learn and Streamlit")

# -----------------------------------
# MAIN HEADER
# -----------------------------------

st.markdown(
    '<div class="main-title">Customer Support Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Ask questions about products, services, '
    'payments, accounts and more.</div>',
    unsafe_allow_html=True
)

st.divider()

# -----------------------------------
# ANALYTICS
# -----------------------------------

stats = get_statistics()

total = stats[0] or 0
answered = stats[1] or 0
fallbacks = stats[2] or 0
avg_time = stats[3] or 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Questions", total)
col2.metric("Answered", answered)
col3.metric("Fallbacks", fallbacks)
col4.metric("Avg Response Time", f"{avg_time:.3f}s")

st.divider()

# -----------------------------------
# WELCOME MESSAGE
# -----------------------------------

if not st.session_state.messages:

    with st.chat_message("assistant", avatar="🤖"):

        st.markdown("""
        ### Hello! Welcome to Customer Support.

        I can help you find information from our FAQ knowledge base.

        **You can ask me about:**
        - Payments and refunds
        - Orders and delivery
        - Account management
        - Subscriptions and software
        - Courses and education

        What would you like to know?
        """)

# -----------------------------------
# DISPLAY CHAT HISTORY
# -----------------------------------

for index, message in enumerate(st.session_state.messages):

    with st.chat_message(
        message["role"],
        avatar="🤖" if message["role"] == "assistant" else "👤"
    ):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            if message.get("matched"):

                st.divider()

                st.caption(
                    f"📚 Source FAQ: {message['source']}"
                )

                st.caption(
                    f"Category: {message['category']}"
                )

                st.progress(
                    min(message["score"], 1.0),
                    text=f"Similarity score: {message['score']:.3f}"
                )

                st.caption(
                    f"Response time: {message['response_time']:.4f} seconds"
                )

                chat_id = message.get("chat_id")

                if (
                    chat_id is not None
                    and chat_id not in st.session_state.feedback_submitted
                ):

                    st.write("Was this answer helpful?")

                    yes_col, no_col = st.columns(2)

                    with yes_col:
                        if st.button(
                            "👍 Yes",
                            key=f"yes_{chat_id}",
                            use_container_width=True
                        ):

                            save_feedback(chat_id, 1)

                            st.session_state.feedback_submitted.add(
                                chat_id
                            )

                            st.success("Thank you for your feedback!")
                            st.rerun()

                    with no_col:
                        if st.button(
                            "👎 No",
                            key=f"no_{chat_id}",
                            use_container_width=True
                        ):

                            save_feedback(chat_id, 0)

                            st.session_state.feedback_submitted.add(
                                chat_id
                            )

                            st.success("Thank you for your feedback!")
                            st.rerun()

                elif chat_id in st.session_state.feedback_submitted:
                    st.caption("✓ Feedback received")

            else:

                st.caption(
                    f"Response time: {message['response_time']:.4f} seconds"
                )

                st.warning("No sufficiently relevant FAQ was found.")

# -----------------------------------
# CHAT INPUT
# -----------------------------------

prompt = st.chat_input(
    "Type your question here..."
)

if prompt:

    # Display user question
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Retrieve answer
    start_time = time.perf_counter()

    result = retriever.search(
        prompt,
        threshold=threshold
    )

    response_time = time.perf_counter() - start_time

    # -----------------------------------
    # MATCHED ANSWER
    # -----------------------------------

    if result["matched"]:

        answer = result["answer"]

        chat_id = save_chat(
            prompt,
            result["faq_id"],
            result["score"],
            response_time,
            "answered"
        )

        assistant_message = {
            "role": "assistant",
            "content": answer,
            "matched": True,
            "source": result["question"],
            "category": result["category"],
            "score": result["score"],
            "response_time": response_time,
            "chat_id": chat_id
        }

    # -----------------------------------
    # FALLBACK RESPONSE
    # -----------------------------------

    else:

        answer = (
            "I'm sorry, I couldn't find a sufficiently relevant "
            "answer in our FAQ knowledge base.\n\n"
            "Please try rephrasing your question or contact "
            "our customer support team for further assistance."
        )

        chat_id = save_chat(
            prompt,
            None,
            result["score"],
            response_time,
            "fallback"
        )

        assistant_message = {
            "role": "assistant",
            "content": answer,
            "matched": False,
            "score": result["score"],
            "response_time": response_time,
            "chat_id": chat_id
        }

    st.session_state.messages.append(assistant_message)

    st.rerun()
