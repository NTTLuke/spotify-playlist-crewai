from crewai import Task
from textwrap import dedent
from tools.spotify_tools import SpotifyTools


class PlaylistTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"

    def extract_info_from_text(self, agent, text_info):
        return Task(
            description=dedent(
                f"""
                **Task**: Analyze text to pick the right information for searching appropriated songs for the user.
                **Description**: Your objective is to analyze the text provided by the user to extract key information necessary for producing a tailored playlist. 
                This information will be utilized to identify the user's specific requirements regarding the songs they desire. 
                When extracting this information, it's crucial to focus on important details such as: 
                - the preferred music genre
                - the desired mood or emotions the user wants to evoke
                - the current activity or situation they're engaged in
                - any other relevant factors that could influence their song preferences. 
                
                By carefully considering these details, we can create a playlist that perfectly matches the user's needs and preferences.

                The result MUST be a query for serpapi endpoint.

                **Parameters**:
                - text_info : {text_info}
                
                **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            expected_output="a string with the query for serpapi endpoint",
        )

    def search_for_songs(self, agent):
        return Task(
            description=dedent(
                f"""
                **Task**: Curate a selection of 10 songs based on user needs, reflecting current music trends.
                **Description**: Your objective is to curate a playlist of 10 songs tailored to meet specific user preferences or needs. 
                Each song should be carefully chosen to suit its designated situation, ensuring diversity and relevance. 
                It's essential to select songs that are distinct from one another and align with prevalent tastes in today's music scene as of February 2024. 
                If you find a playlist, you need to get the songs contained in it, not the playlist name. Don't search on youtube.com 
                Additionally, ensure that your playlist does not contain any duplicate songs, offering a unique listening experience throughout.

                **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            expected_output="a list of strings",
        )

    def search_spotify_uri_songs(self, agent):
        return Task(
            description=dedent(
                f"""
                **Task**:Search for songs uris on Spotify
                **Description**: Search for the uri of the songs on spotify and return list of uris related each song. The uris are the unique identifiers of each song on spotify.
                
                **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            expected_output="a list of strings with the uris of the songs",
        )

    def create_spotify_playlist(self, agent, access_token):
        return Task(
            description=dedent(
                f"""
                **Task**:Create Spotify playlist using uris and access token
                **Description**: Create a new playlist on Spotify using the uris of the songs and the access_token. 
                The playlist should be named "made by NTTLuke (with CrewAI)" and should include the songs selected.
                
                **Parameters**:
                - Access Token: {access_token}

                **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            expected_output="a string with the playlist id",
        )

    def identify_the_device_type(self, agent, access_token, text_from_user):
        return Task(
            description=dedent(
                f"""
                **Task**: Identify the device to play the playlist
                **Description**: Identify the device type where the user wants to play the playlist based on the text received. 
                If no device type is specified, use computer. 
                
                Available device types are : computer, smartphone or speaker
                
                **Parameters**:
                - Access Token: {access_token}
                - Text from User: {text_from_user}

                **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            tools=[
                SpotifyTools.retrieve_device_type_id,
            ],
            expected_output="The device type id where the playlist will be played.",
        )

    def starting_play_playlist(self, agent, access_token):
        return Task(
            description=dedent(
                f"""
                **Task**:Start the playlist on my device
                **Description**: Play the playlist on the user's device using the Spotify API.               
                **Parameters**:
                - Access Token: {access_token}

                **Note**: {self.__tip_section()}
                """
            ),
            agent=agent,
            tools=[
                SpotifyTools.start_playing_playlist,
            ],
            expected_output="Information about the playlist playing on the user's device or an error message if the playlist could not be played.",
        )
