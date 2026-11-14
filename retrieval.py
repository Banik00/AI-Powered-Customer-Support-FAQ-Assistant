
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from modules.preprocessing import clean_text


class FAQRetriever:

    def __init__(self, csv_path):

        self.faqs = pd.read_csv(
            csv_path,
            encoding="utf-8-sig"
        ).fillna("")

        required_columns = [
            "faq_id", "category", "question", "answer"
        ]

        for column in required_columns:
            if column not in self.faqs.columns:
                raise ValueError(
                    f"Missing required column: {column}"
                )

        if self.faqs.empty:
            raise ValueError("FAQ dataset is empty.")

        self.faqs["clean_question"] = (
            self.faqs["question"].apply(clean_text)
        )

        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            sublinear_tf=True
        )

        self.faq_vectors = self.vectorizer.fit_transform(
            self.faqs["clean_question"]
        )

    def search(self, user_question, threshold=0.25):

        cleaned_question = clean_text(user_question)

        if not cleaned_question:
            return {
                "matched": False,
                "score": 0.0
            }

        query_vector = self.vectorizer.transform(
            [cleaned_question]
        )

        scores = cosine_similarity(
            query_vector,
            self.faq_vectors
        ).flatten()

        best_index = scores.argmax()
        best_score = float(scores[best_index])

        if best_score < threshold:
            return {
                "matched": False,
                "score": best_score
            }

        faq = self.faqs.iloc[best_index]

        return {
            "matched": True,
            "faq_id": int(faq["faq_id"]),
            "category": faq["category"],
            "question": faq["question"],
            "answer": faq["answer"],
            "score": best_score
        }
