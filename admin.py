
import streamlit as st
import pandas as pd
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="FAQ Admin Dashboard",
    page_icon="⚙️",
    layout="wide"
)

# Dataset location
FAQ_FILE = Path("data/faqs.csv")

REQUIRED_COLUMNS = [
    "faq_id",
    "category",
    "question",
    "answer"
]

# Load FAQ dataset
def load_faqs():
    if not FAQ_FILE.exists():
        FAQ_FILE.parent.mkdir(parents=True, exist_ok=True)

        pd.DataFrame(columns=REQUIRED_COLUMNS).to_csv(
            FAQ_FILE, index=False
        )

    df = pd.read_csv(FAQ_FILE)

    if not all(col in df.columns for col in REQUIRED_COLUMNS):
        raise ValueError(
            "CSV must contain: faq_id, category, question, answer"
        )

    return df


# Save FAQ dataset
def save_faqs(df):
    df.to_csv(FAQ_FILE, index=False)


# Dashboard heading
st.title("⚙️ FAQ Assistant - Admin Dashboard")
st.caption("Manage your customer support knowledge base.")

# Load dataset
try:
    faqs = load_faqs()
except Exception as error:
    st.error(f"Dataset error: {error}")
    st.stop()

# Dashboard metrics
total_faqs = len(faqs)
total_categories = faqs["category"].nunique()

col1, col2 = st.columns(2)

col1.metric("Total FAQs", total_faqs)
col2.metric("Total Categories", total_categories)

st.divider()

# Dashboard navigation
tab1, tab2, tab3, tab4 = st.tabs([
    "View FAQs",
    "Add FAQ",
    "Edit FAQ",
    "Delete FAQ"
])


# TAB 1: VIEW FAQs
with tab1:

    st.subheader("FAQ Knowledge Base")

    search = st.text_input("Search FAQs")

    if search:
        filtered = faqs[
            faqs.astype(str).apply(
                lambda row: row.str.contains(
                    search, case=False, regex=False
                ).any(),
                axis=1
            )
        ]
    else:
        filtered = faqs

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )

    st.caption(f"Showing {len(filtered)} FAQ records")


# TAB 2: ADD FAQ
with tab2:

    st.subheader("Add New FAQ")

    with st.form("add_faq_form"):

        category = st.text_input("Category")

        question = st.text_area("FAQ Question")

        answer = st.text_area("FAQ Answer")

        submitted = st.form_submit_button(
            "Add FAQ",
            type="primary"
        )

        if submitted:

            if not category.strip() or not question.strip() or not answer.strip():
                st.error("Please fill in all fields.")

            else:

                if len(faqs) == 0:
                    new_id = 1
                else:
                    new_id = int(
                        pd.to_numeric(
                            faqs["faq_id"], errors="raise"
                        ).max()
                    ) + 1

                new_faq = pd.DataFrame([{
                    "faq_id": new_id,
                    "category": category.strip(),
                    "question": question.strip(),
                    "answer": answer.strip()
                }])

                updated_faqs = pd.concat(
                    [faqs, new_faq],
                    ignore_index=True
                )

                save_faqs(updated_faqs)

                st.success("FAQ added successfully!")
                st.rerun()


# TAB 3: EDIT FAQ
with tab3:

    st.subheader("Edit Existing FAQ")

    if not faqs.empty:

        selected_id = st.selectbox(
            "Select FAQ ID",
            faqs["faq_id"].tolist(),
            key="edit_faq_id"
        )

        selected = faqs[
            faqs["faq_id"] == selected_id
        ].iloc[0]

        with st.form("edit_faq_form"):

            new_category = st.text_input(
                "Category",
                value=str(selected["category"])
            )

            new_question = st.text_area(
                "Question",
                value=str(selected["question"])
            )

            new_answer = st.text_area(
                "Answer",
                value=str(selected["answer"])
            )

            update = st.form_submit_button(
                "Update FAQ",
                type="primary"
            )

            if update:

                if not new_category.strip() or not new_question.strip() or not new_answer.strip():
                    st.error("All fields are required.")

                else:

                    updated_faqs = faqs.copy()

                    mask = (
                        updated_faqs["faq_id"] == selected_id
                    )

                    updated_faqs.loc[mask, "category"] = new_category.strip()
                    updated_faqs.loc[mask, "question"] = new_question.strip()
                    updated_faqs.loc[mask, "answer"] = new_answer.strip()

                    save_faqs(updated_faqs)

                    st.success("FAQ updated successfully!")
                    st.rerun()

    else:
        st.info("No FAQs available to edit.")


# TAB 4: DELETE FAQ
with tab4:

    st.subheader("Delete FAQ")

    if not faqs.empty:

        delete_id = st.selectbox(
            "Select FAQ to delete",
            faqs["faq_id"].tolist(),
            key="delete_faq_id"
        )

        st.warning(
            "You are about to permanently delete this FAQ."
        )

        confirm = st.checkbox(
            "I confirm that I want to delete this FAQ."
        )

        if st.button("Delete FAQ", type="primary"):

            if confirm:

                updated_faqs = faqs[
                    faqs["faq_id"] != delete_id
                ]

                save_faqs(updated_faqs)

                st.success("FAQ deleted successfully!")
                st.rerun()

            else:
                st.error("Please confirm before deleting.")

    else:
        st.info("No FAQs available to delete.")


st.divider()

st.caption("AI-Powered Customer Support FAQ Assistant | Admin Panel")
