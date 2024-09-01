import logging
import os
import shutil
from typing import Optional

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .collect import collect_data
from .storage import download_all_files, download_file, list_files, upload_file
from .utils import initialize_service

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger("htt")

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup template directory
templates = Jinja2Templates(directory="templates")

DEFAULT_KEY = None


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    """Serve the main page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/collect/")
async def collect(
    zip: bool = Form(True),
    data_dir: str = Form("/tmp/data"),
    classes_number: int = Form(26),
    samples_number: int = Form(100),
    capture_device: int = Form(0),
):
    """Endpoint to start data collection."""
    collect_data(data_dir, classes_number, samples_number, capture_device)
    if zip:
        shutil.make_archive("output", "zip", data_dir)
        shutil.rmtree(data_dir)
        return FileResponse("output.zip")
    return {"status": "Data collection completed without zipping."}


@app.post("/process/")
async def process(data_dir: str = Form("./data")):
    """Endpoint to process images into dataset pickle."""
    logging.info("Processing data from directory %s", data_dir)
    # Your processing logic here
    return {"status": "Processing not implemented yet"}


@app.post("/upload/")
async def upload(file: UploadFile = File(...), key: Optional[str] = Form(DEFAULT_KEY)):
    """Upload files to Google Storage."""
    file_location = f"temp/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    service = initialize_service(key)
    upload_file(file_location, service)
    os.remove(file_location)
    return {"status": "File uploaded successfully"}


@app.get("/list/")
async def list(key: Optional[str] = Form(DEFAULT_KEY)):
    """List files in Google Storage."""
    service = initialize_service(key)
    files = list_files(service)
    return {"files": files}


@app.post("/download/")
async def download(
    file_id: Optional[str] = Form(None), key: Optional[str] = Form(DEFAULT_KEY)
):
    """Download files from Google Drive."""
    service = initialize_service(key)
    if file_id:
        download_file(file_id, f"./{file_id}.zip", service)
        return FileResponse(f"./{file_id}.zip")
    else:
        download_all_files("./dataset.zip", service)
        return FileResponse("./dataset.zip")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
