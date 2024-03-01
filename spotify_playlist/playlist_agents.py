from crewai import Agent
from textwrap import dedent

from langchain.llms.ollama import Ollama
from langchain_openai import AzureChatOpenAI
from tools.search_tools import SearchTools
from tools.spotify_tools import SpotifyTools


# **********
# I found this in anonline , it is very useful to understand how to create a crew of agents to accomplish a goal.
# **********
# Creating Agents Cheat Sheet:
# - Think like a boss. Work backwards from the goal and think about what kind of person you need to get the job done.
# - Define a Captain of the crew who orient the other agents towards the goal.
# - Define which experts the captain needs to communicate with and delegate tasks to.
#   Build on top down structure of the crew.

#   GOAL:
#     - Let's write the goal of the crew here.

#   Captain/Manager/Boss
#    - Role: The person who is responsible for the overall goal of the crew.

#   Empleyees/Experts to hire:
#   - who are the experts that the captain needs to communicate with and delegate tasks to.

#   Notes:
#     -Agents should be results driven and have a clear goal in mind.
#     -Role is their job title.
#     -Goals should be actionable.
#     -Backstory should be their resume.


class PlaylistAgents:
    def __init__(self, llm_callback=None):
        self.AzureChatOpenAI = AzureChatOpenAI(
            deployment_name="chat",
            temperature=0.7,
            streaming=True,
        )
        if llm_callback:
            self.AzureChatOpenAI.callbacks = [llm_callback]
        # self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        # self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.7)
        # self.Ollama = Ollama(model="phi", num_gpu=1)

    def expert_analyzing_text(self, agent_callback=None):
        return Agent(
            role="Expert Text Analyzer for music selection",
            backstory=dedent(
                f"""Expert at analyzing text to pick the right information for searching appropriated songs. I have decades of experience understanding songs needed by text info."""
            ),
            goal=dedent(f"""Identify the person music needs based on a text."""),
            allow_delegation=False,
            verbose=True,
            llm=self.AzureChatOpenAI,
            step_callback=agent_callback if agent_callback is not None else None,
        )

    # select songs on internet
    def expert_music_curator(self, agent_callback=None):
        return Agent(
            role="Expert Music Curator",
            backstory=dedent(
                f"""Expert at analyzing music data to pick ideal songs for a playlist considering the information provided by user. I have decades of experience understanding music trends."""
            ),
            goal=dedent(
                f"""Search for 10 songs based on the user needs. 
                    Take care about current music trends.
                    Provide a search query to find the songs on the internet specific for the user needs.
                """
            ),
            tools=[SearchTools.search_internet],
            allow_delegation=False,
            verbose=True,
            llm=self.AzureChatOpenAI,
            step_callback=agent_callback if agent_callback is not None else None,
        )

    # select songs on spotify
    def spotify_song_finder(self):
        return Agent(
            role="Spotify Song Finder",
            backstory=dedent(
                f"""Expert to search music on spotify database. I have experience in searching music on spotify finding uri."""
            ),
            goal=dedent(f"""Search song uri on spotify database"""),
            tools=[SpotifyTools.search_songs_uris],
            allow_delegation=False,
            verbose=True,
            llm=self.AzureChatOpenAI,
        )

    # create playlist on spotify
    def spotify_playlist_creator(self):
        return Agent(
            role="Spotify Playlist Creator",
            backstory=dedent(
                f"""I have experience creating playlist in Spotify using the uris of the songs."""
            ),
            goal=dedent(
                f"""Create a spotify playlist with the selected songs and save it for the user."""
            ),
            tools=[SpotifyTools.create_playlist_by_uris],
            allow_delegation=False,
            verbose=True,
            llm=self.AzureChatOpenAI,
        )
