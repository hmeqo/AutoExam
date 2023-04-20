from fastapi.requests import Request
from fastapi.responses import Response

from .app import app


@app.middleware('http')
async def modify_js_file_header(request: Request, call_next):
    response: Response = await call_next(request)
    index = request.url.path.rfind('.')
    if index != -1 and request.url.path[index:] in ('.js'):
        response.headers['content-type'] = 'text/javascript'
    return response
