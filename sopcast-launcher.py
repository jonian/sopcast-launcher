#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import time
import psutil
import argparse

class SopcastLauncher(object):
    """Sopcast Launcher: Open sopcast links with any media player"""

    def __init__(self):
        parser = argparse.ArgumentParser(
            prog='sopcast-launcher',
            description='Open sopcast links with any media player'
        )
        parser.add_argument(
            'url',
            metavar='URL',
            help='The sopcast url to play'
        )
        parser.add_argument(
            '--localport',
            help='The local port to use (default: 3000)',
            default='3000'
        )
        parser.add_argument(
            '--playerport',
            help='The player port to use (default: 3001)',
            default='3001'
        )
        parser.add_argument(
            '--player',
            help='The media player to use (default: vlc)',
            default='vlc'
        )

        self.args = parser.parse_args()

        self.start_sopcast()
        self.start_player()
        self.close_player()

    def start_sopcast(self):
        """Start sopcast service"""

        sopurl = self.args.url
        localport = self.args.localport
        playerport = self.args.playerport

        self.url = 'http://localhost:' + playerport

        self.sopcast = psutil.Popen(['sp-sc', sopurl, localport, playerport])
        time.sleep(5)

    def start_player(self):
        """Start the media player"""

        self.player = psutil.Popen([self.args.player, self.url])
        self.player.wait()

    def close_player(self):
        """Close sopcast and media player"""

        try:
            self.player.terminate()
        except (AttributeError, psutil.NoSuchProcess):
            print('Media Player not running...')

        try:
            self.sopcast.terminate()
        except (AttributeError, psutil.NoSuchProcess):
            print('Sopcast not running...')

        sys.exit(0)

def main():
    """Start Sopcast Launcher"""

    try:
        SopcastLauncher()
    except (KeyboardInterrupt, EOFError):
        print('Sopcast Launcher exiting...')

        for process in psutil.process_iter():
            if 'sp-sc' in process.name():
                process.terminate()

        sys.exit(0)

main()
