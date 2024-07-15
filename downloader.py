import asyncio
import aiohttp
import os
from aiohttp import ClientSession
from urllib.parse import urlparse
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, ProgressBar, Label

class Downloader(App):

    CSS_PATH = "downloader.css"

    def __init__(self, url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = url
        self.filename = None
        self.is_paused = False
        self.is_downloading = False
        self.download_task = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label(self.url, id="url-label")
        yield ProgressBar(id="progress-bar")
        yield Label("Not started", id="status-label")
        yield Button("Start", id="start-button")
        yield Button("Pause", id="pause-button", disabled=True)
        yield Button("Cancel", id="cancel-button", disabled=True)
        yield Footer()

    async def fetch_filename(self, response):
        cd = response.headers.get("Content-Disposition")
        if cd and 'filename' in cd:
            filename = cd.split('filename=')[-1].strip('"')
        else:
            filename = os.path.basename(urlparse(self.url).path)
        return filename

    async def download_file(self):
        chunk_size = 1024 * 1024  # 1MB
        retries = 5
        retry_delay = 1
        session_timeout = aiohttp.ClientTimeout(total=None, connect=60, sock_connect=60, sock_read=60)

        async with aiohttp.ClientSession(timeout=session_timeout) as session:
            for attempt in range(retries):
                if self.is_paused:
                    await self.update_status("Paused")
                    await asyncio.sleep(1)
                    continue
                try:
                    async with session.get(self.url) as response:
                        self.filename = await self.fetch_filename(response)
                        total_size = int(response.headers.get("content-length", 0))
                        progress_bar = self.query_one("#progress-bar", ProgressBar)
                        progress_bar.max = total_size
                        progress = 0

                        with open(self.filename, "wb") as f:
                            while not self.is_paused:
                                chunk = await response.content.read(chunk_size)
                                if not chunk:
                                    break
                                f.write(chunk)
                                progress += len(chunk)
                                progress_bar.value = progress
                                await self.update_status(f"Downloading: {progress / total_size * 100:.2f}%")
                                
                            if self.is_paused:
                                await self.update_status("Paused")
                                await asyncio.sleep(1)
                                continue
                                
                        if progress == total_size:
                            await self.update_status("Download completed")
                        else:
                            await self.update_status("Download interrupted")
                    break

                except aiohttp.ClientError as e:
                    await self.update_status(f"Error: {e}")
                    if attempt < retries - 1:
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2
                    else:
                        await self.update_status("Download failed after retries")

    async def update_status(self, status):
        status_label = self.query_one("#status-label", Label)
        status_label.update(status)

    async def on_button_pressed(self, event):
        button_id = event.button.id
        if button_id == "start-button":
            self.is_downloading = True
            self.query_one("#start-button", Button).disabled = True
            self.query_one("#pause-button", Button).disabled = False
            self.query_one("#cancel-button", Button).disabled = False
            self.download_task = asyncio.create_task(self.download_file())
        elif button_id == "pause-button":
            self.is_paused = not self.is_paused
            if self.is_paused:
                self.query_one("#pause-button", Button).label = "Resume"
                await self.update_status("Paused")
            else:
                self.query_one("#pause-button", Button).label = "Pause"
        elif button_id == "cancel-button":
            if self.download_task:
                self.download_task.cancel()
            self.is_downloading = False
            self.is_paused = False
            self.query_one("#start-button", Button).disabled = False
            self.query_one("#pause-button", Button).disabled = True
            self.query_one("#cancel-button", Button).disabled = True
            await self.update_status("Cancelled")

if __name__ == "__main__":
    url = "https://example.com/largefile.zip"  # Replace with actual URL
    AsyncDownloader.run(title="AsyncDownloader", url=url)
