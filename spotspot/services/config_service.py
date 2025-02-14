import os
import json
import logging
import platform

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class ConfigService:
    def __init__(self):
        self.get_vars()
        self.get_spotdl_vars()
        self.create_config_file()

    def get_vars(self):
        logging.info("Loading Environmental Variables...")

        os_system = platform.system()
        logging.info(f"OS: {os_system}")

        self.config_path = "D:\\config.json" if os_system == "Windows" else "/home/appuser/.spotdl/config.json"
        logging.info(f"Config file path: {self.config_path}")

        self.ffmpeg_location = "D:\\" if os_system == "Windows" else "/usr/bin/ffmpeg"
        logging.info(f"FFmpeg location set to: {self.ffmpeg_location}")

        self.track_output = os.getenv("TRACK_OUTPUT", "/data/media/music/singles/{artist} - {title}.{output-ext}")
        logging.info(f"Track Output: {self.track_output}")

        self.album_output = os.getenv("ALBUM_OUTPUT", "/data/media/music/{artist}/{album} - ({year})/{artist} - {title}.{output-ext}")
        logging.info(f"Album Output: {self.album_output}")

        self.playlist_output = os.getenv("PLAYLIST_OUTPUT", "/data/media/music/{list-name}/{artist} - {title}.{output-ext}")
        logging.info(f"Playlist Output: {self.playlist_output}")

        self.artist_output = os.getenv("ARTIST_OUTPUT", "/data/media/music/{artist}/{album} - ({year})/{artist} - {title}.{output-ext}")
        logging.info(f"Artist Output: {self.artist_output}")

        self.trigger_jellyfin_scan = os.getenv("TRIGGER_JELLYFIN_SCAN", "True")
        logging.info(f"Trigger Jellyfin Scan: {self.trigger_jellyfin_scan}")

        self.trigger_plex_scan = os.getenv("TRIGGER_PLEX_SCAN", "True")
        logging.info(f"Trigger Plex Scan: {self.trigger_plex_scan}")

        self.jellyfin_address = os.getenv("JELLYFIN_ADDRESS", "http://192.168.1.123:8096")
        logging.info(f"Jellyfin Address: {self.jellyfin_address}")

        self.jellyfin_api_key = os.getenv("JELLYFIN_API_KEY", "")
        logging.info(f"Jellyfin API Key entered: {self.jellyfin_api_key != ''}")

        self.plex_address = os.getenv("PLEX_ADDRESS", "http://192.168.1.123:32400")
        logging.info(f"Plex Address: {self.plex_address}")

        self.plex_token = os.getenv("PLEX_TOKEN", "")
        logging.info(f"Plex Token entered: {self.plex_token != ''}")

        self.plex_library_section_id = int(os.getenv("PLEX_LIBRARY_SECTION_ID", "1"))
        logging.info(f"Plex Library Section ID: {self.plex_library_section_id}")

        self.plex_library_name = os.getenv("PLEX_LIBRARY_NAME", "Music")
        logging.info(f"Plex Library Name: {self.plex_library_name}")

        self.generate_m3u_playlist = os.getenv("GENERATE_M3U_PLAYLIST", "True")
        logging.info(f"Generate M3U Playlist: {self.generate_m3u_playlist}")

        self.m3u_playlist_name = os.getenv("M3U_PLAYLIST_NAME", "spotify_singles")
        logging.info(f"Playlist Name: {self.m3u_playlist_name}")

        self.m3u_playlist_path = os.getenv("M3U_PLAYLIST_PATH", "/data/media/music/playlists")
        logging.info(f"Playlist Path: {self.m3u_playlist_path}")

        self.absolute_server_path = os.getenv("ABSOLUTE_SERVER_PATH", "/data/media/music/singles")
        logging.info(f"Absolute Server Path: {self.absolute_server_path}")

        self.supported_formats = {".mp3", ".flac", ".wav", ".aac", ".ogg", ".m4a", ".opus"}
        logging.info(f"Supported Formats: {self.supported_formats}")

        self.extra_logging = os.getenv("EXTRA_LOGGING", "False")
        logging.info(f"Extra Logging: {self.extra_logging}")

        self.search_limit = int(os.getenv("SEARCH_LIMIT", "10"))
        logging.info(f"Spotify Search Limit: {self.search_limit}")

    def get_spotdl_vars(self):
        logging.info("Loading SpotDL Environmental Variables...")

        self.client_id = os.getenv("CLIENT_ID", "5f573c9620494bae87890c0f08a60293")
        logging.info(f"Client ID entered: {self.client_id != ''}")

        self.client_secret = os.getenv("CLIENT_SECRET", "212476d9b0f3472eaa762d90b19b0ba8")
        logging.info(f"Client Secret entered: {self.client_secret != ''}")

        self.auth_token = os.getenv("AUTH_TOKEN", None)
        logging.info(f"Auth Token: {self.auth_token}")

        self.user_auth = os.getenv("USER_AUTH", "False").lower() == "true"
        logging.info(f"User Auth: {self.user_auth}")

        self.headless = os.getenv("HEADLESS", "False").lower() == "true"
        logging.info(f"Headless Mode: {self.headless}")

        self.cache_path = os.getenv("CACHE_PATH", "/home/appuser/.spotdl/.spotipy")
        logging.info(f"Cache Path: {self.cache_path}")

        self.no_cache = os.getenv("NO_CACHE", "True").lower() == "true"
        logging.info(f"No Cache: {self.no_cache}")

        self.output = os.getenv("OUTPUT", "{artists} - {title}.{output-ext}")
        logging.info(f"Output: {self.output}")

        self.format = os.getenv("FORMAT", "mp3")
        logging.info(f"Format: {self.format}")

        self.preload = os.getenv("PRELOAD", "False").lower() == "true"
        logging.info(f"Preload: {self.preload}")

        self.port = int(os.getenv("PORT", 8800))
        logging.info(f"Port: {self.port}")

        self.host = os.getenv("HOST", "localhost")
        logging.info(f"Host: {self.host}")

        self.keep_alive = os.getenv("KEEP_ALIVE", "False").lower() == "true"
        logging.info(f"Keep Alive: {self.keep_alive}")

        self.enable_tls = os.getenv("ENABLE_TLS", "False").lower() == "true"
        logging.info(f"Enable TLS: {self.enable_tls}")

        self.proxy = os.getenv("PROXY", None)
        logging.info(f"Proxy: {self.proxy}")

        self.skip_explicit = os.getenv("SKIP_EXPLICIT", "False").lower() == "true"
        logging.info(f"Skip Explicit: {self.skip_explicit}")

        self.log_level = os.getenv("LOG_LEVEL", "DEBUG")
        logging.info(f"Log Level: {self.log_level}")

        self.restrict_mode = os.getenv("RESTRICT_MODE", "none")
        logging.info(f"Restrict Mode: {self.restrict_mode}")

        self.max_retries = int(os.getenv("MAX_RETRIES", 3))
        logging.info(f"Max Retries: {self.max_retries}")

        self.use_cache_file = os.getenv("USE_CACHE_FILE", "False").lower() == "true"
        logging.info(f"Use Cache File: {self.use_cache_file}")

        self.audio_providers = os.getenv("AUDIO_PROVIDERS", "youtube-music").split(",")
        logging.info(f"Audio Providers: {self.audio_providers}")

        self.lyrics_providers = os.getenv("LYRICS_PROVIDERS", "genius,azlyrics,musixmatch").split(",")
        logging.info(f"Lyrics Providers: {self.lyrics_providers}")

        self.genious_token = os.getenv("GENIOUS_TOKEN", "alXXDbPZtK1m2RrZ8I4k2Hn8Ahsd0Gh_o076HYvcdlBvmc0ULL1H8Z8xRlew5qaG")
        logging.info(f"Genius Token Entered: {self.genious_token!=""}")

        self.playlist_numbering = os.getenv("PLAYLIST_NUMBERING", "False").lower() == "true"
        logging.info(f"Playlist Numbering: {self.playlist_numbering}")

        self.playlist_retain_track_cover = os.getenv("PLAYLIST_RETAIN_TRACK_COVER", "False").lower() == "true"
        logging.info(f"Playlist Retain Track Cover: {self.playlist_retain_track_cover}")

        self.scan_for_songs = os.getenv("SCAN_FOR_SONGS", "False").lower() == "true"
        logging.info(f"Scan for Songs: {self.scan_for_songs}")

        self.m3u = os.getenv("M3U", None)
        logging.info(f"M3U: {self.m3u}")

        self.overwrite = os.getenv("OVERWRITE", "skip")
        logging.info(f"Overwrite: {self.overwrite}")

        self.search_query = os.getenv("SEARCH_QUERY", None)
        logging.info(f"Search Query: {self.search_query}")

        self.ffmpeg = os.getenv("FFMPEG", "ffmpeg")
        logging.info(f"FFmpeg: {self.ffmpeg}")

        self.bitrate = os.getenv("BITRATE", None)
        logging.info(f"Bitrate: {self.bitrate}")

        self.ffmpeg_args = os.getenv("FFMPEG_ARGS", None)
        logging.info(f"FFmpeg Args: {self.ffmpeg_args}")

        self.save_file = os.getenv("SAVE_FILE", None)
        logging.info(f"Save File: {self.save_file}")

        self.filter_results = os.getenv("FILTER_RESULTS", "True").lower() == "true"
        logging.info(f"Filter Results: {self.filter_results}")

        self.threads = int(os.getenv("THREADS", 4))
        logging.info(f"Threads: {self.threads}")

        self.cookie_file = os.getenv("COOKIE_FILE", None)
        logging.info(f"Cookie File: {self.cookie_file}")

        self.print_errors = os.getenv("PRINT_ERRORS", "False").lower() == "true"
        logging.info(f"Print Errors: {self.print_errors}")

        self.sponsor_block = os.getenv("SPONSOR_BLOCK", "False").lower() == "true"
        logging.info(f"Sponsor Block: {self.sponsor_block}")

        self.archive = os.getenv("ARCHIVE", None)
        logging.info(f"Archive: {self.archive}")

        self.load_config = os.getenv("LOAD_CONFIG", "True").lower() == "true"
        logging.info(f"Load Config: {self.load_config}")

        self.simple_tui = os.getenv("SIMPLE_TUI", "False").lower() == "true"
        logging.info(f"Simple TUI: {self.simple_tui}")

        self.fetch_albums = os.getenv("FETCH_ALBUMS", "False").lower() == "true"
        logging.info(f"Fetch Albums: {self.fetch_albums}")

        self.id3_separator = os.getenv("ID3_SEPARATOR", "/")
        logging.info(f"ID3 Separator: {self.id3_separator}")

        self.album_type = os.getenv("ALBUM_TYPE", None)
        logging.info(f"Album Type: {self.album_type}")

        self.restrict = os.getenv("RESTRICT", None)
        logging.info(f"Restrict: {self.restrict}")

        self.ytm_data = os.getenv("YTM_DATA", "False").lower() == "true"
        logging.info(f"YTM Data: {self.ytm_data}")

        self.add_unavailable = os.getenv("ADD_UNAVAILABLE", "False").lower() == "true"
        logging.info(f"Add Unavailable: {self.add_unavailable}")

        self.generate_lrc = os.getenv("GENERATE_LRC", "False").lower() == "true"
        logging.info(f"Generate LRC: {self.generate_lrc}")

        self.force_update_metadata = os.getenv("FORCE_UPDATE_METADATA", "False").lower() == "true"
        logging.info(f"Force Update Metadata: {self.force_update_metadata}")

        self.only_verified_results = os.getenv("ONLY_VERIFIED_RESULTS", "False").lower() == "true"
        logging.info(f"Only Verified Results: {self.only_verified_results}")

        self.sync_without_deleting = os.getenv("SYNC_WITHOUT_DELETING", "False").lower() == "true"
        logging.info(f"Sync Without Deleting: {self.sync_without_deleting}")

        self.max_filename_length = os.getenv("MAX_FILENAME_LENGTH", None)
        logging.info(f"Max Filename Length: {self.max_filename_length}")

        self.yt_dlp_args = os.getenv("YT_DLP_ARGS", None)
        logging.info(f"YT-DLP Args: {self.yt_dlp_args}")

        self.detect_formats = os.getenv("DETECT_FORMATS", None)
        logging.info(f"Detect Formats: {self.detect_formats}")

        self.save_errors = os.getenv("SAVE_ERRORS", None)
        logging.info(f"Save Errors: {self.save_errors}")

        self.ignore_albums = os.getenv("IGNORE_ALBUMS", None)
        logging.info(f"Ignore Albums: {self.ignore_albums}")

        self.log_format = os.getenv("LOG_FORMAT", None)
        logging.info(f"Log Format: {self.log_format}")

        self.redownload = os.getenv("REDOWNLOAD", "False").lower() == "true"
        logging.info(f"Redownload: {self.redownload}")

        self.skip_album_art = os.getenv("SKIP_ALBUM_ART", "False").lower() == "true"
        logging.info(f"Skip Album Art: {self.skip_album_art}")

        self.create_skip_file = os.getenv("CREATE_SKIP_FILE", "False").lower() == "true"
        logging.info(f"Create Skip File: {self.create_skip_file}")

        self.respect_skip_file = os.getenv("RESPECT_SKIP_FILE", "False").lower() == "true"
        logging.info(f"Respect Skip File: {self.respect_skip_file}")

        self.sync_remove_lrc = os.getenv("SYNC_REMOVE_LRC", "False").lower() == "true"
        logging.info(f"Sync Remove LRC: {self.sync_remove_lrc}")

        self.web_use_output_dir = os.getenv("WEB_USE_OUTPUT_DIR", "False").lower() == "true"
        logging.info(f"Web Use Output Dir: {self.web_use_output_dir}")

        self.key_file = os.getenv("KEY_FILE", None)
        logging.info(f"Key File: {self.key_file}")

        self.cert_file = os.getenv("CERT_FILE", None)
        logging.info(f"Cert File: {self.cert_file}")

        self.ca_file = os.getenv("CA_FILE", None)
        logging.info(f"CA File: {self.ca_file}")

        self.allowed_origins = os.getenv("ALLOWED_ORIGINS", None)
        logging.info(f"Allowed Origins: {self.allowed_origins}")

        self.keep_sessions = os.getenv("KEEP_SESSIONS", "False").lower() == "true"
        logging.info(f"Keep Sessions: {self.keep_sessions}")

        self.force_update_gui = os.getenv("FORCE_UPDATE_GUI", "False").lower() == "true"
        logging.info(f"Force Update GUI: {self.force_update_gui}")

        self.web_gui_repo = os.getenv("WEB_GUI_REPO", None)
        logging.info(f"Web GUI Repo: {self.web_gui_repo}")

        self.web_gui_location = os.getenv("WEB_GUI_LOCATION", None)
        logging.info(f"Web GUI Location: {self.web_gui_location}")

        # Create the spotdl_config dictionary
        self.spotdl_config = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "auth_token": self.auth_token,
            "user_auth": self.user_auth,
            "headless": self.headless,
            "cache_path": self.cache_path,
            "no_cache": self.no_cache,
            "max_retries": self.max_retries,
            "use_cache_file": self.use_cache_file,
            "audio_providers": self.audio_providers,
            "lyrics_providers": self.lyrics_providers,
            "genius_token": self.genious_token,
            "playlist_numbering": self.playlist_numbering,
            "playlist_retain_track_cover": self.playlist_retain_track_cover,
            "scan_for_songs": self.scan_for_songs,
            "m3u": self.m3u,
            "output": self.output,
            "overwrite": self.overwrite,
            "search_query": self.search_query,
            "ffmpeg": self.ffmpeg,
            "bitrate": self.bitrate,
            "ffmpeg_args": self.ffmpeg_args,
            "format": self.format,
            "save_file": self.save_file,
            "filter_results": self.filter_results,
            "threads": self.threads,
            "cookie_file": self.cookie_file,
            "print_errors": self.print_errors,
            "sponsor_block": self.sponsor_block,
            "preload": self.preload,
            "archive": self.archive,
            "load_config": self.load_config,
            "log_level": self.log_level,
            "simple_tui": self.simple_tui,
            "fetch_albums": self.fetch_albums,
            "album_type": self.album_type,
            "restrict": self.restrict,
            "id3_separator": self.id3_separator,
            "ytm_data": self.ytm_data,
            "add_unavailable": self.add_unavailable,
            "generate_lrc": self.generate_lrc,
            "force_update_metadata": self.force_update_metadata,
            "only_verified_results": self.only_verified_results,
            "sync_without_deleting": self.sync_without_deleting,
            "max_filename_length": self.max_filename_length,
            "yt_dlp_args": self.yt_dlp_args,
            "detect_formats": self.detect_formats,
            "save_errors": self.save_errors,
            "ignore_albums": self.ignore_albums,
            "proxy": self.proxy,
            "skip_explicit": self.skip_explicit,
            "log_format": self.log_format,
            "redownload": self.redownload,
            "skip_album_art": self.skip_album_art,
            "create_skip_file": self.create_skip_file,
            "respect_skip_file": self.respect_skip_file,
            "sync_remove_lrc": self.sync_remove_lrc,
            "web_use_output_dir": self.web_use_output_dir,
            "port": self.port,
            "host": self.host,
            "keep_alive": self.keep_alive,
            "enable_tls": self.enable_tls,
            "key_file": self.key_file,
            "cert_file": self.cert_file,
            "ca_file": self.ca_file,
            "allowed_origins": self.allowed_origins,
            "keep_sessions": self.keep_sessions,
            "force_update_gui": self.force_update_gui,
            "web_gui_repo": self.web_gui_repo,
            "web_gui_location": self.web_gui_location,
        }

    def create_config_file(self):
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as config_file:
                json.dump(self.spotdl_config, config_file, indent=4)
            logging.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            logging.error(f"Failed to save config file: {e}")
