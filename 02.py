import json
from typing import List
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_tavily import TavilySearch
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

load_dotenv()

# model = init_chat_model(model="gpt-oss", model_provider="ollama", temperature=0)
model = init_chat_model(model="gpt-4o-mini", model_provider="openai", temperature=0)


def create_search_query(genre: str, mood: str, decade: str) -> str:
    prompt = ChatPromptTemplate(
        [
            (
                "system",
                (
                    "You are a search query generator for a movie recommendation system.\n\n"
                    "The user provides three fields:\n"
                    "- Genre: the type of movie they want (this is the ONLY genre; never invent or add genres).\n"
                    "- Mood: the user's CURRENT emotional state — NOT a movie descriptor, NOT a genre.\n"
                    "- Decade: the preferred release decade.\n\n"
                    "=== JUDGEMENT GUIDELINE ===\n"
                    "Your job is to make a judgement call: the Mood must be TRANSLATED into the "
                    "desired *quality* of movie that would best serve the user, then that quality is "
                    "combined with the Genre and Decade.\n\n"
                    "CRITICAL RULE: The raw mood word must NEVER appear in the final search query.\n"
                    "The mood is an INPUT to your reasoning, not an OUTPUT in the query.\n\n"
                    "Step 1 — Translate the mood into a target movie quality:\n"
                    "- sad       -> uplifting, feel-good\n"
                    "- stressed  -> relaxing, comforting\n"
                    "- bored     -> exciting, entertaining\n"
                    "- happy     -> fun, celebratory\n"
                    "- romantic  -> romantic, heartwarming\n"
                    "- scared    -> light-hearted, gentle\n"
                    "(If the mood is not listed, judge the best-fitting quality yourself.)\n\n"
                    "Step 2 — Combine: <translated_quality> + <genre> + movies + <decade>\n\n"
                    "Step 3 — Self-check before answering:\n"
                    "  a. Does my query contain the literal mood word (e.g. 'sad')? "
                    "If YES, remove it and use the translated quality instead.\n"
                    "  b. Did I keep the user's genre unchanged? It must not be replaced or dropped.\n"
                    "  c. Is the query recommending movies that HELP the user's state, "
                    "not movies that MATCH their negative state?\n\n"
                    "=== EXAMPLES ===\n"
                    "Genre: comedy | Mood: sad | Decade: 2020s\n"
                    "  WRONG: 'sad comedy movies 2020s'  (leaks the mood word)\n"
                    "  RIGHT: 'uplifting feel-good comedy movies 2020s'\n\n"
                    "Genre: thriller | Mood: stressed | Decade: 1990s\n"
                    "  WRONG: 'stressful thriller movies 1990s'\n"
                    "  RIGHT: 'comforting relaxing thriller movies 1990s'\n\n"
                    "Genre: action | Mood: bored | Decade: 2010s\n"
                    "  RIGHT: 'exciting entertaining action movies 2010s'\n\n"
                    "Return ONLY the final search query. No explanation, no reasoning, no quotes."
                ),
            ),
            (
                "human",
                (
                    "Create a search query based on the following fields:\n"
                    "- Genre: {genre}\n"
                    "- Mood: {mood}\n"
                    "- Decade: {decade}\n"
                ),
            ),
        ]
    )

    chain = prompt | model | StrOutputParser()

    print("Generating search query...")
    response = chain.invoke({"genre": genre, "mood": mood, "decade": decade})
    return response


class Movie(BaseModel):
    title: str = Field(description="Title of the movie")
    release_year: str = Field(description="Which year the movie is released")
    short_reason: str = Field(description="Why this movie is recommended")
    content_warning: str = Field(
        description="Content warning for this recommended movie"
    )


class Movies(BaseModel):
    movies: List[Movie] = Field(
        description="List of 3 movies", min_length=3, max_length=3
    )


search_tool = TavilySearch(
    max_results=3,
    topic="general",
    search_depth="advanced",
)


def recommend_movie_agent(query: str) -> Movies:
    tools = [search_tool]
    agent = create_agent(
        model=model,
        tools=tools,
        response_format=ToolStrategy(Movies),
        system_prompt=(
            "You are a movie recommendation engine that uses Tavily search to produce "
            "accurate and relevant recommendations.\n\n"
            "Given the user's query, search the web and return exactly 3 movies that best "
            "match their preferences.\n\n"
            "For each recommendation:\n"
            "- Confirm the movie title and release year.\n"
            "- Explain briefly why it matches the user's request.\n"
            "- Include a concise and factual content warning. Use 'None known' only when "
            "no meaningful warning is identified from reliable information.\n\n"
            "Interpret the user's mood carefully. By default, mood describes how the user "
            "currently feels, so recommend movies suitable for that emotional state rather "
            "than treating the mood as a required movie characteristic.\n\n"
            "Use search results as supporting information, but do not mention the search "
            "process in the final response. Return only a valid `Movies` object containing "
            "exactly 3 unique recommendations."
        ),
    )

    response = agent.invoke(
        {"messages": [{"role": "user", "content": f"Query: {query}"}]}
    )

    return response["structured_response"]


# Take user's input
while True:
    print("Welcome to move recommender")
    print("Answer the folling questions:")
    genre = input("Genre: ")
    if len(genre.strip()) == 0:
        raise Exception("Genre is required")

    mood = input("Mood: ")
    if len(mood.strip()) == 0:
        raise Exception("Mood is required")

    decade = input("Decade: ")
    if len(decade.strip()) == 0:
        raise Exception("Decade is required")

    # Create a search query
    search_query = create_search_query(genre, mood, decade)
    movies = recommend_movie_agent(search_query)
    print(json.dumps(movies.model_dump(), indent=2))
    break
