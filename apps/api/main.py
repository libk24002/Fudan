from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from apps.api.app.routes import problems, review, sandbox


app = FastAPI()
web_root = Path(__file__).resolve().parents[2] / "web"
web_dist = web_root / "dist"


@app.get('/api/health')
def health():
    return {'status': 'ok'}


app.include_router(problems.router)
app.include_router(sandbox.router)
app.include_router(review.router)

if web_dist.exists() and (web_dist / "assets").exists():
    app.mount("/assets", StaticFiles(directory=web_dist / "assets"), name="web-assets")


@app.get("/")
def root():
    index = web_dist / "index.html"
    if index.exists():
        return FileResponse(index)
    return {"message": "web ui not built, run npm run build in apps/web"}
