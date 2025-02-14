from .functions import ip, send_dm, graficarfuncion, get_info_user, search, calculadora, web, audio, youtube, pdf, shodan
from .functions.cronjobs import temporizador, rutine

# Proximas funciones:
# Personalizar imágenes con cloudinary

functions = {
  "sumar": calculadora.sumar,
  "fetchIPData": ip.fetchIPData,
  "graficar": graficarfuncion.graficar,
  "send_dm": send_dm.send_dm,
  "fetchDataUser": get_info_user.fetchDataUser,
  "google_search": search.google_search,
  "temporizador": temporizador.temporizador,
  
  "crear_rutina": rutine.crear_rutina,
  "olvidar_rutina": rutine.olvidar_rutina,
  "listar_rutinas": rutine.listar_rutinas,
  "modificar_rutina": rutine.modificar_rutina,

  "visitarURL": web.visitarURL,
  "youtube_obtener_video_transcripcion": youtube.youtube_obtener_video_transcripcion,
  "crear_pdf_html": pdf.crear_pdf_html,

  "searchShodan": shodan.searchShodan,
}