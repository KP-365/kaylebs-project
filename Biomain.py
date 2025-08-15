import os
from crewai import Agent, Task, Crew
from apify_client import ApifyClient

# Set environment variables directly
os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"


def search_biomedical_research(query: str) -> str:
    """Search for biomedical research using Apify"""
    client = ApifyClient("YOUR_APIFY_API_KEY")

    if not query.strip():
        return "Error: No search keyword provided"

    run_input = {
        "keyword": query.strip(),
        "maxitems": 10,
        "sort_by": "Best match",
    }

    try:
        print(f"🔍 Searching for: {query}")
        run = client.actor("I55A4lAMNxZwfySX4").call(run_input=run_input)

        if not run or "defaultDatasetId" not in run:
            return "Error: Invalid response from Apify"

    except Exception as e:
        return f"Apify error: {str(e)}"

    results = []
    try:
        count = 0
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            if count >= 10:  # Limit results
                break

            title = item.get('title', 'No title available')
            url = item.get('url', 'No URL available')
            abstract = item.get('abstract', item.get('description', ''))

            result_text = f"Title: {title}\nURL: {url}"
            if abstract:
                abstract_preview = abstract[:150] + "..." if len(abstract) > 150 else abstract
                result_text += f"\nSummary: {abstract_preview}"

            results.append(result_text)
            count += 1

    except Exception as e:
        return f"Error processing results: {str(e)}"

    if not results:
        return f"No results found for '{query}'"

    return f"Found {len(results)} research papers on '{query}':\n\n" + "\n\n" + ("-" * 50) + "\n\n".join(results)


def main():
    """Main execution function"""
    try:
        print("🏥 Biomedical Research Agent Starting...")
        print("=" * 50)

        # Get research topic from user
        research_topic = input("What biomedical topic should I research? ").strip()

        if not research_topic:
            print("No research topic provided. Exiting...")
            return

        # Do the research first
        print(f"\n🔍 Searching for research on: {research_topic}")
        research_data = search_biomedical_research(research_topic)

        print("\n" + "=" * 50)
        print("📊 RESEARCH RESULTS")
        print("=" * 50)
        print(research_data)

        # Create research agent (no tools needed)
        research_agent = Agent(
            role="Biomedical Research Analyst",
            goal=f"Analyze the biomedical research data provided about {research_topic}",
            backstory=(
                "You are a highly skilled biomedical research analyst with expertise in "
                "evaluating scientific literature, clinical studies, and medical research. "
                "You excel at synthesizing complex medical information and identifying "
                "key trends, methodologies, and clinical implications."
            ),
            verbose=True
        )

        # Create analysis task with the research data
        analysis_task = Task(
            description=(
                f"Analyze the following biomedical research data about '{research_topic}':\n\n"
                f"{research_data}\n\n"
                "Based on this research data, provide a comprehensive analysis that includes:\n"
                "1. Summary of the key findings and research themes\n"
                "2. Analysis of the types of studies and methodologies mentioned\n"
                "3. Clinical significance and potential real-world applications\n"
                "4. Current trends in this research area\n"
                "5. Assessment of the research scope and quality\n"
                "6. Recommendations for patients, clinicians, or future research"
            ),
            agent=research_agent,
            expected_output=(
                "A detailed research analysis report containing:\n"
                "- Executive summary of key findings\n"
                "- Analysis of research methodologies and study types\n"
                "- Clinical implications and practical applications\n"
                "- Current trends and future directions\n"
                "- Quality assessment and recommendations"
            )
        )

        # Create and run crew
        crew = Crew(
            agents=[research_agent],
            tasks=[analysis_task],
            verbose=True
        )

        print(f"\n🧠 Starting analysis of {research_topic} research...")
        print("=" * 60)

        result = crew.kickoff()

        print("\n" + "=" * 60)
        print("🎯 RESEARCH ANALYSIS COMPLETED")
        print("=" * 60)
        print(result)

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()