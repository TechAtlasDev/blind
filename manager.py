import argparse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time
import threading

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

def check_repo_updates(interval=30):
    """Verifica periódicamente si el repositorio está actualizado cada cierto intervalo."""
    from src.utils.repo import is_updated
    while True:
        repo_status = is_updated()
        printTest(repo_status)
        if not repo_status["status"]:
            print("El repositorio no está actualizado. Actualizando...")
            subprocess.run(["git", "pull"])
            print("Repositorio actualizado. Reiniciando bot...")
            reload_handler.start_bot()
        else:
            print ("[INFO-SYSTEM 5] Sistema actualizado")
        time.sleep(interval)

if __name__ == "__main__":
    # Modo producción -> Parámetro --prod
    parser = argparse.ArgumentParser()
    parser.add_argument("--prod", action="store_true", help="Modo de producción")
    parser.add_argument("--dev", action="store_true", help="Modo de desarrollo")
    args = parser.parse_args()

    if args.prod:
        print ("Produccion")
        # Modo de producción
        try:
            from src.utils.repo import is_updated
            from src.utils.utilities import printTest

            # Verifica si el repositorio está actualizado
            repo_status = is_updated()
            printTest(repo_status)

            # Sistema actualizado
            if repo_status:
                print("El repositorio está actualizado. Ejecutando bot en modo producción...")
                reload_handler = ReloadBotHandler("src.main")
                
                # Inicia el hilo para verificar actualizaciones periódicas
                update_thread = threading.Thread(target=check_repo_updates)
                update_thread.daemon = True
                update_thread.start()

                # Mantiene el script corriendo en producción
                while True:
                    time.sleep(1)

            # Sistema desactualizado
            else:
                print("El repositorio no está actualizado. Realizando 'git pull'...")
                subprocess.run(["git", "pull"])
                print("Repositorio actualizado. Ejecutando bot en modo producción...")
                reload_handler = ReloadBotHandler("src.main")

                # Inicia el hilo para verificar actualizaciones periódicas
                update_thread = threading.Thread(target=check_repo_updates)
                update_thread.daemon = True
                update_thread.start()

                # Mantiene el script corriendo en producción
                while True:
                    time.sleep(1)

        except ImportError as e:
            print(f"Error de importación: {e}. Asegúrate de que las dependencias están correctamente configuradas.")
        except Exception as e:
            print(f"Error en modo producción: {e}")


    # Modo de desarrollo
    if args.dev:
        print (f"Sistema en modo desarrollo activado")
        script_name = "src.main"
        event_handler = ReloadBotHandler(script_name)
        observer = Observer()
        observer.schedule(event_handler, path="./src", recursive=True)
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Interrumpido manualmente. Deteniendo el bot...")
            event_handler.stop_bot()
            observer.stop()
        observer.join()
