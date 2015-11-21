#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Sopcast Launcher: Open sopcast links with any media player"""

import sys
import time
import socket
import psutil
import notify2
import argparse

class SopcastLauncher(object):
    """Sopcast Launcher"""

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

        self.appname = 'Sopcast Launcher'
        self.args = parser.parse_args()

        notify2.init(self.appname)
        self.notifier = notify2.Notification(self.appname)

        self.start_sopcast()
        self.start_session()
        self.start_player()
        self.close_player()

    def notify(self, message):
        """Show player status notifications"""

        icon = self.args.player
        messages = {
            'running': 'Sopcast engine running.',
            'started': 'Streaming started. Launching player.',
            'waiting': 'Waiting for channel response...',
            'unavailable': 'Sopcast channel unavailable!',
            'terminated': 'Sopcast engine terminated.'
        }

        print(messages[message])
        self.notifier.update(self.appname, messages[message], icon)
        self.notifier.show()

    def start_sopcast(self):
        """Start sopcast service"""

        for process in psutil.process_iter():
            if 'sp-sc' in process.name():
                process.kill()

        sopurl = self.args.url
        localport = self.args.localport
        playerport = self.args.playerport

        self.url = 'http://localhost:' + playerport + '/sopcast.mp4'

        self.sopcast = psutil.Popen(['sp-sc', sopurl, localport, playerport])
        self.notify('running')
        time.sleep(5)

    def start_session(self):
        """Start sopcast socket session"""

        self.notify('waiting')
        time.sleep(25)

        try:
            session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            session.settimeout(30)
            session.connect(('localhost', int(self.args.playerport)))
            session.close()
            self.notify('started')
        except socket.error:
            self.notify('unavailable')
            self.close_player(1)

    def start_player(self):
        """Start the media player"""

        self.player = psutil.Popen([self.args.player, self.url])
        self.player.wait()

    def close_player(self, code=0):
        """Close sopcast and media player"""

        try:
            self.player.kill()
        except (AttributeError, psutil.NoSuchProcess):
            print('Media Player not running...')

        try:
            self.sopcast.kill()
            self.notify('terminated')
        except (AttributeError, psutil.NoSuchProcess):
            print('Sopcast not running...')

        sys.exit(code)

def main():
    """Start Sopcast Launcher"""

    try:
        SopcastLauncher()
    except (KeyboardInterrupt, EOFError):
        print('Sopcast Launcher exiting...')

        for process in psutil.process_iter():
            if 'sp-sc' in process.name():
                process.kill()

        sys.exit(0)

main()
