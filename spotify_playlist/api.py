from fastapi import FastAPI, Request, HTTPException, Response, BackgroundTasks
from fastapi.responses import RedirectResponse
import requests
from urllib.parse import urlencode
import os
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from playlist_crew import PlaylistCrew
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8000/callback"
SCOPES = "playlist-modify-private playlist-modify-public user-modify-playback-state user-read-playback-state"

# Mount the static directory to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/login")
def read_root():
    auth_url = f"https://accounts.spotify.com/authorize?response_type=code&client_id={CLIENT_ID}&scope={SCOPES}&redirect_uri={REDIRECT_URI}"
    return RedirectResponse(url=auth_url)


@app.get("/callback")
def callback(code: str, request: Request, response: Response) -> RedirectResponse:
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }

    token_response = requests.post(token_url, data=payload)
    if token_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Error retrieving access token")

    token_data = token_response.json()
    access_token = token_data["access_token"]
    refresh_token = token_data["refresh_token"]

    # set the response to redirect to the frontend
    response = RedirectResponse(url="http://localhost:8000/static/index.html?#showForm")

    # JUST FOR TESTING PORPUSES
    # not super secure
    # Set the refresh token in cookie
    response.set_cookie(
        path="/",
        domain="localhost",
        key="accessToken",
        value=access_token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="Lax",
    )

    return response


from langchain_core.callbacks import BaseCallbackHandler


class MyCustomHandler(BaseCallbackHandler):
    from typing import Any, Dict
    from langchain_core.agents import AgentFinish

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> Any:
        """Run on agent end."""
        print(f"Agent finished: {finish.return_values["output"]}")
        return None


def run_playlist_crew(
    text_info: str,
    autoplay_device: str,
    access_token: str,
):
    # Simulating a long-running task
    playlist_crew = PlaylistCrew(
        text_info=text_info,
        access_token=access_token,
        autoplay_device=autoplay_device,
    )

    result = playlist_crew.run(callbacks=[MyCustomHandler()])
    print(result)


class Submission(BaseModel):
    text_info: str
    autoplay_device: str


@app.post("/submit-api")
async def handle_long_process(
    request: Request, background_tasks: BackgroundTasks, submission: Submission
):
    import uuid

    text_info = submission.text_info
    autoplay_device = submission.autoplay_device

    # Extract the access token from the cookies
    access_token = request.cookies.get("accessToken")
    if not access_token:
        return {"error": "Refresh token not found"}

    task_id = str(uuid.uuid4())  # Generate a unique task ID
    background_tasks.add_task(run_playlist_crew, text_info, autoplay_device, access_token)
    return {"message": "Task started, processing in the background", "task_id": task_id}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
