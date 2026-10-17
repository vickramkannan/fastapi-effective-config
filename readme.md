# FastAPI Effective Config

## Run locally
Install dependencies with `pip install -r requirements.txt`, then run:
`uvicorn main:app --reload`

Test:
`http://127.0.0.1:8000/effective-config?set=port=9000&set=debug=true`

## Render deployment
Build command: `pip install -r requirements.txt`
Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

Set these environment variables in Render:
- `APP_ENV=development`
- `APP_WORKERS=13`
- `APP_API_KEY=key-9i830akj9v`

Keep `.env` and `config.development.yaml` in the repository.
