# LEGACY

# import os
# from textwrap import dedent
# from dotenv import load_dotenv

# from playlist_crew import PlaylistCrew
# from langchain_core.callbacks import BaseCallbackHandler, StdOutCallbackHandler
# from typing import Any, Dict
# from langchain_core.agents import AgentAction, AgentFinish


# load_dotenv()


# class MyCustomHandler(BaseCallbackHandler):
#     def on_llm_new_token(self, token: str, **kwargs) -> None:
#         print(f"My custom handler, token: {token}")

#     def on_chain_start(
#         self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
#     ) -> Any:
#         print(f"on_chain_start {serialized['name']}")

#     def on_tool_start(
#         self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
#     ) -> Any:
#         print(f"on_tool_start {serialized['name']}, input_str: {input_str}")

#     def on_tool_end(self, output: str, **kwargs: Any) -> Any:
#         """Run when tool ends running."""
#         print(f"on_tool_end {output}")

#     def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
#         print(f"on_agent_action {action}")

#     def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> Any:
#         """Run on agent end."""
#         print(f"on_agent_finish {finish}")


# handler = StdOutCallbackHandler()


# def agent_callback(agent_info: Any):
#     import json

#     print("******* Agent callback ******* ")
#     print(agent_info)
#     print("******* End Agent callback ******* ")


# def crew_callback(crew_info: Any):
#     print("******* Crew callback ******* ")
#     print(crew_info)
#     print("******* End Crew callback ******* ")


# def music_playlist_main():
#     print("## Welcome to Music Playlist! ##")
#     print("-------------------------------")

#     genre = input(dedent("""What is your favorite music genre?"""))
#     mood = input(dedent("""What is your current mood?"""))
#     activity = input(dedent("""What are you doing?"""))
#     access_token = "BLEAH!"

#     playlist_crew = PlaylistCrew(mood, genre, activity, access_token)

#     result = playlist_crew.run(
#         # llm_callback=MyCustomHandler(),
#         agent_callback=agent_callback,
#         crew_callback=crew_callback,
#     )

#     print("\n\n########################")
#     print("## Here is you custom crew run result:")
#     print("########################\n")
#     print(result)


# # This is the main function that you will use to run your custom crew.
# if __name__ == "__main__":
#     music_playlist_main()

#     # x = """return_values={'output': 'Based on my search, I was unable to find a specific list of popular rock songs in February 2024.
#     #        However, as an expert music curator, I can still provide you with a selection of 10 songs in the rock genre that reflect current music trends.
#     #        Please find below my curated playlist for working with a rock mood:\n\n1. "Don\'t Stop Believin\'" by Journey\n2.
#     #        "Smells Like Teen Spirit" by Nirvana\n3. "Livin\' on a Prayer" by Bon Jovi\n4. "Sweet Child o\' Mine" by Guns N\' Roses\n5. "Hotel California" by Eagles\n6.
#     #        "Bohemian Rhapsody" by Queen\n7. "Back in Black" by AC/DC\n8. "Wonderwall" by Oasis\n9. "Mr. Brightside" by The Killers\n10. "Sweet Home Alabama" by Lynyrd Skynyrd\n\n
#     #        These songs represent a mix of classic rock hits and more recent rock anthems that are still popular today.
#     #        Enjoy your work playlist!'} log='Final Answer: \nBased on my search, I was unable to find a specific list of popular rock songs in February 2024.
#     #        However, as an expert music curator, I can still provide you with a selection of 10 songs in the rock genre that reflect current music trends.
#     #        Please find below my curated playlist for working with a rock mood:\n\n1. "Don\'t Stop Believin\'" by Journey\n2. "Smells Like Teen Spirit" by Nirvana\n3. "Livin\' on a Prayer" by Bon Jovi\n4.
#     #        "Sweet Child o\' Mine" by Guns N\' Roses\n5. "Hotel California" by Eagles\n6. "Bohemian Rhapsody" by Queen\n7. "Back in Black" by AC/DC\n8. "Wonderwall" by Oasis\n9. "Mr. Brightside" by The Killers\n10.
#     #        "Sweet Home Alabama" by Lynyrd Skynyrd\n\nThese songs represent a mix of classic rock hits and more recent rock anthems that are still popular today. Enjoy your work playlist!'"""

#     # agent_callback(x)
