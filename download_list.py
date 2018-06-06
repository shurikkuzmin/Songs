from __future__ import unicode_literals 
import youtube_dl
import pandas as pd
import os
import traceback

savedir = "music"
if not os.path.exists(savedir):
    os.makedirs(savedir)

def make_savepath(artist, title, savedir=savedir):
    return os.path.join(savedir, "%s--%s.mp3" % (artist, title))

options = {
    'format': 'bestaudio/best', # choice of quality
    'extractaudio' : True,      # only keep the audio
    'audioformat' : "mp3",      # convert to mp3 
    'outtmpl': '%(id)s',        # name the file the ID of the video
    'noplaylist' : True,}       # only download single song, not playlist

ydl = youtube_dl.YoutubeDL(options)


with ydl:
    music_list = pd.read_csv("list.csv")

    for numrow,row in music_list.iterrows():
        savepath = make_savepath(row.Author.replace(' ','_'), row.Name.replace(' ','_'))

        try:
            os.stat(savepath)
            print("%s already downloaded, continuing..." % savepath)
            continue

        except OSError:
            try:
                result = ydl.extract_info(row.Video, download=True)
                os.rename(result['id'], savepath)
                print("Downloaded and converted %s successfully!" % savepath)

            except Exception as e:
                print("Can't download audio! %s \n" % traceback.format_exc())
                
