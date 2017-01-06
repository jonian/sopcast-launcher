# Sopcast Launcher
Sopcast Launcher allows you to open Sopcast links with a Media Player of your choice

## Dependencies
    python, python-psutil, python-notify2, sopcast

## Usage
    sopcast-launcher URL [--player PLAYER] [--engine ENGINE] [--localport PORT] [--playerport PORT]

## Positional arguments
    URL                      The sopcast url to play

## Optional arguments
    -h, --help               Show this help message and exit
    -p, --player PLAYER      The media player command to use (default: vlc)
    -e, --engine ENGINE      The engine command to use (default: sp-sc)
    --localport PORT         The local port to use (default: 3000)
    --playerport PORT        The player port to use (default: 3001)

## Installation
Arch Linux: [AUR Package](https://aur.archlinux.org/packages/sopcast-launcher)
