#!/bin/sh

# ASCII Art
echo "-----------------------------------------------------------"
echo "  SSSSS  PPPPP   OOO   TTTTT   SSSSS  PPPPP   OOO   TTTTT"
echo "  S      P   P  O   O    T     S      P   P  O   O    T   "
echo "  SSSSS  PPPPP  O   O    T     SSSSS  PPPPP  O   O    T   "
echo "     S   P      O   O    T        S   P      O   O    T   "
echo "  SSSSS  P       OOO     T     SSSSS  P       OOO     T   "
echo "-----------------------------------------------------------"
echo "SPOTSPOT - Spotify Downloader using spotDL"
echo -e "\e[1;32mDesigned by MattBlackOnly\e[0m" 
echo "-----------------------------------------------------------"

# Log versions
if [ -z "$SPOTSPOT_VERSION" ]; then
    echo "SPOTSPOT_VERSION environment variable is not set."
else
    echo "SpotSpot version: ${SPOTSPOT_VERSION}"
fi

if [ -f "requirements.txt" ]; then
    YT_DLP_VERSION=$(awk -F'==' '/yt_dlp\[default\]/{print $2}' requirements.txt)
    if [ -z "$YT_DLP_VERSION" ]; then
        echo "yt-dlp version not found in requirements.txt"
    else
        echo "yt-dlp version: $YT_DLP_VERSION"
    fi
else
    echo "requirements.txt not found."
fi

spotdl_version=$(spotdl --version 2>&1)
echo "SpotDL version: $spotdl_version"


# Default values for PUID and PGID
PUID=${PUID:-1000}
PGID=${PGID:-1000}

echo "Using PUID=${PUID} and PGID=${PGID}"

# Modify the appuser and appgroup to match PUID and PGID
if [ "$(id -u appuser)" != "$PUID" ] || [ "$(id -g appuser)" != "$PGID" ]; then
    echo "Updating UID and GID for appuser to match PUID:PGID..."
    deluser appuser
    addgroup -g "$PGID" appgroup
    adduser -D -u "$PUID" -G appgroup appuser
fi

# Ensure correct ownership
echo "Setting up directories..."
chown -R appuser:appgroup /config /data /home/appuser/.spotdl/.spotipy 
chmod -R 777 /config /home 

# Start the application as appuser
echo "Starting SpotSpot..."
exec su-exec appuser:appgroup gunicorn spotspot.spotspot:app -c start_app.py
