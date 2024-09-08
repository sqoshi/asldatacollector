import logging
import os
import uuid
from datetime import datetime

from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from tabulate import tabulate


def upload_file(file_path: str, service):
    d = datetime.now().strftime("%Y%m%d%H%M%S")
    nm = f"{uuid.uuid4().hex}"
    metadata = {"name": f"{nm}_{d}_{os.path.basename(file_path)}"}
    media = MediaFileUpload(
        file_path, mimetype="application/zip", chunksize=256 * 1024, resumable=True
    )
    request = service.files().create(body=metadata, media_body=media, fields="id")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            prog = int(status.progress() * 100)
            if prog % 10 == 0:
                logging.info(f"Uploaded {prog}%")

    logging.info(f"Uploaded file with ID {response['id']}")


def list_files(service):
    """List all files in Google Drive with
    creation date, size, and URL to parent folder."""
    page_token = None
    data = []

    while True:
        results = (
            service.files()
            .list(
                pageSize=10,
                fields="nextPageToken, files(id, name, createdTime, size, parents)",
                pageToken=page_token,
            )
            .execute()
        )
        items = results.get("files", [])
        page_token = results.get("nextPageToken", None)

        if not items:
            logging.info("No files found.")
            break

        for item in items:
            size = item.get("size", "N/A")
            if size.isdigit():
                size = round(int(size) / (1024 * 1024), 2)

            data.append(
                [item["name"], item["id"], item.get("createdTime", ""), f"{size} MB"]
            )

        if not page_token:
            break

    headers = ["File Name", "File ID", "Created Time", "Size"]
    if data:
        table = tabulate(data, headers=headers, tablefmt="grid")
        logging.info("\n" + table)
    else:
        logging.info("No files to display.")


def download_file(file_id: str, destination_path: str, service):
    """Download a file from Google Drive."""
    request = service.files().get_media(fileId=file_id)
    with open(destination_path, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            logging.info(f"Download {int(status.progress() * 100)}%.")
    logging.info(f"Downloaded file to {destination_path}")


def download_all_files(destination_folder: str, service):
    """Download all files from Google Drive."""
    results = (
        service.files()
        .list(pageSize=10, fields="nextPageToken, files(id, name)")
        .execute()
    )
    items = results.get("files", [])
    if not items:
        logging.info("No files to download.")
    else:
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        for item in items:
            download_file(
                item["id"], os.path.join(destination_folder, item["name"]), service
            )


def delete_file(file_id: str, service):
    """Delete a file from Google Drive by its ID."""
    try:
        service.files().delete(fileId=file_id).execute()
        logging.info(f"Deleted file with ID {file_id}")
    except Exception as e:
        logging.error(f"An error occurred while deleting file with ID {file_id}: {e}")
