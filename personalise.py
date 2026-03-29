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

    try:
        with open("email_template_prompt.txt", "r") as file:
            template = file.read()
    except FileNotFoundError:
        return "Error: email_template_prompt.txt not found."

    try:
        loader = WebBaseLoader(company_url)
        website_info = loader.load()
        cleaned_up_info = website_info[0].page_content
    except Exception as e:
        return f"Error loading website: {e}"

    try:
        prompt = PromptTemplate.from_template(template)
        chain = prompt | llm
        response = chain.invoke({
            "company_info": cleaned_up_info,
            "sender_name": "Your Name",
            "recipient_name": ""
        })
        return response.content
    except Exception as e:
        return f"Error generating email: {e}"


def main():
    init()
    company_url = input("URL: ")

    email_content = generate_email(company_url)
    print(email_content)


if __name__ == "__main__":
    main()
