## Spotify Playlist with CrewAI

### Description

Learning by doing project to generate Spotify playlists using CrewAI.

[Link to GitHub Repository](https://github.com/joaomdmoura/crewAI)

<video src="./assets/demo-spoty-crewai.mp4" width="640" height="360" controls></video>

### Installation

1. Clone the repository: `git clone https://github.com/NTTLuke/spotify-playlist-crewai.git`
2. Install Poetry if you haven't already. You can follow the installation instructions on the Poetry website: [Poetry Installation Guide](https://python-poetry.org/docs/#installation).
3. Install the required dependencies using Poetry:
   ```bash
   poetry install
   ```
4. Set up your environment variables by creating a `.env` file based on the provided `.env_example` file and adding your specific values:

   ```plaintext
   AZURE_OPENAI_API_KEY = "your-azure-openai-api-key"
   AZURE_OPENAI_ENDPOINT = "your-azure-openai-endpoint"
   OPENAI_API_TYPE = "azure"
   OPENAI_API_VERSION = "your-azure-openai-api-version"

   # SerpApi Key
   SERPER_API_KEY = "your-serper-api-key"

   # Uncomment the following lines to use langsmith
   # LANGCHAIN_TRACING_V2=true
   # LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
   # LANGCHAIN_API_KEY=your-langchain-api-key
   # LANGCHAIN_PROJECT=your-langchain-project

   # Spotify API credentials
   SPOTIFY_CLIENT_ID = "your-spotify-client-id"
   SPOTIFY_CLIENT_SECRET = "your-spotify-client-secret"
   ```

   Ensure you have registered your application with Spotify and obtained your client ID and client secret. Refer to the [Spotify Developer Documentation](https://developer.spotify.com/documentation/general/guides/app-settings/) for instructions on how to create and configure your Spotify application. Additionally, you need to acquire your SerpApi key. Please refer to the [SerpApi Documentation](https://serpapi.com/) for more information on obtaining your API key.

### Usage

Start FastAPI and run the Spotify Playlist with CrewAI application, follow these steps:

```bash
uvicorn --app-dir=spotify_playlist api:app --reload
```

To test the application using the starting page provided at

```
http://localhost:8000/static/index.html
```

### Agents involved

> Expert Text Analyzer for music selection

- **Role**: Expert Text Analyzer for music selection

> Expert Music Curator

- **Role**: Expert Music Curator

> Spotify Song Finder

- **Role**: Spotify Song Finder

> Spotify Playlist Creator

- **Role**: Spotify Playlist Creator
