from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import textstat


def find_duplicates(ideas: list, threshold: float = 0.75) -> list:
    """
    Find similar ideas using cosine similarity.
    Returns list of (idea1, idea2, similarity) tuples.
    """
    if len(ideas) < 2:
        return []

    titles = [i["title"] if isinstance(i, dict) else i for i in ideas]
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform(titles)
    similarity_matrix = cosine_similarity(tfidf)

    duplicates = []
    for i in range(len(titles)):
        for j in range(i + 1, len(titles)):
            if similarity_matrix[i][j] >= threshold:
                duplicates.append({
                    "idea1": titles[i],
                    "idea2": titles[j],
                    "similarity": round(float(similarity_matrix[i][j]), 2)
                })
    return duplicates


def analyze_readability(text: str) -> dict:
    """Return readability metrics."""
    return {
        "flesch_score": round(textstat.flesch_reading_ease(text), 1),
        "grade_level": round(textstat.flesch_kincaid_grade(text), 1),
        "word_count": textstat.lexicon_count(text),
        "reading_time_sec": round(textstat.lexicon_count(text) / 4, 0)  # ~240 wpm
    }


def reading_ease_label(score: float) -> str:
    if score >= 80:
        return "🟢 Very Easy"
    elif score >= 60:
        return "🟡 Easy"
    elif score >= 40:
        return "🟠 Moderate"
    else:
        return "🔴 Difficult"