import queue
import logging
import threading
from flask_socketio import SocketIO
from flask import Flask, render_template
from services.config_service import ConfigService
from services.spotfiy_service import SpotifyService
from services.download_service import DownloadService
from services.playlist_manager import PlaylistManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class SpotSpotWebApp:
    def __init__(self):
        # Setup Flask App
        self.app = Flask(__name__)
        self.app.secret_key = "SECRET_KEY"
        self.socketio = SocketIO(self.app)
        # Setup Data
        self.download_queue = queue.Queue()
        self.download_history = {}
        self.active_downloads = {}
        # Instantiate
        self.config = ConfigService()
        self.spotify_services = SpotifyService(self.config)
        self.playlist_manager = PlaylistManager(self.config)
        self.download_services = DownloadService(self.config, self.playlist_manager, self.socketio, self.download_queue, self.download_history)
        # Setup Routes
        self.setup_routes()
        self.start_download_thread()

    def setup_routes(self):
        @self.app.route("/")
        def index_page():
            return render_template("index.html")

        @self.app.route("/status")
        def status_page():
            return render_template("status.html")

        @self.socketio.on("search")
        def handle_search(query_req):
            if not query_req.get("query"):
                self.socketio.emit("toast", {"title": "Blank Search Query", "body": "Please enter search request"})
                parsed_results = {}
            else:
                parsed_results = self.spotify_services.perform_spotify_search(query_req)
            self.socketio.emit("search_results", {"results": parsed_results})

        @self.socketio.on("download_item")
        def handle_download(requested_item):
            self.download_services.add_item_to_queue(requested_item)

        @self.socketio.on("get_status")
        def handle_get_status():
            self.socketio.emit("update_status", {"history": list(self.download_history.values())})

        @self.socketio.on("cancel_all")
        def cancel_all():
            logging.info(f"Request to cancel all download recieved")
            self.download_services.cancel_active_download()
            self.download_services.cancel_pending_downloads()

        @self.socketio.on("cancel_active")
        def cancel_active():
            logging.info(f"Request to cancel active download recieved")
            self.download_services.cancel_active_download()

    def start_download_thread(self):
        download_thread = threading.Thread(target=self.download_services.process_downloads, daemon=True)
        download_thread.start()

    def run_app(self):
        self.socketio.run(self.app, host="0.0.0.0", port=5000)

    def get_app(self):
        return self.app


spotspot_web_app = SpotSpotWebApp()

if __name__ == "__main__":
    spotspot_web_app.run_app()
else:
    app = spotspot_web_app.get_app()
