import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time

class BotHandler(FileSystemEventHandler):
    def __init__(self, script_name):
        self.script_name = script_name
        self.process = None
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