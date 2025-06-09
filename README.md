# Base64File Library for Robot Framework

[![PyPI version](https://badge.fury.io/py/robotframework-base64file.svg)](https://pypi.org/project/robotframework-base64file/)
[![Python versions](https://img.shields.io/pypi/pyversions/robotframework-base64file.svg)](https://pypi.org/project/robotframework-base64file/)

Professional Base64 file handling for Robot Framework with large file support.

## Features

- 🚀 **Memory-efficient** chunked processing
- ⚡ **Multi-GB file support** with streaming
- 🔧 **Configurable chunk sizes** (1KB-100MB+)
- 📄 **Automatic documentation** with libdoc
- 🔄 **Bidirectional conversion**:
  - File ↔ Base64 string
  - File ↔ Base64 file

## Installation

```bash
pip install robotframework-base64file
```

## Basic Usage

```robotframework
*** Settings ***
Library    base64Library

*** Test Cases ***
Encode and Decode File
    ${base64}=    File To Base64    original.pdf
    Base64 To File    ${base64}    copy.pdf
    
Process Large Video
    File To Base64 File    input.mp4    encoded.txt    chunk_size=10MB
    Base64 File To File    encoded.txt    output.mp4
```

## Advanced Options

Configure chunk size globally:
```robotframework
*** Settings ***
Library    base64Library    chunk_size=5MB
```

## API Reference

| Keyword | Arguments | Description |
|---------|-----------|-------------|
| File To Base64 | file_path, chunk_size=None | Encodes file to Base64 string |
| Base64 To File | base64_str, output_path | Saves Base64 string to file |
| File To Base64 File | input_path, output_path, chunk_size=None | Streams file to Base64 file |
| Base64 File To File | input_path, output_path, chunk_size=None | Streams Base64 file to binary |

## License

Apache 2.0 - See [LICENSE](LICENSE) file