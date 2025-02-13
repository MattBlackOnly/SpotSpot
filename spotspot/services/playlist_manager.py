import os
import requests
import logging
from plexapi.server import PlexServer

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class PlaylistManager:
    def __init__(self, config):
        self.config = config

    def generate_m3u_playlist(self):
        try:
            folder_path = "/data"
            logging.info("Generating M3U playlist for immediate /data folder")

            # Ensure playlist directory exists
            os.makedirs(self.config.m3u_playlist_path, exist_ok=True)

            m3u_file_path = os.path.join(self.config.m3u_playlist_path, f"{self.config.m3u_playlist_name}.m3u")

            with open(m3u_file_path, "w") as m3u_file:
                for file in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, file)
                    if os.path.isfile(file_path) and any(file.endswith(ext.lower()) for ext in self.config.supported_formats):
                        relative_path = os.path.join(self.config.relative_server_path, file)
                        m3u_file.write(f"{relative_path}\n")

            logging.info(f"M3U playlist generated at: {m3u_file_path}")

        except Exception as e:
            logging.error(f"Playlist Generation Error: {str(e)}")

    def refresh_plex_library(self):
        try:
            logging.info("Refreshing Plex library...")
            plex_server = PlexServer(self.config.plex_address, self.config.plex_token)
            library_section = plex_server.library.section(self.config.plex_library_name)
            library_section.update()
            logging.info(f"Plex Library scan for '{self.config.plex_library_name}' started.")

        except Exception as e:
            logging.error(f"Plex scan error: {str(e)}")

    def refresh_jellyfin_library(self):
        try:
            logging.info("Refreshing Jellyfin library...")
            url = f"{self.config.jellyfin_address}/Library/Refresh?api_key={self.config.jellyfin_api_key}"
            response = requests.post(url)

            if response.status_code == 204:
                logging.info("Jellyfin library refreshed successfully.")
            else:
                logging.error(f"Failed to refresh Jellyfin library: {response.status_code} - {response.text}")

        except Exception as e:
            logging.error(f"Jellyfin scan error: {str(e)}")

    def media_server_refresh_check(self):
        # Refresh Library to pick up new files
        if self.config.trigger_jellyfin_scan.lower() == "true":
            self.refresh_jellyfin_library()
        if self.config.trigger_plex_scan.lower() == "true":
            self.refresh_plex_library()

        # Generate/Update Playlist
        if self.config.generate_m3u_playlist.lower() == "true":
            logging.info("M3U Playlist Generation started...")
            self.generate_m3u_playlist()

        # Refresh Library to pick up playlist
        if self.config.trigger_jellyfin_scan.lower() == "true":
            self.refresh_jellyfin_library()
        if self.config.trigger_plex_scan.lower() == "true":
            self.refresh_plex_library()
