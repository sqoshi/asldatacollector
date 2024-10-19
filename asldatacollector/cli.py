import logging
import os
import shutil
from typing import Optional

import typer

from asldatacollector.collect.collect import collect_data
from asldatacollector.collect.google.key import initialize_service
from asldatacollector.collect.google.storage import (
    delete_file,
    download_all_files,
    download_file,
    list_files,
    upload_file,
)
from asldatacollector.process.dataset import process_all

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger("htt")

app = typer.Typer()

DEFAULT_KEY = None

key_opt = typer.Option(
    DEFAULT_KEY, "--key", help="Encryption key for the service account"
)


@app.command()
def collect(
    draw: bool = typer.Option(
        False, "--draw/--no-draw", help="Draw hand landmarks connections"
    ),
    graph_samples: bool = typer.Option(
        False,
        "--graph-samples/--no-graph-samples",
        help="Draw image with one sample of each class",
    ),
    zip: bool = typer.Option(True, "--zip/--no-zip", help="Get output as zip"),
    clean: bool = typer.Option(
        False, "--clean/--no-clean", help="Remove images dir but keep only zip"
    ),
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
    collect_data(
        data_dir, classes_number, samples_number, capture_device, draw, graph_samples
    )
    if zip:
        shutil.make_archive("output", "zip", data_dir)
    if clean:
        shutil.rmtree(data_dir)


@app.command()
def process(
    data_dir: str = typer.Option(
        "./data", "--data-dir", "-d", help="Directory with images"
    ),
    output: str = typer.Option(
        "data.pickle", "--output", "-o", help="Output pickle file"
    ),
):
    """Transform images into dataset pickle."""
    process_all(data_dir, output)


@app.command()
def upload(
    file: str = typer.Argument(
        "output.zip",
        help="Path to zip file to upload to Google Drive",
    ),
    key: Optional[str] = key_opt,
):
    """Upload files to Google Storage."""
    if os.path.exists(file):
        service = initialize_service(key)
        if os.path.isdir(file):
            shutil.make_archive("output", "zip", file)
            file = "output.zip"
        upload_file(file, service)
    else:
        logging.info(f"File {file} does not exist")


@app.command()
def list(
    key: Optional[str] = key_opt,
):
    """List files in Google Storage."""
    service = initialize_service(key)
    list_files(service)


@app.command()
def delete(
    file_id: str = typer.Option(None, "--file-id", help="File ID to download"),
    key: Optional[str] = key_opt,
):
    """List files in Google Storage."""
    service = initialize_service(key)
    delete_file(file_id, service)


@app.command()
def download(
    file_id: Optional[str] = typer.Option(
        None, "--file-id", help="File ID to download"
    ),
    key: Optional[str] = key_opt,
    unpack_dir: Optional[str] = typer.Option(
        None, "--unpack-dir", "-ud", help="Directory to unpack files"
    ),
):
    """Download files from Google Drive."""
    service = initialize_service(key)
    if file_id:
        fn = f"{file_id}.zip"
        download_file(file_id, fn, service)
        if unpack_dir:
            logging.info("Unpacked to %s", unpack_dir)
            os.makedirs(unpack_dir, exist_ok=True)
            shutil.unpack_archive(fn, unpack_dir, "zip")
            os.remove(fn)
    else:
        download_all_files("./output", service)


if __name__ == "__main__":
    app()
