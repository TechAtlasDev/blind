import git

def is_updated(link_repo_remote="https://github.com/TechAtlasDev/blind", path_repo_local="."):
    try:
        # Inicializar el repositorio local
        repo = git.Repo(path_repo_local)

        # Obtener la URL del remoto
        remote_url = repo.remotes.origin.url

        # Verificar que la URL del remoto coincida con la proporcionada
        if remote_url != link_repo_remote:
            return {
                "status": False,
                "message": f"El repositorio remoto no coincide. Esperado: {link_repo_remote}, pero se encontró: {remote_url}",
            }

        # Verificar si la rama local es 'main'
        if repo.active_branch.name != "main":
            print("Cambiando a la rama 'main'...")
            repo.git.checkout("main")

        # Obtener el remoto
        remote = repo.remote()

        # Actualizar información del remoto
        remote.fetch()

        # Obtener los commits más recientes
        remote_head = remote.refs["main"].commit
        local_head = repo.head.commit

        # Comparar los commits
        if remote_head.hexsha == local_head.hexsha:
            return {
                "status": True,
                "message": "El repositorio está actualizado",
                "data": {
                    "remote_head": remote_head.hexsha,
                    "local_head": local_head.hexsha,
                },
            }
        else:
            return {
                "status": False,
                "message": "El repositorio no está actualizado",
                "data": {
                    "remote_head": remote_head.hexsha,
                    "local_head": local_head.hexsha,
                },
            }

    except Exception as e:
        return {
            "status": False,
            "message": f"Error al verificar el repositorio: {e}",
        }
