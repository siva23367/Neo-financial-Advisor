import requests
from config.config import load_config
import json

def web_search(query, num_results=3):
    config = load_config()
    api_key = config.get("serper_api_key")
    
    if not api_key:
        return "Web search is not configured properly."
    
    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": query})
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        results = response.json()
        
        # Extract organic search results
        search_results = []
        if 'organic' in results:
            for result in results['organic'][:num_results]:
                search_results.append(f"{result['title']}: {result['snippet']}")
        
        return "\n".join(search_results) if search_results else "No relevant web results found."
    
    except Exception as e:
        return f"Error performing web search: {str(e)}"