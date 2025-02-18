import os
import json
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

def create_market_research_crew(category: str, subcategory: str) -> Crew:
    """
    Create a CrewAI research agent and task.

    Args:
        category (str): The main category of the market research.
        subcategory (str): The subcategory of the market research.

    Returns:
        Crew: Configured CrewAI instance.
    """
    research_agent = Agent(
        name="MarketResearchAgent",
        role="Research Assistant",
        goal="Gather detailed market insights",
        backstory="AI specialist in market research"
    )

    research_task = Task(
        description=f"Research market trends for {category}/{subcategory} including trends over the last 5 years, companies performing well, \
            competition, demand, economic factors, consumer demographics such as age and income groups, \
            brands available in the market and their performance, market sentiment, and both quantitative and qualitative analysis.",
        agent=research_agent,
        expected_output="A detailed summary of market trends in plain text format."
    )

    return Crew(
        agents=[research_agent],
        tasks=[research_task],
        process=Process.sequential,
        verbose=True
    )

def run_market_research(category: str, subcategory: str):
    """
    Run the market research task and save results in the data folder.

    Args:
        category (str): The main category of the market research.
        subcategory (str): The subcategory of the market research.
    """
    # Load environment variables
    load_dotenv()

    # Ensure the OpenAI API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is not set. Please set it in the environment variables.")

    # Define the directory to save research data
    directory = f"data/{category}/{subcategory}"
    os.makedirs(directory, exist_ok=True)

    # Create and kickoff the CrewAI instance
    crew = create_market_research_crew(category, subcategory)
    results = crew.kickoff()

    # Save results in text format
    research_text_path = os.path.join(directory, "research_summary.txt")
    try:
        with open(research_text_path, "w") as file:
            file.write("Market Research Summary:\n\n")
            for result in results:
                if isinstance(result, tuple) and len(result) == 2:
                    task, result_text = result
                    if task == "raw" and result_text:  # Filter for relevant task "raw"
                        file.write(f"{result_text}\n\n")
                else:
                    continue  # Skip irrelevant results
        print(f"Market research data saved in: {research_text_path}")
    except Exception as e:
        print(f"Error saving results to text file: {e}")

if __name__ == "__main__":
    # Example usage
    category = input("Enter the category (e.g., Electronics): ")
    subcategory = input("Enter the subcategory (e.g., Tablets): ")

    try:
        run_market_research(category, subcategory)
    except Exception as e:
        print(f"Error running market research: {e}")