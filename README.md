# Sopcast Launcher
Sopcast Launcher allows you to open Sopcast links with a Media Player of your choice

## Dependencies
    python, python-psutil, python-pexpect, python-notify, sopcast

## Usage
    sopcast-launcher [--localport LOCALPORT] [--playerport PLAYERPORT] [--player PLAYER] URL

## Positional arguments
    URL                       The sopcast url to play

## Optional arguments
    -h, --help                show this help message and exit
    --localport LOCALPORT     The local port to use (default: 3000)
    --playerport PLAYERPORT   The player port to use (default: 3001)
    --player PLAYER           The media player to use (default: vlc)
