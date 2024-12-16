import re
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise

def cosine_similarity(document1: str, document2: str) -> float:
    """Calculate the cosine similarity between two documents.

    Args:
        document1 (str): The first document.
        document2 (str): The second document.

    Returns:
        float: The cosine similarity between the two documents.
    """
    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Transform the documents into TF-IDF vectors
    vectors = vectorizer.fit_transform([document1, document2])

    # Calculate the cosine similarity between the two vectors
    cosine_similarity_score = pairwise.cosine_similarity(vectors[0], vectors[1])

    return cosine_similarity_score.item()

# input data
resume_details = {
    "summary": "Experienced data scientist with a strong background in machine learning and data analysis.",
    "skills": ["Python", "Machine Learning", "Deep Learning", "Data Visualization"],
    "experience": ["Developed predictive models to optimize business decisions.", "Led a team of data scientists."]
}
user_data = {
    "name": "John Doe",
    "skills": ["Python", "Data Analysis", "Machine Learning"],
    "goal": "Seeking a role in AI-driven data analysis."
}
job_details = {
    "title": "Senior Data Scientist",
    "requirements": ["Expertise in Python, Machine Learning, and Deep Learning.", "Experience in data-driven decision making."]
}

# convert input data into JSON format
resume_details_json = json.dumps(resume_details)
user_data_json = json.dumps(user_data)
job_details_json = json.dumps(job_details)

# calculate metrics
print("\nCalculating cosine_similarity...")
user_personalization = cosine_similarity(resume_details_json, user_data_json)
job_alignment = cosine_similarity(resume_details_json, job_details_json)
hallucination = job_alignment/user_personalization

print(f"User Personalization Score: {user_personalization:.4f}")
print(f"Job Alignment Score: {job_alignment:.4f}")
print(f"Model hallucination Score: {hallucination:.4f}")
