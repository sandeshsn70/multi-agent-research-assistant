# 🔬 Multi-Agent Research Assistant

An AI-powered research application that uses multiple specialized agents to search the web, extract information, generate research reports, and review the results. Built with Python, LangChain, Groq, Tavily, and Streamlit.

## 🚀 Features

- **Search Agent:** Finds relevant information from the web.
- **Reader Agent:** Extracts useful content from selected URLs.
- **Writer Agent:** Generates structured research reports.
- **Critic Agent:** Reviews the generated report and provides feedback.
- **Interactive UI:** Explore research results through a Streamlit dashboard.
- **Download Reports:** Save research reports for future reference.

## 🛠️ Tech Stack

- Python
- Streamlit
- LangChain
- LangGraph
- Groq API
- Tavily Search API
- BeautifulSoup
- Requests

## 📁 Project Structure

```text
Multi-Agent-Research-Assistant/
├── app.py
├── agents.py
├── pipeline.py
├── tools.py
├── requirements.txt
├── .env
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/sandeshsn70/multi-agent-research-assistant.git
cd multi-agent-research-assistant
```

### 2. Create a virtual environment

```bash
uv venv
```

### 3. Install dependencies

```bash
uv pip install --python .venv/Scripts/python.exe -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and add your API keys using the variable names expected by your code.

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Get your API keys from:

- [Groq Console](https://console.groq.com/)
- [Tavily](https://tavily.com/)

**Important:** Never upload your `.env` file or expose your API keys on GitHub.

### 5. Run the application

```powershell
.venv\Scripts\python.exe -m streamlit run app.py
```

Open the local URL displayed in your terminal, usually `http://localhost:8501`.

## 🔄 Workflow

1. Enter a research topic.
2. The Search Agent finds relevant sources.
3. The Reader Agent extracts useful information.
4. The Writer Agent creates a research report.
5. The Critic Agent reviews the report.
6. View and download the results from the dashboard.

## 👨‍💻 Author

**Sandesh Naikwade**

- GitHub: [@sandeshsn70](https://github.com/sandeshsn70)

---

⭐ If you find this project useful, consider giving the repository a star.
