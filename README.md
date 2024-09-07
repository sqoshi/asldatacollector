# idatagate

`idatagate` is a CLI tool designed for managing and processing hand image datasets, as well as uploading files to Google Storage. It allows you to collect images, transform them into datasets, and manage files in Google Drive storage efficiently.

## Table Of Contents

- [idatagate](#idatagate)
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

To install `idatagate`, run:

```bash
pipx install idatagate
```

## Usage

### Collecting Hand Images

To collect images, run:

```bash
idatagate collect --data-dir /path/to/save/images --classes-number 26 --samples-number 100
```

The command will take images for 26 different classes (such as the alphabet in sign language) and store them in the specified directory. Each class will have by default 100 images collected using landmark detection.
The collection will continue until all images are gathered for each class.
The image collection uses real-time landmark detection to capture high-quality images. For reference, the classes are aligned with the alphabet as demonstrated in this example image:

![img](./package/idatagate/assets/alphabet.png)

#### Example Command

```bash
idatagate collect --data-dir ./images --classes-number 26 --samples-number 100
```

This command will continuously capture images for 26 classes (each corresponding to a letter of the alphabet) until 100 samples per class are collected.

### Uploading Files

To upload a zip file to Google Storage, use:

```bash
idatagate upload output.zip
```

Make sure the key is already set before running the upload command. If the key is not set, use the idatagate set-key command as described earlier.

### Listing Files

To list files in Google Storage, use:

```bash
idatagate list
```

### Downloading Files

To download a file from Google Storage, you can specify a file ID:

```bash
idatagate download --file-id <FILE_ID>
```

Or download all files:

```bash
idatagate download
```

### Instruction

Firsly collect the data with

```bash
idatagate collect
```

then upload files to server:

```bash
idatagate upload
```

### Caching the Encryption Key

The first time you run the set-key command, the key is securely stored using a credentials management system. You don't need to provide the key again unless you wish to change it.

bash

## Contributing

Feel free to open issues or contribute by submitting pull requests.

## License

This project is licensed under the MIT License.
