import os
from typing import Union
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api.cache import Cache
from api.classes import FaviconResponse, ImageMetadata, TemplateResolutionMetadata
from api.image_utils import ImageUtils
from api.constants import Constants

ENV_PREFIX = "RANDIMG"

version = os.getenv("APP_VERSION", "local-dev")
source_image_dir = os.getenv(f"{ENV_PREFIX}_IMAGE_DIR", "assets/images")
cache_dir = os.getenv(f"{ENV_PREFIX}_CACHE_DIR", "cache")
site_title = os.getenv(f"{ENV_PREFIX}_SITE_TITLE", "Random image")

app = FastAPI(title=site_title)
app.mount("/static", StaticFiles(directory="resources/static"), name="static")
templates = Jinja2Templates(directory="templates")

cache = Cache(image_dir=source_image_dir, cache_dir=cache_dir)


def get_file_response(
    image_id: str, width: int, height: int, download: bool = False, set_cache_header: bool = True
) -> FileResponse:
    if not cache.id_exists(image_id):
        raise HTTPException(status_code=404, detail=f"File with id='{image_id}' could not be found!")
    
    if width and width not in Constants.ALLOWED_DIMENSIONS:
        raise HTTPException(status_code=400, detail=f"Width is not of allowed value! Allowed values: {Constants.ALLOWED_DIMENSIONS}")
    
    if height and height not in Constants.ALLOWED_DIMENSIONS:
        raise HTTPException(status_code=400, detail=f"Height is not of allowed value! Allowed values: {Constants.ALLOWED_DIMENSIONS}")
    
    filename = cache.get_filename_and_generate_copy_if_missing(
        image_id, width=width, height=height
    )
    metadata = cache.get_metadata(image_id)
            
    headers = {
        "Content-Disposition": "inline" if not download else f'attachment; filename="{filename}"',
        "X-Image-Id": f"{image_id}",
    }
    
    if set_cache_header:
        headers["Cache-Control"] = "max-age=2592000, public, no-transform"

    return FileResponse(
        path=filename,
        media_type=metadata.media_type,
        headers=headers,
    )
    
def return_page(request: Request, image_id: str) -> HTMLResponse:
    filename = cache.get_filename_and_generate_copy_if_missing(image_id)
    
    current_height = 512    
    metadata = cache.get_metadata(image_id)
    current_width, current_height = ImageUtils.calculate_scaled_size(original_width=metadata.original_width, original_height=metadata.original_height, height=current_height)
    resolution_data = TemplateResolutionMetadata(original_width=metadata.original_width, original_height=metadata.original_height, current_width=current_width, current_height=current_height)
    
    return templates.TemplateResponse(
        request=request,
        name="image.html",
        context={"site_title": site_title, "image_id": image_id, "image_filename": filename, "height": current_height, "version": version, "resolution_data": resolution_data},
    )


@app.get("/favicon.ico", response_class=FaviconResponse)
async def get_favicon():
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
        + '<text y=".9em" font-size="90">🦈</text>'
        + "</svg>"
    )


@app.get("/", response_class=Union[HTMLResponse, RedirectResponse])
async def page_redirect_rand_image(request: Request, redirect: bool = False):
    image_id = cache.get_random_id()

    if redirect:
        return RedirectResponse(request.url_for("page_get_image", image_id=image_id))
    
    return return_page(request, image_id)


@app.get("/{image_id}", response_class=HTMLResponse)
async def page_get_image(request: Request, image_id: str):    
    return return_page(request, image_id)


@app.get("/api/img/{image_id}")
async def api_get_image(
    image_id: str,
    width: Union[int, None] = None,
    height: Union[int, None] = None,
    download: bool = False,
):
    return get_file_response(image_id, width=width, height=height, download=download)


@app.get("/api/img")
async def api_get_rand_image(
    width: Union[int, None] = None,
    height: Union[int, None] = None,
    download: bool = False,
):
    image_id = cache.get_random_id()
    return get_file_response(image_id, width=width, height=height, download=download, set_cache_header=False)
