from fastapi import FastAPI, File, UploadFile, HTTPException, Body
from pydantic import BaseModel
import motor.motor_asyncio
from bson import ObjectId

app = FastAPI(
    title="Fast API",
    description="API for uploading and managing sprites, audio files, and player scores"
)

client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb+srv://ictstudent:mcast1234@cluster0.qbuvr7z.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
db = client["Database_HomeAssignment"]

class PlayerScore(BaseModel):
    player_name: str
    score: int

# ====================
# Sprite Endpoints
# ====================
@app.get("/sprites", summary="List All Sprites", tags=["Sprites"])
async def get_all_sprites():
    """Retrieves all sprite documents."""
    sprites = await db.sprites.find().to_list(length=None)
    return [{"id": str(sprite["_id"]), "filename": sprite["filename"]} for sprite in sprites]

@app.get("/sprites/{id}", summary="Retrieve a Sprite by ID", tags=["Sprites"])
async def get_sprite_by_id(id: str):
    """Retrieve a specific sprite by its ID."""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    sprite = await db.sprites.find_one({"_id": ObjectId(id)})
    if sprite is None:
        raise HTTPException(status_code=404, detail="Sprite not found")
    return {"id": str(sprite["_id"]), "filename": sprite["filename"]}

@app.post("/sprites", summary="Upload a Sprite", tags=["Sprites"])
async def upload_sprite(file: UploadFile = File(...)):
    """Upload a sprite image file."""
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="File is empty")
    sprite_doc = {"filename": file.filename, "content": content}
    result = await db.sprites.insert_one(sprite_doc)
    return {"message": "Sprite uploaded", "id": str(result.inserted_id)}

@app.put("/sprites/{id}", summary="Update a Sprite by ID", tags=["Sprites"])
async def update_sprite(id: str, updates: dict = Body(...)):
    """Update details of a sprite by its ID."""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    result = await db.sprites.update_one({"_id": ObjectId(id)}, {"$set": updates})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Sprite not updated")
    return {"message": "Sprite updated successfully"}

@app.delete("/sprites/{id}", summary="Delete a Sprite by ID", tags=["Sprites"])
async def delete_sprite(id: str):
    """Delete a sprite by its ID."""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    result = await db.sprites.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Sprite not found")
    return {"message": "Sprite deleted successfully"}

# ====================
# Audio Endpoints
# ====================
@app.get("/audio", summary="List All Audio Files", tags=["Audio"])
async def get_all_audio():
    """Retrieves all audio documents."""
    audios = await db.audio.find().to_list(length=None)
    return [{"id": str(audio["_id"]), "filename": audio["filename"]} for audio in audios]

@app.get("/audio/{id}", summary="Retrieve an Audio File by ID", tags=["Audio"])
async def get_audio_by_id(id: str):
    """Retrieve a specific audio file by its ID."""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    audio = await db.audio.find_one({"_id": ObjectId(id)})
    if audio is None:
        raise HTTPException(status_code=404, detail="Audio not found")
    return {"id": str(audio["_id"]), "filename": audio["filename"]}

@app.post("/audio", summary="Upload an Audio File", tags=["Audio"])
async def upload_audio(file: UploadFile = File(...)):
    """Upload an audio file."""
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="File is empty")
    audio_doc = {"filename": file.filename, "content": content}
    result = await db.audio.insert_one(audio_doc)
    return {"message": "Audio file uploaded", "id": str(result.inserted_id)}

@app.put("/audio/{id}", summary="Update an Audio File by ID", tags=["Audio"])
async def update_audio(id: str, updates: dict = Body(...)):
    """Update details of an audio file by its ID."""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    result = await db.audio.update_one({"_id": ObjectId(id)}, {"$set": updates})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Audio not updated")
    return {"message": "Audio updated successfully"}

@app.delete("/audio/{id}", summary="Delete an Audio File by ID", tags=["Audio"])
async def delete_audio(id: str):
    """Delete an audio file by its ID."""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    result = await db.audio.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Audio not found")
    return {"message": "Audio deleted successfully"}

# ====================
# Player Score Endpoints
# ====================
@app.get("/scores", summary="List All Player Scores", tags=["Player Scores"])
async def get_all_scores():
    """Retrieves all player scores."""
    scores = await db.scores.find().to_list(length=None)
    return [{"id": str(score["_id"]), "player_name": score["player_name"], "score": score["score"]} for score in scores]

@app.get("/scores/{id}", summary="Retrieve a Player Score by ID", tags=["Player Scores"])
async def get_score_by_id(id: str):
    """Retrieve a player score by its ID."""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    score = await db.scores.find_one({"_id": ObjectId(id)})
    if score is None:
        raise HTTPException(status_code=404, detail="Score not found")
    return {"id": str(score["_id"]), "player_name": score["player_name"], "score": score["score"]}

@app.post("/scores", summary="Submit a Player Score", tags=["Player Scores"])
async def add_score(score: PlayerScore):
    """Record a player's score."""
    score_doc = score.dict()
    result = await db.scores.insert_one(score_doc)
    return {"message": "Score recorded", "id": str(result.inserted_id)}

@app.put("/scores/{id}", summary="Update a Player Score by ID", tags=["Player Scores"])
async def update_score(id: str, updates: PlayerScore = Body(...)):
    """Update a player score by its ID."""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    updates_dict = updates.dict(exclude_unset=True)
    result = await db.scores.update_one({"_id": ObjectId(id)}, {"$set": updates_dict})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Score not updated")
    return {"message": "Score updated successfully"}

@app.delete("/scores/{id}", summary="Delete a Player Score by ID", tags=["Player Scores"])
async def delete_score(id: str):
    """Delete a player score by its ID."""
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    result = await db.scores.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Score not found")
    return {"message": "Score deleted successfully"}
