"""
Dropship product research agent.
Uses Claude with web search to find and evaluate promising dropship products.
"""

import anthropic

client = anthropic.Anthropic()


def research_dropship_products(query: str = "best dropshipping products 2024 high margin low competition") -> None:
    print(f"\nResearching: {query}\n{'='*60}\n")

    with client.messages.stream(
        model="claude-opus-4-7",
        max_tokens=4096,
        thinking={"type": "adaptive"},
        tools=[{"type": "web_search_20260209", "name": "web_search"}],
        system=(
            "You are a dropshipping business analyst. "
            "Research and evaluate products for dropshipping potential. "
            "For each product you identify, briefly cover: "
            "supplier availability, estimated margin, competition level, and trend direction. "
            "Present findings as a clear, actionable list."
        ),
        messages=[{"role": "user", "content": query}],
    ) as stream:
        for event in stream:
            if event.type == "content_block_delta":
                if event.delta.type == "text_delta":
                    print(event.delta.text, end="", flush=True)

    print("\n")


if __name__ == "__main__":
    research_dropship_products(
        "What are the top 5 dropshipping product niches right now with good margins? "
        "Look for products that are trending, have low competition, and can be sourced from AliExpress or similar suppliers."
    )
