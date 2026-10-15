import streamlit as st
import json
import pandas as pd
from idea_generator import generate_ideas
# from keyword_extractor import extract_keywords
from clustering import cluster_ideas
from content_calendar import generate_calendar   # ← renamed import
from keyword_extractor import extract_keywords, generate_wordcloud
from sentiment import analyze_sentiment
from text_analysis import find_duplicates, analyze_readability, reading_ease_label

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Topic Content Planner",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    h1, h2, h3 {
        color: #ffffff !important;
        font-family: 'Segoe UI', sans-serif;
    }
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(90deg, #a78bfa, #f472b6, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        text-align: center;
        color: #cbd5e1;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 16px;
        padding: 18px;
        backdrop-filter: blur(10px);
    }
    div[data-testid="stMetricLabel"] {
        color: #cbd5e1 !important;
        font-size: 0.9rem !important;
    }
    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }
    .idea-card {
        background: rgba(255, 255, 255, 0.07);
        border-left: 4px solid #a78bfa;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
        transition: all 0.2s ease;
    }
    .idea-card:hover {
        background: rgba(255, 255, 255, 0.12);
        transform: translateX(4px);
    }
    .idea-title {
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .idea-desc {
        color: #cbd5e1;
        font-size: 0.92rem;
        margin-bottom: 8px;
    }
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .badge-type { background: #6366f1; color: white; }
    .badge-easy { background: #10b981; color: white; }
    .badge-medium { background: #f59e0b; color: white; }
    .badge-hard { background: #ef4444; color: white; }
    section[data-testid="stSidebar"] {
        background: rgba(0, 0, 0, 0.4);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #cbd5e1;
        border-radius: 8px;
        padding: 8px 18px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #6366f1, #a855f7) !important;
        color: white !important;
    }
    .stButton > button {
        background: linear-gradient(90deg, #6366f1, #a855f7);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
        width: 100%;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.5);
    }
</style>
""", unsafe_allow_html=True)


# ---------- HEADER ----------
st.markdown('<div class="main-title">📅 AI Topic Content Planner</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Turn any topic into a complete content strategy — powered by NLP & AI</div>', unsafe_allow_html=True)

if 'topic' in locals() and topic:
    st.markdown(f'<p style="text-align:center;color:#a78bfa;font-size:1.1rem;">📌 Planning content for: <b>{topic}</b></p>', unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    topic = st.text_input("Enter your niche or topic", "Data Science for beginners")
    # num_ideas = st.slider("Number of content ideas", 5, 30, 15)
    num_ideas = st.select_slider(
    "Number of content ideas",
    options=[5, 10, 15, 20, 25, 30],
    value=15
)
    posts_per_week = st.slider("Posts per week", 1, 7, 3)

    st.markdown("---")
    st.markdown("### 🎯 Content Type Filter")
    content_filter = st.multiselect(
        "Filter by content type",
        ["Blog", "Video", "Reel", "Post"],
        default=["Blog", "Video", "Reel", "Post"]
    )

    st.markdown("---")
    generate_btn = st.button("🚀 Generate Content Plan", use_container_width=True)


# ---------- MAIN LOGIC ----------
if generate_btn:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("🧠 Analyzing topic and generating ideas..."):
            try:
                data = generate_ideas(topic, num_ideas)
                ideas = data.get("ideas", [])
            except Exception as e:
                st.error(f"Error: {e}")
                st.stop()

        if not ideas:
            st.warning("No ideas generated. Please try again.")
            st.stop()

        if content_filter:
            ideas = [i for i in ideas if i.get("content_type") in content_filter]

        # ---------- METRICS ----------
                # ---------- METRICS (sirf ek baar) ----------
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("💡 Total Ideas", len(ideas))
        col2.metric("📌 Topic", topic[:15] + ("..." if len(topic) > 15 else ""))
        col3.metric("📅 Posts/Week", posts_per_week)
        col4.metric("🎯 Content Types", len(set(i.get("content_type", "") for i in ideas)))

        # Sentiment metric
        sentiments = [analyze_sentiment(i["title"] + " " + i["description"]) for i in ideas]
        positive_count = sum(1 for s in sentiments if s["label"] == "Positive")
        col5.metric("😊 Positive Vibe", f"{positive_count}/{len(ideas)}")

        st.markdown("---")

        # ---------- TABS (ek baar) ----------
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "💡 Ideas", "🔑 Keywords", "🗂️ Clusters", "📆 Calendar", "📊 Analytics"
        ])

                # ----- TAB 1: IDEAS -----
        with tab1:
            st.markdown("### 💡 Generated Content Ideas")
            st.caption("Scroll to explore all ideas")

            for idx, idea in enumerate(ideas, 1):
                title = idea.get("title", "Untitled")
                desc = idea.get("description", "")
                ctype = idea.get("content_type", "Post")
                diff = idea.get("difficulty", "Medium").lower()
                diff_class = f"badge-{diff}" if diff in ["easy", "medium", "hard"] else "badge-medium"

                # Sentiment analysis (HTML ke bahar)
                sentiment = analyze_sentiment(title + ". " + desc)
                sent_badge = f'<span class="badge badge-type">{sentiment["emoji"]} {sentiment["label"]}</span>'

                st.markdown(f"""
                <div class="idea-card">
                    <div class="idea-title">{idx}. {title}</div>
                    <div class="idea-desc">{desc}</div>
                    <span class="badge badge-type">📄 {ctype}</span>
                    <span class="badge {diff_class}">⚡ {diff.capitalize()}</span>
                    {sent_badge}
                </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns([1, 5])
                with col1:
                    if st.button(f"📝 Script", key=f"script_{idx}"):
                        st.session_state[f"show_script_{idx}"] = not st.session_state.get(f"show_script_{idx}", False)

                if st.session_state.get(f"show_script_{idx}", False):
                    with st.spinner("Generating script..."):
                        from idea_generator import generate_script
                        script = generate_script(title, ctype, topic)
                        st.markdown(script)

                st.markdown("---")

            df = pd.DataFrame(ideas)
            st.download_button(
                "⬇️ Download Ideas (CSV)",
                df.to_csv(index=False),
                file_name="content_ideas.csv",
                mime="text/csv"
            )

               # ----- TAB 2: KEYWORDS -----
        with tab2:
            st.markdown("### 🔑 SEO Keywords & Entities")
            all_text = " ".join([i["title"] + ". " + i["description"] for i in ideas])
            kw = extract_keywords(all_text)

            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("#### 📊 Top Keywords")
                kws = kw.get("keywords", [])
                if kws:
                    for k in kws:
                        st.markdown(f"- {k}")
                else:
                    st.info("No keywords found.")
            with col_b:
                st.markdown("#### 🏷️ Named Entities")
                entities = kw.get("entities", [])
                if entities:
                    for ent, label in entities:
                        st.markdown(f"- **{ent}** `{label}`")
                else:
                    st.info("No entities found.")

            st.markdown("---")
            st.markdown("#### ☁️ Keyword Word Cloud")
            if all_text.strip():
                st.pyplot(generate_wordcloud(all_text))

        # ----- TAB 3: CLUSTERS -----
        with tab3:
            st.markdown("### 🗂️ Topic Clusters")
            st.caption("Similar ideas grouped using TF-IDF + K-Means (auto-optimized)")

            titles = [i["title"] for i in ideas]
            clusters = cluster_ideas(titles)

            for cname, items in clusters.items():
                with st.expander(f"{cname} — {len(items)} ideas", expanded=True):
                    for it in items:
                        st.markdown(f"• {it}")

        # ----- TAB 4: CALENDAR -----
        with tab4:
            st.markdown("### 📆 Your Content Calendar")
            st.caption("Auto-scheduled publishing plan")

            cal = generate_calendar(titles, posts_per_week=posts_per_week)
            cal_df = pd.DataFrame(cal)
            cal_df.columns = ["Date", "Day", "Content Idea"]

            st.dataframe(cal_df, use_container_width=True, hide_index=True)

            st.download_button(
                "⬇️ Download Calendar (CSV)",
                cal_df.to_csv(index=False),
                file_name="content_calendar.csv",
                mime="text/csv"
            )

        # ----- TAB 5: ANALYTICS -----
        with tab5:
            st.markdown("### 📊 Content Analytics")

            from text_analysis import find_duplicates, analyze_readability, reading_ease_label

            # 1. Duplicate Detection
            st.markdown("#### 🔍 Duplicate Idea Detection")
            titles_list = [{"title": i["title"]} for i in ideas]
            dups = find_duplicates(titles_list)
            if dups:
                st.warning(f"Found {len(dups)} similar idea pair(s):")
                for d in dups:
                    st.markdown(f"- **{d['idea1']}** ↔ **{d['idea2']}** (similarity: {d['similarity']})")
            else:
                st.success("✅ No duplicate ideas found. All ideas are unique!")

            st.markdown("---")

            # 2. Readability Analysis
                        # 2. Readability Analysis (based on descriptions, not titles)
            st.markdown("#### 📖 Readability Analysis")
            all_descriptions = " ".join([i.get("description", "") for i in ideas])
            if all_descriptions.strip():
                readability = analyze_readability(all_descriptions)

                c1, c2, c3 = st.columns(3)
                c1.metric("Flesch Score", readability["flesch_score"])
                c2.metric("Reading Ease", reading_ease_label(readability["flesch_score"]))
                c3.metric("Grade Level", readability["grade_level"])

                st.caption(f"📝 Total words: {readability['word_count']} | ⏱️ Estimated read time: {int(readability['reading_time_sec'])} sec")
            else:
                st.info("No descriptions available for readability analysis.")
    st.markdown("""
    <div style="text-align:center; padding: 60px 20px; color:#cbd5e1;">
        <h2 style="color:#a78bfa;">👈 Get Started</h2>
        <p style="font-size:1.1rem;">Enter your topic in the sidebar and click <b>Generate Content Plan</b></p>
        <p style="font-size:0.95rem; opacity:0.7;">Get content ideas, SEO keywords, topic clusters, and a publishing calendar — all in one place.</p>
    </div>
    """, unsafe_allow_html=True)


# Footer (else ke bahar bhi chalega)
st.markdown("""
<div style="text-align:center; padding:40px 0 20px; color:#64748b; font-size:0.85rem;">
    Built with ❤️ using Streamlit, spaCy, scikit-learn & Gemini AI
</div>
""", unsafe_allow_html=True)