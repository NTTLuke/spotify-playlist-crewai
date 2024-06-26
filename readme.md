## Spotify Playlist with CrewAI

Learning by doing project to generate Spotify playlists using [CrewAi](https://github.com/joaomdmoura/crewAI).

(🥸 _Improvements WIP_ 🥸)

### Description

Sharing personal insights, including preferences and specific thoughts, aspects like your preferred music genre, current emotional state, activities you are engaged in, or particular needs you aim to satisfy.
Agents will leverage this detailed information to craft a customized playlist with 10 songs.

### Example of prompts

"Create a playlist with Eurovision 2024 songs", "I need a rock mood for the day", "To the EDM moon" ...

### Demo

[<video/>](https://github.com/NTTLuke/spotify-playlist-crewai/assets/1864745/2e4b9e2b-9c3e-4b7b-acef-fb162c1df4c7)

### Installation

1. Clone the repository: `git clone https://github.com/NTTLuke/spotify-playlist-crewai.git`
2. Install Poetry if you haven't already. You can follow the installation instructions on the Poetry website: [Poetry Installation Guide](https://python-poetry.org/docs/#installation).
3. Install the required dependencies using Poetry:
   ```bash
   poetry install
   ```
4. Set up your environment variables by creating a `.env` file based on the provided `.env_example` file and adding your specific values:

   ```plaintext
   # azure openai api key and endpoint
   AZURE_OPENAI_API_KEY = "your-azure-openai-api-key"
   AZURE_OPENAI_ENDPOINT = "your-azure-openai-endpoint"
   OPENAI_API_TYPE = "azure"
   OPENAI_API_VERSION = "your-azure-openai-api-version"
   AZURE_OPENAI_DEPLOYMENT_NAME="your-azure-openai-deployment-name"

   # openai api key
   OPENAI_API_KEY = "your-openai-key"

   # uncomment the following lines to use langsmith
   # LANGCHAIN_TRACING_V2=true
   # LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
   # LANGCHAIN_API_KEY=your-langchain-api-key
   # LANGCHAIN_PROJECT=your-langchain-project

   SERPER_API_KEY = "your-serper-api-key"

   # see https://developer.spotify.com/documentation/general/guides/app-settings/
   SPOTIFY_CLIENT_ID = "your-spotify-client-id"
   SPOTIFY_CLIENT_SECRET = "your-spotify-client-secret"


   ```

   Ensure you have registered your application with Spotify and obtained your client ID and client secret. Use http://localhost:8000/callback as Redirect URI. Refer to the [Spotify Developer Documentation](https://developer.spotify.com/documentation/general/guides/app-settings/) for instructions on how to create and configure your Spotify application. Additionally, you need to acquire your SerpApi key. Please refer to the [SerpApi Documentation](https://serpapi.com/) for more information on obtaining your API key.

### Usage

Start FastAPI and run the Spotify Playlist with CrewAI application, follow these steps:

Run

```bash
poetry shell
```

then

```bash
uvicorn --app-dir=spotify_playlist api:app --reload
```

Test the application using the starting page provided at

```
http://localhost:8000/static/index.html
```

### Caveats for Autoplay Feature

To use the new autoplay feature, you need to open the Spotify player on the selected device.

**Note:** Occasionally, the player may not immediately receive the play signal. In such cases, simply click on the playlist (without starting it) to trigger autoplay.
