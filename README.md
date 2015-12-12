# Sopcast Launcher
Sopcast Launcher allows you to open Sopcast links with a Media Player of your choice

## Dependencies
    python, python-psutil, python-notify2, sopcast

## Usage
    sopcast-launcher URL [--localport PORT] [--playerport PORT] [--player PLAYER] [--engine-path PATH]

## Positional arguments
    URL                       The sopcast url to play

## Optional arguments
    -h, --help                  Show this help message and exit
    --localport LOCALPORT       The local port to use (default: 3000)
    --playerport PLAYERPORT     The player port to use (default: 3001)
    --player PLAYER             The media player to use (default: vlc)
    --engine-path ENGINE_PATH   The sopcast engine executable to use (default: system)

## Installation
Arch Linux: [AUR Package](https://aur.archlinux.org/packages/sopcast-launcher)
