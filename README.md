# Market-Research

This project is a work in progress and requires several changes. Currently it has the following:

1) app.py: Fast API which will take inputs the following-
      objective: str
      category: str
      subcategory: str
      age: str
      income: str
      location: str
      num_questions: int

The category and subcategory can be the following;
        "Electronics": ["Tablets", "Laptops", "Smartwatches"],
        "Fitness": ["Fitness Trackers", "Gym Equipment"],
        "Appliances": ["Refrigerators", "Microwaves"],
        "Luxury Fashion": ["Apparel","shoes"]


2) crewai_script.py: CrewAI agent which will take category and subcategory as inputs and generate questions based on the following criteria-
       - Trends over the last 5 years
       - companies performing well
       - Competition
       - Demand
       - Economic factors
       - Consumer demographics such as age and income groups
       - Brands available in the market and their performance, market sentiment, and both quantitative and qualitative analysis.
   Currently there is only one research agent - MarketResearchAgent which plays the role of Research Assistant and gathers detailed market insights.
   Result would be saved in a text file - research_summary.txt

   3) question_generator.py:
       This module is responsible for generating questions

   We can run this code by: uvicorn app: app --reload.

   We can then go to http://localhost:8000/

   In this we will get the following:
   {"message":"Welcome to Market Research API","endpoints":{"Generate Questions":"/research","View Categories":"/categories","Documentation":"/docs"}}

   We can then go to http://localhost:8000/docs. then we can go to POST -> Try it out -> Add inputs -> Execute
