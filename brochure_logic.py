import os
import json
from dotenv import load_dotenv
from scraper import fetch_website_links, fetch_website_contents
from google import genai

load_dotenv(override=True)
api_key = os.getenv('GEMINI_API_KEY')

if api_key and api_key.startswith('AQ'):
    print("all good")
else:
    print("There might be a problem with your API key?")

MODEL = 'gemini-2.5-flash'
client = genai.Client(api_key=api_key)

link_system_prompt = """
You are provided with a list of links found on a webpage.
You are able to decide which of the links would be most relevant to include in a brochure about the company,
such as links to an About page, or a Company page, or Careers/Jobs pages.
You should respond in JSON as in this example:

{
    "links": [ 
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page", "url": "https://another.full.url/careers"}
    ]
}
"""

def get_links_user_prompt(url):
    user_prompt = f"""
Here is the list of links on the website {url} -
Please decide which of these are relevant web links for a brochure about the company, 
respond with the full https URL in JSON format.
Do not include Terms of Service, Privacy, email links.

Links (some might be relative links):

"""
    links = fetch_website_links(url)
    user_prompt += "\n".join(links)
    return user_prompt

MODEL = 'gemini-3.5-flash-lite'
def select_relevant_links(url):
    response = client.models.generate_content(
        model=MODEL,
        contents=get_links_user_prompt(url),
        config={
            "system_instruction": link_system_prompt,
            "response_mime_type": "application/json"
        }
    )
    result = response.text
    links = json.loads(result)
    return links


def fetch_page_and_all_relevant_links(url):
    contents = fetch_website_contents(url)
    relevant_links = select_relevant_links(url)
    result = f"## Landing Page:\n\n{contents}\n## Relevant Links:\n"
    for link in relevant_links['links']:
        result += f"\n\n### Link: {link['type']}\n"
        result += fetch_website_contents(link["url"])
    return result

brochure_system_prompt = """
You are an assistant that analyzes the contents of several relevant pages from a company website
and creates a short brochure about the company for prospective customers, investors and recruits.
Respond in markdown without code blocks.
Include details of company culture, customers and careers/jobs if you have the information.
"""

def get_brochure_user_prompt(company_name, url):
    user_prompt = f"""
You are looking at a company called: {company_name}
Here are the contents of its landing page and other relevant pages;
use this information to build a short brochure of the company in markdown without code blocks.\n\n
"""
    user_prompt += fetch_page_and_all_relevant_links(url)
    user_prompt = user_prompt[:5_000] # Truncate if more than 5,000 characters
    return user_prompt

def create_brochure(company_name, url):
    response = client.models.generate_content(
        model=MODEL,
        contents =get_brochure_user_prompt(company_name, url),
        config={
            "system_instruction": brochure_system_prompt
            }
        
    )
    result = response.text
    return result