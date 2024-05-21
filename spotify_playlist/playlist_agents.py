from crewai import Agent
from textwrap import dedent
from langchain_openai.chat_models.azure import AzureChatOpenAI
from tools.search_tools import SearchTools
from tools.spotify_tools import SpotifyTools
import os


class PlaylistAgents:
    def __init__(self, llm_callback=None):
        self.AzureChatOpenAI = AzureChatOpenAI(
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            temperature=0.7,
            streaming=True,
        )
        if llm_callback:
            self.AzureChatOpenAI.callbacks = [llm_callback]
        # self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        # self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4", temperature=0.7)
        # self.Ollama = Ollama(model="phi", num_gpu=1)

    def expert_analyzing_text(self, agent_callback=None, callbacks=None):
        return Agent(
            role="Expert Text Analyzer for music selection",
            backstory=dedent(
                f"""I'm am an expert in analyzing textual information to accurately select music. 
                    With decades of experience, I specialize in interpreting a wide range of textual data to identify 10 (TEN) songs that best match the provided context.
                    I have decades of experience in understanding songs based text info.
                """
            ),
            goal=dedent(
                f"""My primary objective is to accurately identify and recommend songs based on the text provided. 
                    I leverage my extensive experience and deep understanding of music-related text analysis to deliver relevant and tailored song selections that meet the user's needs and preferences."""
            ),
            allow_delegation=False,
            verbose=True,
            llm=self.AzureChatOpenAI,
            step_callback=agent_callback if agent_callback is not None else None,
            callbacks=callbacks,
        )

    # select songs on internet
    def expert_music_curator(self, agent_callback=None, callbacks=None):
        return Agent(
            role="Expert Music Curator",
            backstory=dedent(
                f"""Expert at analyzing music data to pick ideal songs for a playlist considering the information provided by user. I have decades of experience understanding music trends."""
            ),
            goal=dedent(
                f"""Search for 10 SONGS ONLY based on the user needs. 
                    Take care about current music trends.
                    Provide a search query to find the songs on the internet specific for the user needs.
                """
            ),
            max_iter=4,
            tools=[SearchTools.search_internet],
            allow_delegation=False,
            verbose=True,
            llm=self.AzureChatOpenAI,
            step_callback=agent_callback if agent_callback is not None else None,
            callbacks=callbacks,
        )

    def spotify_api_expert(self):
        return Agent(
            role="Spotify API Expert",
            backstory=dedent(
                f"""Expert to work with Spotify API. 
                    I have experience in searching music on Spotify finding uri of the songs and 
                    a year of experience to create playlist."""
            ),
            goal=dedent(
                f"""Find Uri of the songs on Spotify.
                    Create a playlist using uri.
                    Start playing the playlist on the specific device of the user."""
            ),
            tools=[
                SpotifyTools.search_songs_uris,
                SpotifyTools.create_playlist_by_uris,
            ],
            allow_delegation=False,
            verbose=True,
            llm=self.AzureChatOpenAI,
        )

    def spotify_dj_expert(self):
        return Agent(
            role="Spotify DJ Expert",
            backstory=dedent(
                f"""I'm an expert DJ on Spotify. I have experience to play a playlist already created on Spotify and start playing on the specific device of the user."""
            ),
            goal=dedent(
                f"""Start playing the playlist that already exists on the user's device."""
            ),
            tools=[
                SpotifyTools.start_playing_playlist,
            ],
            allow_delegation=False,
            verbose=True,
            llm=self.AzureChatOpenAI,
        )
