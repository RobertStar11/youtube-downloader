from flask import Flask, request, render_template, send_file, redirect, url_for
import yt_dlp as youtube_dl
import re
import os
from io import BytesIO

app = Flask(__name__)

# Función para limpiar la URL
def limpiar_url(url):
    return re.sub(r'&list=[^&]+', '', url)

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para procesar la descarga del video
@app.route('/download', methods=['POST'])
def download_video():
    url = request.form.get('url')
    url = limpiar_url(url)
    
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(title)s.%(ext)s',
        }
        
        # Usamos un buffer en memoria para el archivo
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
            ydl.download([url])
        
        file_name = f"{video_title}.mp4"
        
        # Comprobamos que el archivo se descargó
        if os.path.exists(file_name):
            return send_file(file_name, as_attachment=True)
        else:
            return "Error al descargar el video", 500

    except Exception as e:
        return f"Ocurrió un error: {e}", 500

# Ejecutar la app
if __name__ == '__main__':
    app.run(debug=True)
