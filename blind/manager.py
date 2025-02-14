import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time

import os, re

class BotHandler(FileSystemEventHandler):
    def __init__(self, script_name):
        self.script_name = script_name
        self.process = None

        # Limpiando caché
        self._clear_cache()
        self.start_bot()

    def start_bot(self):
        if self.process:
            self.process.kill()
        self.process = subprocess.Popen(["python3", "-m", self.script_name])

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"Cambio detectado en {event.src_path}. Reiniciando bot...")
            self.start_bot()

    def stop_bot(self):
        if self.process:
            self.process.kill()

    @staticmethod
    def _clear_cache():
        """
        Funcion que elimina los archivos que tienen el patron: <name_bot>.session<opcional>
        """
        for root, dirs, files in os.walk("."):
            for file in files:
                if re.search(r"\.session", file):
                    os.remove(os.path.join(root, file))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", action="store_true", help="Modo desarrollo (auto-reload)")
    args = parser.parse_args()

    script_name = "blind.src.main"
    bot_handler = BotHandler(script_name)

    if args.dev:
        print("Modo desarrollo activado (con auto-reload)")
        observer = Observer()
        observer.schedule(bot_handler, path="./blind", recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Deteniendo el bot...")
            bot_handler.stop_bot()
            observer.stop()
            observer.join()
    else:
        print("Modo producción activado")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Deteniendo el bot...")
            bot_handler.stop_bot()