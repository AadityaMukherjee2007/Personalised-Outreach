import os 
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader

def init():
    global llm
    load_dotenv()

    os.environ["OPENAI_API_KEY"] = os.getenv("API_KEY", "")

    llm  = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        model="openrouter/free"
    )

def generate_email(company_url):
    if not company_url.startswith("http"):
        company_url = "https://" + company_url


    template = """
    You are an elite B2B sales representative pitching custom AI integration services.
    Analyze the following scraped website data from our target company:
    
    {company_info}
    
    Write a highly personalized, professional cold email to a decision-maker at this company. You MUST strictly follow this exact psychological framework:
    
    1. Trigger: Start with "Hi [Name]," (use a generic name if none is found) and mention one specific, unique thing you noticed about their core product or target audience from the data.
    2. Current Process & Pain: "You're likely [guess their current manual process related to their business]..." followed by "But it's a pain to [state the bottleneck, like scaling, manual data entry, or slow response times]."
    3. Root Cause: "Normally, it's down to [briefly state the root cause, like disconnected software or relying on manual labor]."
    4. The Ask: "Could I share a case study showing how we helped a similar company get [dream outcome] by automating this with AI?"
    
    Keep the tone conversational, concise, and strictly under 5 sentences. Do not use cheesy buzzwords. Make it sound like a human wrote it after studying their website.
    """

    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm

    loader = WebBaseLoader(company_url)
    website_info = loader.load()

    cleaned_up_info = website_info[0].page_content
    response = chain.invoke({"company_info": cleaned_up_info})

    return response.content


def generate_research(company_url):
    ...


def main():
    init()
    company_url = input("URL: ")

    email_content = generate_email(company_url)
    print(email_content)


if __name__ == "__main__":
    main()