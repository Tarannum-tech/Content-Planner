# 📅 AI Topic Content Planner

An NLP-powered content planning tool that generates content ideas, SEO keywords, sentiment analysis, topic clusters, and a publishing calendar from a single topic — built with Python, spaCy, scikit-learn, Streamlit, and Google Gemini API.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36-red)
![spaCy](https://img.shields.io/badge/spaCy-3.7-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 What It Does

Content creators face "blank page syndrome" — they struggle to come up with fresh ideas, optimize for SEO, and plan a publishing schedule. **AI Topic Content Planner** solves this in **under 10 seconds** by combining Large Language Models with traditional NLP techniques.

**Input:** A topic (e.g., "cooking for beginners")
**Output:** A complete content strategy — ideas, keywords, sentiment, clusters, and a calendar.

---

## ✨ Features

| Feature | Technique |
|---------|-----------|
| 🤖 AI Idea Generation | Google Gemini LLM |
| 🔑 SEO Keyword Extraction | spaCy Noun Chunks |
| 🏷️ Named Entity Recognition | spaCy NER |
| 😊 Sentiment Analysis | TextBlob |
| 🗂️ Topic Clustering | TF-IDF + K-Means |
| 🔍 Duplicate Detection | Cosine Similarity |
| 📖 Readability Analysis | Flesch-Kincaid |
| 📆 Auto Content Calendar | Custom scheduler |
| ☁️ Word Cloud Visualization | WordCloud library |
| 📝 Script Generator | LLM-based |
| ⬇️ CSV Export | Pandas |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Language** | Python 3.12 |
| **NLP** | spaCy, TextBlob, textstat |
| **ML** | scikit-learn (TF-IDF, K-Means, Cosine Similarity) |
| **LLM** | Google Gemini API (gemini-1.5-flash) |
| **UI** | Streamlit |
| **Visualization** | Matplotlib, WordCloud |
| **Data** | Pandas, NumPy |

---

## 🔄 NLP Pipeline
