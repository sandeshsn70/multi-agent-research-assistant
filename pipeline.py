from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain


def run_research_pipeline(topic: str, progress_callback=None) -> dict:
    state = {}

    def update_progress(step, message):
        print(f"\n{'=' * 50}")
        print(message)
        print("=" * 50)

        if progress_callback:
            progress_callback(step, message)

    update_progress(1, "Step 1 - Search agent is working...")

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [
            ("user", f"Find recent, reliable and detailed information about: {topic}")
        ]
    })
    state["search_results"] = search_result["messages"][-1].content

    print("\nSearch results:\n", state["search_results"])

    update_progress(2, "Step 2 - Reader agent is scraping top resources...")

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [
            (
                "user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )
        ]
    })
    state["scraped_content"] = reader_result["messages"][-1].content

    print("\nScraped content:\n", state["scraped_content"])

    update_progress(3, "Step 3 - Writer is drafting the report...")

    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\nFinal report:\n", state["report"])

    update_progress(4, "Step 4 - Critic is reviewing the report...")

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    print("\nCritic report:\n", state["feedback"])

    if progress_callback:
        progress_callback(4, "Research completed")

    return state


if __name__ == "__main__":
    topic = input("\nEnter a research topic: ")
    result = run_research_pipeline(topic)
    print("\nResearch completed successfully.")
