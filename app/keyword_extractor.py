import spacy
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

nlp = spacy.load("en_core_web_sm")


def extract_keywords(text: str, top_n: int = 15):
    """
    Extract keywords using spaCy noun chunks + named entities.
    Better than RAKE for short, meaningful keywords.
    """
    doc = nlp(text)

    # Noun chunks (e.g., "knife skills", "sourdough bread")
    noun_chunks = [
        chunk.text.lower().strip()
        for chunk in doc.noun_chunks
        if 1 < len(chunk.text.split()) <= 3
        and not chunk.root.is_stop
    ]

    # Named entities
    entities = [
        (ent.text, ent.label_)
        for ent in doc.ents
        if ent.label_ in ["PERSON", "ORG", "PRODUCT", "GPE", "NORP", "WORK_OF_ART", "EVENT"]
    ]

    # Frequency count
    freq = Counter(noun_chunks)
    top_keywords = [kw for kw, _ in freq.most_common(top_n)]

    # Deduplicate entities
    seen = set()
    unique_entities = []
    for ent, label in entities:
        if ent.lower() not in seen:
            seen.add(ent.lower())
            unique_entities.append((ent, label))

    return {
        "keywords": top_keywords,
        "entities": unique_entities[:15]
    }


def generate_wordcloud(text: str):
    wc = WordCloud(
        width=1000, height=500,
        background_color=None, mode="RGBA",
        colormap="cool", max_words=60
    ).generate(text)

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    fig.patch.set_alpha(0)
    return fig