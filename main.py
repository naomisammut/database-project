# main.py - FastAPI app for uploading sprites, audio, and player scores

from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import motor.motor_asyncio

# Initialize FastAPI app with title and description
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

# Uploads and stores a sprite.
@app.post("/upload_sprite", summary="Upload a sprite image") # POST endpoint for sprite upload
async def upload_sprite(file: UploadFile = File(...)): # Accept sprite file
    """
    Upload a sprite image and save it in the 'sprites' collection.
    """
    content = await file.read() # Read file data
    if not content: # Check if empty
        raise HTTPException(status_code=400, detail="File is empty") # Raise error if empty
    sprite_doc = {"filename": file.filename, "content": content} # Prepares data to insert 
    result = await db.sprites.insert_one(sprite_doc) # Saves to DB
    return {"message": "Sprite uploaded", "id": str(result.inserted_id)} # Return result

# Handles audio file upload and stores it in the database.
@app.post("/upload_audio", summary="Upload an audio file") # Defines POST endpoint for audio upload
async def upload_audio(file: UploadFile = File(...)): # Accepts audio file
    """
    Upload an audio file and save it in the 'audio' collection.
    """
    content = await file.read() # Reads the file content
    if not content: # Checks if the file is empty
        raise HTTPException(status_code=400, detail="File is empty") # Raises an error if empty
    audio_doc = {"filename": file.filename, "content": content} # Prepares data to insert
    result = await db.audio.insert_one(audio_doc) # Save to DB
    return {"message": "Audio file uploaded", "id": str(result.inserted_id)} # Return response

# Saves player score to database.
@app.post("/player_score", summary="Submit a player score") # POST endpoint for score
async def add_score(score: PlayerScore): # Get player score input
    """
    Save a player's score in the 'scores' collection.
    """
    score_doc = score.dict() # Turns the input into a dictionary < prevents SQL injection
    result = await db.scores.insert_one(score_doc) # Adds the data to the database
    return {"message": "Score recorded", "id": str(result.inserted_id)} # Sends back a success message
