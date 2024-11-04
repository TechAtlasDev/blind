from .functions import ip, send_dm, graficarfuncion, get_info_user, search, calculadora

# Proximas funciones:
# Notificaciones
# Generar pdfs
# Generar audio

functions = {
  "sumar": calculadora.sumar,
  "fetchIPData": ip.fetchIPData,
  "graficar": graficarfuncion.graficar,
  "send_dm": send_dm.send_dm,
  "fetchDataUser": get_info_user.fetchDataUser,
#  "google_search": search.google_search
}