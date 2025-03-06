from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException




load_dotenv()
llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"),model_name="llama-3.3-70b-versatile")


