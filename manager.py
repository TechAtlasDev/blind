import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time

class ReloadBotHandler(FileSystemEventHandler):
    def __init__(self, script_name):
        self.script_name = script_name
        self.process = None
        self.start_bot()

    def start_bot(self):
        # Inicia el bot en un proceso separado
        if self.process:
            self.process.kill()
        self.process = subprocess.Popen(["python3", "-m", self.script_name])

    def on_modified(self, event):
        # Reinicia el bot al detectar cambios
        if event.src_path.endswith(".py"):
            print(f"Detectado cambio en {event.src_path}. Reiniciando bot...")
            self.start_bot()

    def stop_bot(self):
        if self.process:
            self.process.kill()

if __name__ == "__main__":
    script_name = "src.main"  # Cambia esto al nombre de tu script principal
    event_handler = ReloadBotHandler(script_name)
    observer = Observer()
    observer.schedule(event_handler, path="./src", recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        event_handler.stop_bot()
        observer.stop()
    observer.join()