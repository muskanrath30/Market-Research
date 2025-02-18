from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain_openai.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import os
from typing import List, Dict

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("The OpenAI API key is missing. Please set OPENAI_API_KEY in your environment or .env file.")

def generate_questions(category: str, subcategory: str, context: str, num_questions: int = 10) -> List[str]:
    """Generate survey questions based on market research and user context."""
    try:
        # Load research data
        directory = f"data/{category}/{subcategory}"
        research_data = load_research_data(directory)
        
        # Create combined context
        full_context = create_market_context(research_data, context)
        
        # Initialize ChatOpenAI
        llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            openai_api_key=OPENAI_API_KEY,
            temperature=0.7
        )

        # Create a more detailed prompt template
        prompt_template = ChatPromptTemplate.from_template("""
You are a market research expert. Based on the provided research data and context, 
generate {num_questions} insightful survey questions that will help understand customer needs 
and preferences for {subcategory} in the {category} category.

Guidelines for questions:
- Mix of quantitative and qualitative questions
- Include questions about:
  * Purchase intent
  * Product features preferences
  * Price sensitivity
  * Brand awareness
  * Usage patterns
  * Pain points
  * Customer satisfaction
  * Competitive comparison
  * Future needs
  * Demographics validation
- Consider the demographic context: {context}
- Make questions specific to the product category
- Avoid leading or biased questions
- Each question should be clear and focused

Generate exactly {num_questions} questions, numbered 1-{num_questions}.

Context:
{full_context}
""")

        # Create and run the chain
        chain = LLMChain(llm=llm, prompt=prompt_template)
        
        response = chain.run({
            "category": category,
            "subcategory": subcategory,
            "context": context,
            "full_context": full_context,
            "num_questions": num_questions
        })

        # Process the response
        questions = [
            q.strip() for q in response.split("\n")
            if q.strip() and any(q.startswith(str(i)) for i in range(1, num_questions + 1))
        ]

        # Validate output
        if len(questions) != num_questions:
            raise ValueError(f"Failed to generate exactly {num_questions} questions")

        # Remove numbering from questions
        questions = [q.split(". ", 1)[1] if ". " in q else q for q in questions]

        return questions

    except Exception as e:
        raise Exception(f"Failed to generate questions: {str(e)}")

def validate_questions(questions: List[str], expected_count: int = 10) -> Dict[str, bool]:
    """Validate the generated questions for quality."""
    return {
        "correct_count": len(questions) == expected_count,
        "non_empty": all(len(q.strip()) > 0 for q in questions),
        "unique": len(set(questions)) == len(questions),
        "proper_length": all(10 <= len(q) <= 200 for q in questions)
    }

def load_research_data(directory: str) -> str:
    """Load and combine research data from text files."""
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    loader = DirectoryLoader(directory, glob="*.txt")
    docs = loader.load()
    
    if not docs:
        raise ValueError(f"No documents found in {directory}")
    
    # Combine all documents into one text
    return "\n".join(doc.page_content for doc in docs)

def create_market_context(research_data: str, user_context: str) -> str:
    """Combine research data with user context."""
    return f"""
Research Data:
{research_data}

User Context:
{user_context}
"""