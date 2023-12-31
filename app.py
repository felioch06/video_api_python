from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os

import moviepy.editor as mp
import json

app = Flask(__name__)
CURRENT_DIRECTORY = os.getcwd()
port = 4000
debug = True

CORS(app)

@app.get('/')
def index():
  return CURRENT_DIRECTORY
  
@app.post('/video/v2')
def video():
  body = request.form
  
  # Data Body
  options = json.loads(body.get('options'))
  photo = request.files['file']
  video = request.files['video']

  photo.save(CURRENT_DIRECTORY+'/images/'+photo.filename) 
  video.save(CURRENT_DIRECTORY+'/videos/'+video.filename) 

  generarVideo(
    srcImagen=photo.filename, 
    srcVideo=video.filename, 
    options=options
  )
  
  return send_file('./output/testFinal.mp4', as_attachment=True)

def generarVideo(srcVideo, srcImagen, options):
  VIDEO_FPS = 25
  VIDEO_CODEC = 'libx264'
  
  video = mp.VideoFileClip(CURRENT_DIRECTORY+'/videos/'+srcVideo)
  image = mp.ImageClip(CURRENT_DIRECTORY+'/images/'+srcImagen)

  images = [video]
  for opt in options:
    img = (image.resize(height=int(opt["size"]))
            .set_duration(video.duration)
            .set_start(opt["start"])
            .set_end(opt["end"])
            .set_position((int(opt["positionX"]), int(opt["positionY"])), relative= False)
            # .fx(mp.vfx.rotate, lambda t: 90*t, expand = False)
            # .fx(mp.vfx.rotate, 45, unit='deg')
            )
    
    images.append(img)

  videoFinal = mp.CompositeVideoClip(images)
  videoFinal.subclip(0,video.duration).write_videofile(CURRENT_DIRECTORY+"/output/testFinal.mp4",fps=VIDEO_FPS, codec=VIDEO_CODEC, verbose=False)

  return jsonify({"status": True})

if __name__ == '__main__':
  app.run(debug=debug, port=port)