from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import motor.motor_asyncio

app = FastAPI(
    title="Multimedia API",
    description="API for uploading sprites, audio files, and player scores"
)

# Connect to MongoDB Atlas
client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb+srv://ictstudent:mcast1234@cluster0.qbuvr7z.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
db = client["Database_HomeAssignment"]

# Data model for player score
class PlayerScore(BaseModel):
    player_name: str # Accepts only strings
    score: int # Accepts only integers

@app.post("/upload_sprite", summary="Upload a sprite image")
async def upload_sprite(file: UploadFile = File(...)):
    """
    Upload a sprite image and save it in the 'sprites' collection.
    """
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="File is empty")
    sprite_doc = {"filename": file.filename, "content": content}
    result = await db.sprites.insert_one(sprite_doc)
    return {"message": "Sprite uploaded", "id": str(result.inserted_id)}

@app.post("/upload_audio", summary="Upload an audio file")
async def upload_audio(file: UploadFile = File(...)):
    """
    Upload an audio file and save it in the 'audio' collection.
    """
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="File is empty")
    audio_doc = {"filename": file.filename, "content": content}
    result = await db.audio.insert_one(audio_doc)
    return {"message": "Audio file uploaded", "id": str(result.inserted_id)}

@app.post("/player_score", summary="Submit a player score")
async def add_score(score: PlayerScore):
    """
    Save a player's score in the 'scores' collection.
    """
    score_doc = score.dict() # Turns the input into a dictionary < prevents SQL injection
    result = await db.scores.insert_one(score_doc) # Adds the data to the database
    return {"message": "Score recorded", "id": str(result.inserted_id)} # Sends back a success message
