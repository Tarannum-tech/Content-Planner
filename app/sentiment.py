from textblob import TextBlob


def analyze_sentiment(text: str) -> dict:
    """
    Analyze sentiment of a text.
    Returns polarity (-1 to 1) and subjectivity (0 to 1).
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity > 0.1:
        label = "Positive"
        emoji = "😊"
    elif polarity < -0.1:
        label = "Negative"
        emoji = "😟"
    else:
        label = "Neutral"
        emoji = "😐"

    return {
        "polarity": round(polarity, 2),
        "subjectivity": round(subjectivity, 2),
        "label": label,
        "emoji": emoji
    }


def analyze_ideas(ideas: list) -> list:
    """Add sentiment to each idea."""
    enriched = []
    for idea in ideas:
        text = idea.get("title", "") + ". " + idea.get("description", "")
        sentiment = analyze_sentiment(text)
        enriched.append({**idea, **sentiment})
    return enriched