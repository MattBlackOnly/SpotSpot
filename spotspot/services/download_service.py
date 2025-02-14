import os
import logging
import subprocess

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class DownloadService:
    def __init__(self, config, playlist_manager, socketio, download_queue, download_history):
        self.config = config
        self.playlist_manager = playlist_manager
        self.socketio = socketio
        self.download_queue = download_queue
        self.download_history = download_history
        self.spodtdl_subprocess = None

    def add_item_to_queue(self, data):
        logging.info(f"Download Requested: {data}")

        spotify_url = data.get("url")
        item_type = data.get("type")
        item_name = data.get("name")
        item_artist = data.get("artist")

        download_info = {"name": item_name, "type": item_type, "artist": item_artist, "url": spotify_url, "status": "Pending..."}

        self.download_queue.put((spotify_url, download_info))
        self.download_history[spotify_url] = download_info

        self.socketio.emit("update_status", {"history": list(self.download_history.values())})

    def process_downloads(self):
        while True:
            url, download_info = self.download_queue.get()

            if download_info["status"] == "Cancelled":
                self.download_queue.task_done()
                continue

            if download_info["type"] == "track":
                download_path = self.config.track_output
            elif download_info["type"] == "playlist":
                download_path = self.config.playlist_output
            elif download_info["type"] == "album":
                download_path = self.config.album_output
            elif download_info["type"] == "artist":
                download_path = self.config.artist_output

            download_info["status"] = "Downloading..."
            self.download_history[url] = download_info
            self.socketio.emit("update_status", {"history": list(self.download_history.values())})

            try:
                logging.info(f"Downloading: {url}")

                command = ["spotdl", "--output", f"{download_path}", url]
                logging.info(f"SpotDL command: {command}")

                self.spodtdl_subprocess = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = self.spodtdl_subprocess.communicate()

                if self.config.extra_logging.lower() == "true":
                    logging.info(f"Extra Logging: {stdout=}")
                    logging.info(f"Extra Logging: {stderr=}")

                if download_info["status"] == "Cancelled":
                    self.download_queue.task_done()
                    continue

                if self.spodtdl_subprocess.returncode == 0:
                    download_info["status"] = "Complete"
                    logging.info(f"Finished Item")
                else:
                    download_info["status"] = "Failed"
                    logging.error(f"Error downloading: {stderr}")

                self.download_history[url] = download_info

            except Exception as e:
                logging.error(f"Process Downloads Error: {str(e)}")
                download_info["status"] = "Error"
                self.download_history[url] = download_info

            self.socketio.emit("update_status", {"history": list(self.download_history.values())})

            self.download_queue.task_done()

            if self.download_queue.empty():
                logging.info("Queue is empty")
                self.playlist_manager.media_server_refresh_check()

    def cancel_active_download(self):
        try:
            if not self.spodtdl_subprocess:
                logging.info(f"No active download.")
                return

            logging.info(f"Cancelling active download.")
            self.spodtdl_subprocess.terminate()

            # Find the active download in history and update its status
            for url, info in self.download_history.items():
                if info["status"] == "Downloading...":
                    info["status"] = "Cancelled"
                    self.download_history[url] = info
                    break

            self.spodtdl_subprocess = None

        except Exception as e:
            logging.error(f"Cancel Active Error: {str(e)}")

        finally:
            self.socketio.emit("update_status", {"history": list(self.download_history.values())})

    def cancel_pending_downloads(self):
        try:
            temp_queue = []
            while not self.download_queue.empty():
                url, download_info = self.download_queue.get()
                download_info["status"] = "Cancelled"
                self.download_history[url] = download_info
                temp_queue.append((url, download_info))

            for item in temp_queue:
                self.download_queue.put(item)

        except Exception as e:
            logging.error(f"Cancel Pending Error: {str(e)}")

        finally:
            self.socketio.emit("update_status", {"history": list(self.download_history.values())})
