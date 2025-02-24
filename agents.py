from crewai import Agent
from tools import search_tool, scrape_tool
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
import os


## call the gemini models
llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                           verbose=True,
                           temperature=0.5,
                           google_api_key=st.secrets["GOOGLE_API_KEY"])

# Creating a senior researcher agent with memory and verbose mode
comp_res=Agent(
    role="""An expert in retail market research who leverages deep industry knowledge to assess and classify companies as retail or non-retail, adept at distinguishing between various sales modalities in digital commerce. You also have landing page analytics expertise, combining insights from global web trends, regional user behavior, and market-specific data and an expert researcher of retail headquarter locations, skilled in mining online databases and authoritative resources for corporate geolocation data. Finally, you are a seasoned data formatter and writer.""",
    goal="You quickly and accurately capture a company’s core identity by summarizing its homepage content in a concise, single-sentence overview then determine with confidence whether a given company qualifies as a retailer based on a strict set of definitions and exclusion criteria then analyze and classify the payment processing methods used on a company’s product page, thus revealing the underlying e-commerce model identify the most impactful landing pages for a company on a global, European, and UK level then gather and verify critical headquarter information, ensuring that the company’s main physical presence is clearly mapped and documented. Finally you Collect relevant data from all the agents and save it in a structured manner in a markdown file.",
    verbose=True,
    memory=True,
    backstory=(
        """You emerged from a background in investigative journalism and digital analysis."""
    ),
    tools=[search_tool, scrape_tool],
    llm=llm,
)

reviewer=Agent(
    role='Review the final output and exit',
    goal='Exit chain of thought',
    verbose=True,
    backstory=(
        """You know when to stop"""
    ),
    memory=True,
    llm=llm,
)