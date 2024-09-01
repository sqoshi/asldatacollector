import logging
import os
import shutil
from typing import Optional

import typer

from .collect import collect_data
from .storage import download_all_files, download_file, list_files, upload_file
from .utils import initialize_service

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger("htt")

app = typer.Typer()

DEFAULT_KEY = None


@app.command()
def collect(
    zip: bool = typer.Option(True, "--zip/--no-zip", help="Get output as zip"),
    data_dir: str = typer.Option(
        "/tmp/data", "--data-dir", "-d", help="Directory to store images"
    ),
    classes_number: int = typer.Option(
        26, "--classes-number", "-cn", help="Number of classes"
    ),
    samples_number: int = typer.Option(
        100, "--samples-number", "-sn", help="Number of images per class"
    ),
    capture_device: int = typer.Option(0, "--capture-device", help="Camera device ID"),
):
    """Take hand images."""
    collect_data(data_dir, classes_number, samples_number, capture_device)
    if zip:
        shutil.make_archive("output", "zip", data_dir)
        shutil.rmtree(data_dir)


@app.command()
def process(
    data_dir: str = typer.Option(
        "./data", "--data-dir", "-d", help="Directory with images"
    ),
):
    """Transform images into dataset pickle."""
    logging.info("not implemented %s", data_dir)


@app.command()
def upload(
    file: str = typer.Argument(
        "output.zip",
        help="Path to zip file to upload to Google Drive",
    ),
    key: Optional[str] = typer.Option(
        DEFAULT_KEY, "--key", help="Encryption key for the service account"
    ),
):
    """Upload files to Google Storage."""
    if os.path.exists(file):
        service = initialize_service(key)
        upload_file(file, service)
    else:
        logging.info(f"File {file} does not exist")


@app.command()
def list(
    key: Optional[str] = typer.Option(
        DEFAULT_KEY, "--key", help="Encryption key for the service account"
    ),
):
    """List files in Google Storage."""
    service = initialize_service(key)
    list_files(service)


@app.command()
def download(
    file_id: Optional[str] = typer.Option(
        None, "--file-id", help="File ID to download"
    ),
    key: Optional[str] = typer.Option(
        DEFAULT_KEY, "--key", help="Encryption key for the service account"
    ),
):
    """Download files from Google Drive."""
    service = initialize_service(key)
    if file_id:
        download_file(file_id, f"./{file_id}.zip", service)
    else:
        download_all_files("./dataset.zip", service)


if __name__ == "__main__":
    app()
