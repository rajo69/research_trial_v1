## https://serper.dev/

from dotenv import load_dotenv
import streamlit as st
load_dotenv()
import os


os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
os.environ['SERPER_API_KEY'] = st.secrets['SERPER_API_KEY']

from crewai_tools import SerperDevTool, ScrapeWebsiteTool


# Initialize the tool for internet searching capabilities
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()