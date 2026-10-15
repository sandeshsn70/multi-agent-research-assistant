import streamlit as st
from datetime import datetime
from pipeline import run_research_pipeline

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0b1020;
    color: #e8ecf8;
}

[data-testid="stSidebar"] {
    background: #11182b;
    border-right: 1px solid #26304a;
}

.hero {
    padding: 32px;
    border-radius: 22px;
    background: linear-gradient(135deg, #171f3b, #25205a, #17182e);
    border: 1px solid #383b70;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 36px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 10px;
}

.hero p {
    color: #c0c8e4;
    font-size: 15px;
}

.eyebrow {
    color: #a99bff;
    text-transform: uppercase;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
}

.agent-card {
    background: #141c30;
    border: 1px solid #293550;
    padding: 18px;
    border-radius: 15px;
    min-height: 125px;
    margin-bottom: 12px;
}

.agent-icon {
    font-size: 25px;
    margin-bottom: 8px;
}

.agent-title {
    font-weight: 700;
    color: #ffffff;
    font-size: 15px;
}

.agent-description {
    font-size: 12px;
    color: #a7b2cc;
    margin-top: 6px;
}

.metric-card {
    background: #141c30;
    border: 1px solid #293550;
    border-radius: 14px;
    padding: 17px;
}

.metric-label {
    color: #a7b2cc;
    font-size: 12px;
}

.metric-value {
    color: #ffffff;
    font-size: 24px;
    font-weight: 800;
    margin-top: 6px;
}

.section-heading {
    font-size: 21px;
    font-weight: 750;
    color: #ffffff;
    margin: 22px 0 14px 0;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #7465f5, #a06aff);
    border: none;
    border-radius: 10px;
    min-height: 46px;
    font-weight: 700;
    color: white;
}

div.stButton > button[kind="primary"]:hover {
    border: 1px solid #c0b6ff;
    color: white;
}

.stTextArea textarea, .stTextInput input {
    background: #11182b;
    color: white;
    border: 1px solid #36415e;
    border-radius: 10px;
}

div[data-testid="stTabs"] button {
    color: #c6cde0;
}

.footer {
    border-top: 1px solid #293550;
    padding-top: 18px;
    margin-top: 40px;
    color: #8793af;
    font-size: 11px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "research_history" not in st.session_state:
    st.session_state.research_history = []

if "current_result" not in st.session_state:
    st.session_state.current_result = None

if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------
def extract_text(value):
    """Convert common agent response objects into displayable text."""
    if value is None:
        return ""

    if isinstance(value, str):
        return value

    content = getattr(value, "content", None)
    if content is not None:
        return str(content)

    return str(value)


def render_agent_card(icon, title, description):
    st.markdown(
        f"""
        <div class="agent-card">
            <div class="agent-icon">{icon}</div>
            <div class="agent-title">{title}</div>
            <div class="agent-description">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.markdown("## 🔬 Multi-Agent")
    st.markdown("### Research Assistant")
    st.caption("AUTONOMOUS RESEARCH WORKSPACE")

    st.divider()

    st.markdown("#### ⚙️ Research Settings")

    research_depth = st.selectbox(
        "Report focus",
        [
            "Comprehensive Research",
            "Technical Analysis",
            "Business Insights",
            "Academic Research",
        ],
    )

    show_sources = st.toggle(
        "Show search results",
        value=True,
    )

    show_scraped_content = st.toggle(
        "Show extracted content",
        value=True,
    )

    st.divider()

    st.markdown("#### 🕘 Recent Research")

    if st.session_state.research_history:
        for item in reversed(st.session_state.research_history[-5:]):
            if st.button(
                f"📄 {item['topic'][:30]}",
                key=f"history_{item['id']}",
                use_container_width=True,
            ):
                st.session_state.current_result = item["result"]
                st.session_state.last_topic = item["topic"]
                st.rerun()
    else:
        st.caption("Your research history will appear here.")

    st.divider()

    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.research_history = []
        st.session_state.current_result = None
        st.session_state.last_topic = ""
        st.rerun()

    st.caption("Built with Streamlit and your agent pipeline.")

# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="eyebrow">AI-powered research workspace</div>
    <h1>Multi-Agent Research Assistant 🔬</h1>
    <p>
        Research complex topics using specialized AI agents.
        Search the web, extract relevant content, generate reports,
        and review the final output in one workspace.
    </p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# AGENT PIPELINE OVERVIEW
# --------------------------------------------------
st.markdown('<div class="section-heading">Your AI research team</div>',
            unsafe_allow_html=True)

agent_columns = st.columns(4)

agents = [
    (
        "🔎",
        "Search Agent",
        "Finds relevant information and research sources.",
    ),
    (
        "📖",
        "Reader Agent",
        "Extracts useful information from selected sources.",
    ),
    (
        "✍️",
        "Writer Agent",
        "Creates a structured report from collected evidence.",
    ),
    (
        "🛡️",
        "Critic Agent",
        "Reviews the report and provides feedback.",
    ),
]

for column, agent in zip(agent_columns, agents):
    with column:
        render_agent_card(*agent)

# --------------------------------------------------
# RESEARCH INPUT
# --------------------------------------------------
st.markdown('<div class="section-heading">Start a new research task</div>',
            unsafe_allow_html=True)

with st.form("research_form"):
    topic = st.text_area(
        "Research topic",
        placeholder=(
            "Example: How are multi-agent AI systems transforming "
            "healthcare, finance, and software development?"
        ),
        height=115,
        help="Enter a specific topic for more focused research.",
    )

    submitted = st.form_submit_button(
        "🚀 Start AI Research",
        type="primary",
        use_container_width=True,
    )

if submitted:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()

        stage_names = {
            1: "🔎 Search Agent: Finding relevant sources...",
            2: "📖 Reader Agent: Extracting useful information...",
            3: "✍️ Writer Agent: Generating the report...",
            4: "🛡️ Critic Agent: Reviewing the report...",
        }

        def update_progress(stage_number, label):
            progress_bar.progress(
                min(max(int(stage_number), 0), 4) / 4
            )
            status_text.info(label)

        try:
            with st.spinner("Your research team is working..."):
                # The callback is optional. The pipeline should accept it
                # for live stage updates; see compatibility note below.
                result = run_research_pipeline(
                    topic.strip(),
                    progress_callback=update_progress,
                )

            if not isinstance(result, dict):
                raise TypeError(
                    "run_research_pipeline() must return a dictionary."
                )

            st.session_state.current_result = result
            st.session_state.last_topic = topic.strip()

            st.session_state.research_history.append({
                "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
                "topic": topic.strip(),
                "result": result,
            })

            progress_bar.progress(1.0)
            status_text.success("Research completed successfully!")

        except TypeError as exc:
            # If the existing pipeline has no progress_callback parameter,
            # retry only when the error indicates that unsupported argument.
            if "progress_callback" not in str(exc):
                st.error(f"Research failed: {exc}")
            else:
                try:
                    with st.spinner("Running your existing research pipeline..."):
                        result = run_research_pipeline(topic.strip())

                    if not isinstance(result, dict):
                        raise TypeError(
                            "run_research_pipeline() must return a dictionary."
                        )

                    st.session_state.current_result = result
                    st.session_state.last_topic = topic.strip()

                    st.session_state.research_history.append({
                        "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
                        "topic": topic.strip(),
                        "result": result,
                    })

                    progress_bar.progress(1.0)
                    status_text.success("Research completed successfully!")

                except Exception as retry_exc:
                    st.error(f"Research failed: {retry_exc}")

        except Exception as exc:
            st.error(f"Research failed: {exc}")
            st.caption(
                "Check your agent configuration, API key, and terminal logs."
            )

# --------------------------------------------------
# RESULTS DASHBOARD
# --------------------------------------------------
result = st.session_state.current_result

if result:
    st.markdown("---")
    st.markdown(
        '<div class="section-heading">Research results</div>',
        unsafe_allow_html=True,
    )

    report = extract_text(result.get("report", ""))
    feedback = extract_text(result.get("feedback", ""))
    search_results = result.get("search_results", [])
    scraped_content = result.get("scraped_content", "")

    if isinstance(search_results, (dict, list, tuple)):
        search_text = (
            "\n".join(
                str(item) for item in search_results
            )
            if isinstance(search_results, (list, tuple))
            else "\n".join(
                f"**{key}:** {value}"
                for key, value in search_results.items()
            )
        )
    else:
        search_text = extract_text(search_results)

    scraped_text = extract_text(scraped_content)

    metric_columns = st.columns(4)

    metrics = [
        ("Research Topic", st.session_state.last_topic[:24] or "Research"),
        ("Search Results", str(
            len(search_results)
            if isinstance(search_results, (list, tuple, dict))
            else "Available" if search_text else 0
        )),
        ("Report Length", f"{len(report.split())} words"),
        ("Review", "Completed" if feedback else "Unavailable"),
    ]

    for column, (label, value) in zip(metric_columns, metrics):
        with column:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    report_tab, critic_tab, search_tab, reader_tab = st.tabs([
        "📝 Final Report",
        "🛡️ Critic Review",
        "🔎 Search Results",
        "📖 Extracted Content",
    ])

    with report_tab:
        if report:
            st.markdown(report)
            st.download_button(
                "⬇️ Download Report",
                data=report,
                file_name="research_report.md",
                mime="text/markdown",
                use_container_width=False,
            )
        else:
            st.info("No report was returned by the writer chain.")

    with critic_tab:
        if feedback:
            st.markdown(feedback)
            st.download_button(
                "⬇️ Download Critic Review",
                data=feedback,
                file_name="critic_review.md",
                mime="text/markdown",
            )
        else:
            st.info("No critic feedback was returned.")

    with search_tab:
        if show_sources:
            if search_text.strip():
                st.markdown(search_text)
                st.download_button(
                    "⬇️ Download Search Results",
                    data=search_text,
                    file_name="search_results.txt",
                    mime="text/plain",
                )
            else:
                st.info("No search results were returned.")
        else:
            st.info("Enable 'Show search results' in the sidebar.")

    with reader_tab:
        if show_scraped_content:
            if scraped_text.strip():
                st.markdown(scraped_text)
                st.download_button(
                    "⬇️ Download Extracted Content",
                    data=scraped_text,
                    file_name="extracted_content.txt",
                    mime="text/plain",
                )
            else:
                st.info("No extracted content was returned.")
        else:
            st.info("Enable 'Show extracted content' in the sidebar.")

# --------------------------------------------------
# EMPTY STATE
# --------------------------------------------------
else:
    st.markdown("""
    <div class="agent-card" style="text-align:center; padding:35px;">
        <div style="font-size:40px;">🧠</div>
        <h3 style="color:white;">Ready to investigate?</h3>
        <p style="color:#a7b2cc;">
            Enter a research topic above to start your AI agent workflow.
            Your report and review will appear here.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown("""
<div class="footer">
    MULTI-AGENT RESEARCH ASSISTANT
    <span style="float:right;">Built with Streamlit ✳</span>
</div>
""", unsafe_allow_html=True)
