# asldatacollector

`asldatacollector` is a CLI tool designed for managing and processing hand image datasets, as well as uploading files to Google Storage. It allows you to collect images, transform them into datasets, and manage files in Google Drive storage efficiently.

## Table Of Contents

- [asldatacollector](#asldatacollector)
  - [Table Of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Collecting Hand Images](#collecting-hand-images)
      - [Example Command](#example-command)
    - [Uploading Files](#uploading-files)
    - [Listing Files](#listing-files)
    - [Downloading Files](#downloading-files)
    - [Instruction](#instruction)
    - [Caching the Encryption Key](#caching-the-encryption-key)
  - [Contributing](#contributing)
  - [License](#license)

## Features

- **Collect hand images** with real-time landmark detection for multiple classes.
- **Upload files** to Google Storage.
- **Download files** or list files from Google Storage.

## Installation

To install `asldatacollector`, run:

```bash
pipx install asldatacollector
```

## Usage

### Collecting Hand Images

To collect images, run:

```bash
asldatacollector collect --data-dir /path/to/save/images --classes-number 26 --samples-number 100
```

The command will take images for 26 different classes (such as the alphabet in sign language) and store them in the specified directory. Each class will have by default 100 images collected using landmark detection.
The collection will continue until all images are gathered for each class.
The image collection uses real-time landmark detection to capture high-quality images. For reference, the classes are aligned with the alphabet as demonstrated in this example image:

![img](https://github.com/sqoshi/asldatacollector/raw/master/asldatacollector/assets/alphabet.png)

#### Example Command

```bash
asldatacollector collect --data-dir ./images --classes-number 26 --samples-number 100
```

This command will continuously capture images for 26 classes (each corresponding to a letter of the alphabet) until 100 samples per class are collected.

### Uploading Files

To upload a zip file to Google Storage, use:

```bash
asldatacollector upload --key <API_KEY>
```

Make sure the key is already set before running the upload command. If the key is not set, use the asldatacollector set-key command as described earlier.

### Listing Files

To list files in Google Storage, use:

```bash
asldatacollector list
```

### Downloading Files

To download a file from Google Storage, you can specify a file ID:

```bash
asldatacollector download --file-id <FILE_ID>
```

Or download all files:

```bash
asldatacollector download
```

### Instruction

Firsly collect the data with

```bash
asldatacollector collect
```

then upload files to server:

```bash
asldatacollector upload
```

### Caching the Encryption Key

It is possible


## Contributing

Feel free to open issues or contribute by submitting pull requests.

## License

This project is licensed under the MIT License.
