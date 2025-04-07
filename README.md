# database-project
Task 1
set up a python virtual environment
installed fastapi, uvicorn, etc...
created main.py with fastapi stuff from appendix b (uploaded to git)
ran http://127.0.0.1:8000/docs and worked
took screenshot of task 1 showing api working and the uvicorn main:app --reload working (word doc uploaded to git)
Installed all required packages: fastapi, uvicorn, motor, pydantic, python-dotenv, requests
made requirements.txt using pip freeze

Task 2
made a user on MongoDB Atlas with a username and password
used secure connection string given by MongoDB Atlas
linked it with Compass
linked MongoDB DB with main.py
collection showed up on Compass and Atlas
inserted mock data for testing via local host - worked

Task 3
tested all 3 endpoints locally using Postman (/upload_sprite, /upload_audio, /player_score) - worked
created and configured vercel.json
deployed the API to Vercel and accessed it at https://database-project-five.vercel.app/docs

Task 4
Whitelisted local IP address, used my personal IP to make it that i can access it then back to 0.0.0.0/0
Used Pydantic models to prevent SQL injection
    Example: score = PlayerScore(...), then score.dict() safely inserted
added IP whitelist entry and screenshot
added comments to code explaining each line of code
removed Word doc from repo and submitted it separately
filled the README.md
created Word document with all screenshots and links as required in Appendix A
zipped source code and prepared both files for submission

What tools i used: 
MongoDB Compass - to manage collections and view data
MongoDB Atlas - to host the database online
Visual Studio Code (VS Code) - to write and organize the code
VS Code Terminal - to run commands and launch the API
Postman - to test API endpoints with real data
Vercel - to deploy the API and make it publicly accessible
GitHub - to store and version-control the projec