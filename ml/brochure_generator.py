from dotenv import load_dotenv
import os
# Load .env file
load_dotenv()
from bs4 import BeautifulSoup
import requests
# Get OpenAI keys from .env file
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")



from langchain_community.chat_models import ChatOpenAI
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def generate_brochure(input:str):
    product_schema=ResponseSchema(
        name="description",
        description="This is the description for the given product"
    )
    tagline_schema=ResponseSchema(
        name="explaination",
        description="This is the tagline for the given product"
    )
    response_schema=[product_schema,tagline_schema]
    output_parser=StructuredOutputParser.from_response_schemas(response_schema)
    format_instructions=output_parser.get_format_instructions()
  
    from langchain_core.prompts import (
        ChatPromptTemplate,
        # MessagesPlaceholder,
        # HumanMessagePromptTemplate,
        # SystemMessagePromptTemplate,
    )

    

    prompt_template="""
            Generate a brochure for the given product {product} for the age group {age_group}
            {format_instructions}
            """ 

    prompt = ChatPromptTemplate.from_template(template=prompt_template)
    messages=prompt.format_messages(
        input=input,
        format_instructions=format_instructions
    )
    return model.invoke(messages)
