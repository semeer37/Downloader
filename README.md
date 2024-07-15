# Downloader

Downloader is a Python application designed for efficiently downloading single large files using asynchronous programming techniques. It features a reactive and user-friendly interface powered by the `textual` library, ensuring smooth interaction and real-time updates during the download process.

## Features

1. **Asynchronous Downloading:**
   - Utilizes `asyncio` and `aiohttp` for efficient and non-blocking file downloads.
   - Supports downloading large files seamlessly without impacting performance.
   - Handles chunked downloads and connection pooling.

2. **Reactive User Interface:**
   - Built with `textual` for a responsive and intuitive user interface.
   - Displays real-time download progress, status updates, and error messages.

3. **Single File Focus:**
   - Simplified interface dedicated to downloading a single large file at a time.
   - Provides controls for starting, pausing/resuming, and canceling downloads.

4. **Error Handling and Retry:**
   - Gracefully handles network errors and interruptions during downloads.
   - Implements adaptive retry logic with exponential backoff.
   - Detects offline status and automatically pauses downloads, resuming them when the network is available again.

5. **Progress Visualization:**
   - Shows download progress with a dynamic progress bar.
   - Displays the current download percentage.

## Installation

### Prerequisites

- Python 3.7 or higher
- `aiohttp` library
- `textual` library

### Install Dependencies

```bash
pip install aiohttp textual
```

