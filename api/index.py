from api import app

@app.get("/")
async def root_endpoint():
    return {"message": "Bot is running!"}