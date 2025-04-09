from fastapi import FastAPI, File, UploadFile, HTTPException, Body
from pydantic import BaseModel
import motor.motor_asyncio
from bson import ObjectId

app = FastAPI(
    title="Fast API",
    description="API for uploading and managing sprites, audio files, and player scores"
)

client = motor.motor_asyncio.AsyncIOMotorClient( # MongoDB client
    "mongodb+srv://ictstudent:mcast1234@cluster0.qbuvr7z.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
db = client["Database_HomeAssignment"] # Database access

class PlayerScore(BaseModel): # Data model for player scores
    player_name: str
    score: int

# ====================
# Sprite Endpoints
# ====================
@app.get("/sprites", summary="List All Sprites", tags=["Sprites"]) # API endpoint for retrieving sprites
async def get_all_sprites():
    """Retrieves all sprite documents.""" # Function description
    sprites = await db.sprites.find().to_list(length=None) # Get sprites from DB
    return [{"id": str(sprite["_id"]), "filename": sprite["filename"]} for sprite in sprites] # Format and return data


@app.get("/sprites/{id}", summary="Retrieve a Sprite by ID", tags=["Sprites"]) # API endpoint for retrieving sprites by ID
async def get_sprite_by_id(id: str):
    """Retrieve a specific sprite by its ID.""" # Function description
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format") # Validate ID format
    sprite = await db.sprites.find_one({"_id": ObjectId(id)}) # Fetch sprite by ID
    if sprite is None:
        raise HTTPException(status_code=404, detail="Sprite not found") # Raise error if sprite does not exist
    return {"id": str(sprite["_id"]), "filename": sprite["filename"]} # Return sprite details


@app.post("/sprites", summary="Upload a Sprite", tags=["Sprites"]) # API endpoint for sprite upload
async def upload_sprite(file: UploadFile = File(...)):
    """Upload a sprite image file.""" # Function description
    content = await file.read() # Read file content
    if not content:
        raise HTTPException(status_code=400, detail="File is empty") # Validate file is not empty
    sprite_doc = {"filename": file.filename, "content": content}
    result = await db.sprites.insert_one(sprite_doc) # Insert sprite into database
    return {"message": "Sprite uploaded", "id": str(result.inserted_id)} # Return success message


@app.put("/sprites/{id}", summary="Update a Sprite by ID", tags=["Sprites"]) # API endpoint to update a sprite by ID
async def update_sprite(id: str, updates: dict = Body(...)):
    """Update details of a sprite by its ID.""" # Function description
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format") # Validate ID format
    result = await db.sprites.update_one({"_id": ObjectId(id)}, {"$set": updates}) # Update sprite in DB
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Sprite not updated") # Raise error if no sprite was updated
    return {"message": "Sprite updated successfully"} # Return success message


@app.delete("/sprites/{id}", summary="Delete a Sprite by ID", tags=["Sprites"]) # API endpoint to delete a sprite by ID
async def delete_sprite(id: str):
    """Delete a sprite by its ID.""" # Function description
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format") # Validate ID format
    result = await db.sprites.delete_one({"_id": ObjectId(id)}) # Attempt to delete the sprite
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Sprite not found") # Handle sprite not found
    return {"message": "Sprite deleted successfully"} # Confirm deletion success

# ====================
# Audio Endpoints
# ====================
@app.get("/audio", summary="List All Audio Files", tags=["Audio"]) # API endpoint to list all audio files
async def get_all_audio():
    """Retrieves all audio documents.""" # Function description
    audios = await db.audio.find().to_list(length=None) # Retrieve all audio files from the database
    return [{"id": str(audio["_id"]), "filename": audio["filename"]} for audio in audios] # Return list of audio files with ID and filename


@app.get("/audio/{id}", summary="Retrieve an Audio File by ID", tags=["Audio"]) # API endpoint to retrieve audio by ID
async def get_audio_by_id(id: str):
    """Retrieve a specific audio file by its ID."""  # Function description
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format") # Validate ID format
    audio = await db.audio.find_one({"_id": ObjectId(id)}) # Fetch specified audio file from DB
    if audio is None:
        raise HTTPException(status_code=404, detail="Audio not found") # Error if not found
    return {"id": str(audio["_id"]), "filename": audio["filename"]} # Return audio details


@app.post("/audio", summary="Upload an Audio File", tags=["Audio"]) # API endpoint to upload audio files
async def upload_audio(file: UploadFile = File(...)):
    """Upload an audio file."""  # Function description
    content = await file.read() # Read the content of the uploaded file
    if not content:
        raise HTTPException(status_code=400, detail="File is empty") # Check if file is empty
    audio_doc = {"filename": file.filename, "content": content}
    result = await db.audio.insert_one(audio_doc) # Insert into the DB
    return {"message": "Audio file uploaded", "id": str(result.inserted_id)} # Return success message and ID


@app.put("/audio/{id}", summary="Update an Audio File by ID", tags=["Audio"]) # Endpoint to update an existing audio file
async def update_audio(id: str, updates: dict = Body(...)):
    """Update details of an audio file by its ID."""  # Function description
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format") # Validate ID format
    result = await db.audio.update_one({"_id": ObjectId(id)}, {"$set": updates}) # Update in DB
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Audio not updated") # Check if the update was successful
    return {"message": "Audio updated successfully"} # Return success message 


@app.delete("/audio/{id}", summary="Delete an Audio File by ID", tags=["Audio"]) # Endpoint to delete an existing audio file
async def delete_audio(id: str):
    """Delete an audio file by its ID."""  # Function description
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format") # Validate ID format
    result = await db.audio.delete_one({"_id": ObjectId(id)}) # Delete from DB with ID
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Audio not found") # If not found
    return {"message": "Audio deleted successfully"} # Return success message

# ====================
# Player Score Endpoints
# ====================
@app.get("/scores", summary="List All Player Scores", tags=["Player Scores"]) # Endpoint to list all player scores
async def get_all_scores():
    """Retrieves all player scores."""  # Function purpose
    scores = await db.scores.find().to_list(length=None) # Fetch all scores from DB
    return [{"id": str(score["_id"]), "player_name": score["player_name"], "score": score["score"]} for score in scores] # Return scores


@app.get("/scores/{id}", summary="Retrieve a Player Score by ID", tags=["Player Scores"]) # Endpoint to get a specific score by ID
async def get_score_by_id(id: str):
    """Retrieve a player score by its ID."""  # Function purpose
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format") # Validate ID format
    score = await db.scores.find_one({"_id": ObjectId(id)}) # search score in the DB using ID
    if score is None:
        raise HTTPException(status_code=404, detail="Score not found") # Return error if not found
    return {"id": str(score["_id"]), "player_name": score["player_name"], "score": score["score"]} # Return score details


@app.post("/scores", summary="Submit a Player Score", tags=["Player Scores"]) # Endpoint to submit a new player score
async def add_score(score: PlayerScore):
    """Record a player's score."""  # Function purpose
    score_doc = score.dict()
    result = await db.scores.insert_one(score_doc)  # Insert score into DB
    return {"message": "Score recorded", "id": str(result.inserted_id)} # Return confirmation with new score ID


@app.put("/scores/{id}", summary="Update a Player Score by ID", tags=["Player Scores"]) # Endpoint to update a score by ID
async def update_score(id: str, updates: PlayerScore = Body(...)):
    """Update a player score by its ID."""  # Function purpose
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format") # Validate ID format
    updates_dict = updates.dict(exclude_unset=True)
    result = await db.scores.update_one({"_id": ObjectId(id)}, {"$set": updates_dict})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Score not updated")
    return {"message": "Score updated successfully"} # Return success message


@app.delete("/scores/{id}", summary="Delete a Player Score by ID", tags=["Player Scores"]) # Endpoint to delete a score by ID
async def delete_score(id: str):
    """Delete a player score by its ID."""  # Function purpose
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format") # Validate ID format
    result = await db.scores.delete_one({"_id": ObjectId(id)})  # Attempt to delete score from DB
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Score not found") # Score doesn't exist
    return {"message": "Score deleted successfully"} # Confirm deletion
