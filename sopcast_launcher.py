#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Sopcast Launcher: Open sopcast links with any media player"""

import sys
import time
import socket
import argparse
import psutil
import notify2

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
            help='the sopcast url to play'
        )
        parser.add_argument(
            '-e', '--engine',
            help='the sopcast engine command to use (default: sp-sc)',
            default='sp-sc'
        )
        parser.add_argument(
            '-p', '--player',
            help='the media player command to use (default: vlc)',
            default='vlc'
        )
        parser.add_argument(
            '--localport',
            help='the local port to use (default: 3000)',
            default='3000'
        )
        parser.add_argument(
            '--playerport',
            help='the player port to use (default: 3001)',
            default='3001'
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
            'noengine': 'Sopcast engine not found in provided path!',
            'unavailable': 'Sopcast channel unavailable!'
        }

        print(messages[message])
        self.notifier.update(self.appname, messages[message], icon)
        self.notifier.show()

    def start_sopcast(self):
        """Start sopcast service"""

        self.url = 'http://localhost:' + self.args.playerport + '/sopcast.mp4'

        for process in psutil.process_iter():
            if 'sp-sc' in process.name():
                process.kill()

        try:
            engine_args = self.args.engine.split()
            engine_args.append(self.args.url)
            engine_args.append(self.args.localport)
            engine_args.append(self.args.playerport)

            self.sopcast = psutil.Popen(engine_args)
            self.notify('running')
            time.sleep(5)
        except FileNotFoundError:
            self.notify('noengine')
            self.close_player(1)

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

        player_args = self.args.player.split()
        player_args.append(self.url)

        self.player = psutil.Popen(player_args)
        self.player.wait()

    def close_player(self, code=0):
        """Close sopcast and media player"""

        try:
            self.player.kill()
        except (AttributeError, psutil.NoSuchProcess):
            print('Media Player not running...')

        try:
            self.sopcast.kill()
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
