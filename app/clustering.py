from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def _find_best_k(X, max_k=6):
    """Find optimal number of clusters using silhouette score."""
    best_k = 2
    best_score = -1
    max_k = min(max_k, X.shape[0] - 1)
    for k in range(2, max_k + 1):
        try:
            km = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = km.fit_predict(X)
            if len(set(labels)) < 2:
                continue
            score = silhouette_score(X, labels)
            if score > best_score:
                best_score = score
                best_k = k
        except Exception:
            continue
    return best_k


def cluster_ideas(ideas: list, n_clusters: int = None):
    """
    Cluster similar ideas using TF-IDF + KMeans.
    If n_clusters is None, auto-detects optimal count.
    """
    if len(ideas) < 3:
        return {"All Ideas": ideas}

    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),
        max_features=500
    )
    X = vectorizer.fit_transform(ideas)

    # Auto-detect k if not provided
    if n_clusters is None:
        n_clusters = _find_best_k(X, max_k=min(6, len(ideas) // 2))
    n_clusters = max(2, min(n_clusters, len(ideas) - 1))

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)

    # Group ideas by cluster and give them meaningful names
    clusters = {}
    for idea, label in zip(ideas, labels):
        clusters.setdefault(label, []).append(idea)

    # Auto-generate cluster names using top keywords from that cluster
    named_clusters = {}
    for label, items in clusters.items():
        # Get top terms for this cluster
        cluster_text = " ".join(items)
        vec = TfidfVectorizer(stop_words='english', max_features=3)
        try:
            vec.fit([cluster_text])
            top_terms = vec.get_feature_names_out()
            name = " & ".join([t.title() for t in top_terms[:2]])
        except Exception:
            name = f"Topic {label + 1}"
        named_clusters[f"📁 {name}"] = items

    # Sort by cluster size (biggest first)
    named_clusters = dict(
        sorted(named_clusters.items(), key=lambda x: -len(x[1]))
    )
    return named_clusters