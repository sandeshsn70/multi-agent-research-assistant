from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
import os
from dotenv import load_dotenv

load_dotenv()

provider = os.getenv("LLM_PROVIDER", "groq").lower()

if provider == "groq":
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        max_tokens=1200,
        max_retries=1,
        timeout=60
    )
elif provider == "gemini":
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        max_output_tokens=1200,
        max_retries=1,
        timeout=60
    )
else:
    raise ValueError("LLM_PROVIDER must be 'groq' or 'gemini'")

def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search]
    )

def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )

writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports. Avoid repetition and unsupported claims."),
    ("human", """Write a concise, factual research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 points)
- Conclusion
- Sources (include URLs found in the research)

Do not invent sources or URLs."""),
])

writer_chain = writer_prompt | llm | StrOutputParser()

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a constructive research critic. Evaluate accuracy, evidence, clarity and completeness. Be specific and concise."),
    ("human", """Review the research report below.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm | StrOutputParser()
