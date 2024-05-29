from playlist_agents import PlaylistAgents
from playlist_tasks import PlaylistTasks
from crewai import Crew


class PlaylistCrew:
    def __init__(self, text_info, model_name, autoplay_device, access_token):
        self.access_token = access_token
        self.autoplay_device = autoplay_device
        self.model_name = model_name
        self.text_info = text_info

    def run(
        self, llm_callback=None, agent_callback=None, crew_callback=None, callbacks=None
    ):

        agents = PlaylistAgents(model_name=self.model_name, llm_callback=llm_callback)
        tasks = PlaylistTasks()

        # Agents definition
        expert_text_analyzer = agents.expert_analyzing_text(callbacks=callbacks)
        expert_music_curator = agents.expert_music_curator(callbacks=callbacks)
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

        # optional agents and tasks
        spotify_dj_expert = agents.spotify_dj_expert()
        play_playlist = tasks.starting_play_playlist(
            agent=spotify_dj_expert,
            task_context=create_spotify_playlist,
            access_token=self.access_token,
            autoplay_device=self.autoplay_device,
        )

        # default agents
        all_agents = [
            expert_text_analyzer,
            expert_music_curator,
            spotify_api_expert,
        ]

        if self.autoplay_device != "none":
            all_agents.append(spotify_dj_expert)

        # default tasks
        all_tasks = [
            find_user_needs,
            find_songs,
            search_spotify_uri_songs,
            create_spotify_playlist,
        ]

        if self.autoplay_device != "none":
            all_tasks.append(play_playlist)

        # My Crew
        crew = Crew(
            agents=all_agents,
            tasks=all_tasks,
            verbose=True,
            step_callback=crew_callback if crew_callback is not None else None,
        )

        result = crew.kickoff()
        return result
