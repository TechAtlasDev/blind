from .functions import ip, send_dm, graficarfuncion, get_info_user, search, calculadora, cronjobs, web, audio, youtube, pdf

# Proximas funciones:
# Generar pdfs
# Personalizar iamgenes con cloudinary
# Generar audio

functions = {
  "sumar": calculadora.sumar,
  "fetchIPData": ip.fetchIPData,
  "graficar": graficarfuncion.graficar,
  "send_dm": send_dm.send_dm,
  "fetchDataUser": get_info_user.fetchDataUser,
  "google_search": search.google_search,
  "alarma": cronjobs.alarma,
  "visitarURL": web.visitarURL,
  "youtube_obtener_video_transcripcion": youtube.youtube_obtener_video_transcripcion,
  "crear_pdf_html": pdf.crear_pdf_html
  
#  "generar_audio": audio.generar_audio
}