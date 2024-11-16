# Funcion que verifica si el repositorio local está actualizado en base al repositorio remoto
import git

def is_updated(link_repo_remote:str="https://github.com/techatlasdev/blind", path_repo_local="."):
  # Inicializar el repositorio local
  repo = git.Repo(path_repo_local)

  # Obtener el remoto
  remote = repo.remote()

  # Obtener el hash del último commit del remoto
  remote_head = remote.refs.main.commit

  # Obtener el hash del último commit local
  local_head = repo.head.commit

  # Comparar los hashes
  if remote_head.hexsha == local_head.hexsha:
      response = {
         "status": True,
         "message": "El repositorio está actualizado",
         "data": {
            "remote_head": remote_head.hexsha,
            "local_head": local_head.hexsha
         }
      }
      return response
  else:
      response = {
         "status": False,
         "message": "El repositorio no está actualizado",
         "data": {
            "remote_head": remote_head.hexsha,
            "local_head": local_head.hexsha
         }
      }
      return response