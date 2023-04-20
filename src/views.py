from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

from src.app import app
from src import settings
from src import req
from src.models import *

app.mount(
    '/assets',
    StaticFiles(directory=settings.STATIC_DIR, html=True),
    name='static',
)


@app.get("/", response_class=HTMLResponse)
async def root() -> HTMLResponse:
    return HTMLResponse(
        (settings.DIST_DIR / 'index.html').read_text(),
        media_type='text/html',
    )


@app.post('/submitexam', response_model=str)
async def submit_exam(request: Request, exam: Exam):
    print(exam)
    response = req.main(request, exam)
    print(response)
    return response
