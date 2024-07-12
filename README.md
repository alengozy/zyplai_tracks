# zyplai_tracks
Take home assignment for zypl.ai

Quick Start:
1. Clone the repo
2. Cd to project root directory
3. Create a .env file with DB_NAME, DB_PASSWORD, DB_USER which are self-explanatory, and SECRET_KEY for JWT, which can be generated here: https://emn178.github.io/online-tools/sha256.html
4. Run ```docker-compose up -d --build```
5. (Optional) Run ```docker-compose exec web alembic revision --autogenerate -m "init"``` to create migrations
6. Run ```docker-compose exec web alembic upgrade head``` to apply migrations

```localhost:8000/docs``` to test endpoints

Includes JWT Authentication, see auth block to create new user, then press the Authenticate button in the top right corner prior to making requests.
