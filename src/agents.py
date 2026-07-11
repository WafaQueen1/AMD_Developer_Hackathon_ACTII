import asyncio
import requests
from crewai import Agent, Task, Crew, LLM


def read_github_readme(repo_url: str) -> str:
    if not repo_url:
        return "No repository URL provided."

    normalized_url = repo_url.rstrip("/")
    try:
        for branch in ["main", "master"]:
            raw_url = normalized_url.replace("github.com", "raw.githubusercontent.com", 1) + f"/{branch}/README.md"
            response = requests.get(raw_url, timeout=15)
            if response.status_code == 200:
                return response.text[:13000]
    except Exception:
        pass

    return "Could not fetch README content."


def _build_llm(api_key: str) -> LLM:
    return LLM(
        model="fireworks_ai/accounts/fireworks/models/gpt-oss-120b",
        base_url="https://api.fireworks.ai/inference/v1",
        api_key=api_key,
        temperature=0.65,
        max_tokens=2048,
    )


def _run_single_task(api_key: str, repo_url: str, repo_description: str, readme_content: str, role: str, goal: str, backstory: str, description: str, expected_output: str) -> str:
    llm = _build_llm(api_key)
    agent = Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        llm=llm,
        verbose=True,
    )

    task = Task(
        description=(
            f"Repository URL: {repo_url}\n\n"
            f"User Description:\n{repo_description}\n\n"
            f"README:\n{readme_content}\n\n"
            f"{description}"
        ),
        expected_output=expected_output,
        agent=agent,
    )

    crew = Crew(agents=[agent], tasks=[task], verbose=True)
    result = asyncio.run(crew.kickoff_async())
    return str(result)


def run_startup_strategy(api_key: str, repo_url: str, repo_description: str) -> dict:
    readme_content = read_github_readme(repo_url)

    return {
        "summary": _run_single_task(
            api_key=api_key,
            repo_url=repo_url,
            repo_description=repo_description,
            readme_content=readme_content,
            role="GitHub Repository Analyst",
            goal="Analyze the repository and README",
            backstory="You are an expert at understanding open source projects.",
            description="Analyze and summarize: purpose, key features, target users, and unique strengths.",
            expected_output="Clear project summary",
        ),
        "marketing_posts": _run_single_task(
            api_key=api_key,
            repo_url=repo_url,
            repo_description=repo_description,
            readme_content=readme_content,
            role="Technical Marketing Copywriter",
            goal="Write engaging promotional posts",
            backstory="Expert in creating content for developers on LinkedIn, X, Reddit, and Hacker News.",
            description="Write 3 ready-to-post promotional messages (LinkedIn/X, Reddit, Hacker News) tailored to the repository and the user's description.",
            expected_output="High-quality marketing posts",
        ),
        "growth_strategy": _run_single_task(
            api_key=api_key,
            repo_url=repo_url,
            repo_description=repo_description,
            readme_content=readme_content,
            role="Open Source Growth Strategist",
            goal="Create an effective launch and growth strategy",
            backstory="Specialist in growing GitHub repositories.",
            description="Create a practical growth and launch strategy for this repository, based on the summary and README content.",
            expected_output="Actionable plan with steps and timeline.",
        ),
    }


def create_startup_crew(api_key: str, repo_url: str, repo_description: str) -> Crew:
    readme_content = read_github_readme(repo_url)
    fireworks_llm = _build_llm(api_key)

    repo_analyzer = Agent(
        role="GitHub Repository Analyst",
        goal="Analyze the repository and README",
        backstory="You are an expert at understanding open source projects.",
        llm=fireworks_llm,
        verbose=True,
    )

    marketing_writer = Agent(
        role="Technical Marketing Copywriter",
        goal="Write engaging promotional posts",
        backstory="Expert in creating content for developers on LinkedIn, X, Reddit, and Hacker News.",
        llm=fireworks_llm,
        verbose=True,
    )

    growth_expert = Agent(
        role="Open Source Growth Strategist",
        goal="Create an effective launch and growth strategy",
        backstory="Specialist in growing GitHub repositories.",
        llm=fireworks_llm,
        verbose=True,
    )

    task1 = Task(
        description=(
            f"Repository URL: {repo_url}\n\n"
            f"User Description:\n{repo_description}\n\n"
            f"README:\n{readme_content}\n\n"
            "Analyze and summarize: purpose, key features, target users, and unique strengths."
        ),
        expected_output="Clear project summary",
        agent=repo_analyzer,
    )

    task2 = Task(
        description=(
            "Write 3 ready-to-post promotional messages (LinkedIn/X, Reddit, Hacker News) "
            "tailored to the repository and the user's description."
        ),
        expected_output="High-quality marketing posts",
        agent=marketing_writer,
    )

    task3 = Task(
        description=(
            "Create a practical growth and launch strategy for this repository, based on the summary "
            "and README content."
        ),
        expected_output="Actionable plan with steps and timeline.",
        agent=growth_expert,
    )

    return Crew(
        agents=[repo_analyzer, marketing_writer, growth_expert],
        tasks=[task1, task2, task3],
        verbose=True,
    )