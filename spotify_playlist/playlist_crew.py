from playlist_agents import PlaylistAgents
from playlist_tasks import PlaylistTasks
from crewai import Crew


class PlaylistCrew:
    def __init__(self, text_info, access_token):
        self.access_token = access_token
        self.text_info = text_info

    def run(self, llm_callback=None, agent_callback=None, crew_callback=None):

        agents = PlaylistAgents(llm_callback=llm_callback)
        tasks = PlaylistTasks()

        # Custom Agents definition
        expert_text_analyzer = agents.expert_analyzing_text(
            agent_callback=agent_callback
        )
        expert_music_curator = agents.expert_music_curator(
            agent_callback=agent_callback
        )
        spotify_api_expert = agents.spotify_api_expert()

        # Custom Tasks definition
        find_user_needs = tasks.extract_info_from_text(
            expert_text_analyzer,
            self.text_info,
        )

        find_songs = tasks.search_for_songs(expert_music_curator)
        search_spotify_uri_songs = tasks.search_spotify_uri_songs(spotify_api_expert)
        create_spotify_playlist = tasks.create_spotify_playlist(
            spotify_api_expert,
            self.access_token,
        )

        # My Crew
        crew = Crew(
            agents=[
                expert_text_analyzer,
                expert_music_curator,
                spotify_api_expert,
            ],
            tasks=[
                find_user_needs,
                find_songs,
                search_spotify_uri_songs,
                create_spotify_playlist,
            ],
            verbose=True,
            step_callback=crew_callback if crew_callback is not None else None,
        )

        result = crew.kickoff()
        return result
