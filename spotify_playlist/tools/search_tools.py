import requests, os
import json
from langchain.tools import tool


class SearchTools:

    @tool("Search the internet")
    def search_internet(query):
        """Userful to search on internet about a given topic and return relevant results"""

        print("Searching the internet...", query)
        top_result_to_return = 4
        url = f"https://google.serper.dev/search"

        payload = json.dumps({"q": query})
        headers = {
            "X-API-KEY": os.environ["SERPER_API_KEY"],
            "Content-Type": "application/json",
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        if "organic" not in response.json():
            return "No results found"
        else:
            results = response.json()["organic"]
            string = []
            for result in results[:top_result_to_return]:
                try:
                    string.append(
                        "\n".join(
                            [
                                f"Title: {result['title']}",
                                f"Link: {result['link']}",
                                f"Snippet: {result['snippet']}",
                            ]
                        )
                    )
                except KeyError:
                    next

            return "\n".join(string)


if __name__ == "__main__":
    print(SearchTools.search_internet("How to make a cake"))
