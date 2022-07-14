from genericpath import isdir
from bs4 import BeautifulSoup
import os
import subprocess
import shutil
from pathlib import Path
from glob import glob

def getLyrics():
    def deleteHTML(): 
        # Delete HTML file and folder
        os.remove(webpage)
        shutil.rmtree(f"{webpage[0:-5]}_files")

    # Find the first HTML in Downloads folder
    downloadsPath = str(Path.home() / "Downloads")
    downloadsPath = os.path.abspath(downloadsPath)
    htmlFiles = glob(f"{downloadsPath}/*.html")
    if (htmlFiles == []):
        print("There are no HTML files in your Downloads folder!")
        return
    htmlFile = sorted(htmlFiles, key=os.path.getmtime)[-1]
    webpage = htmlFile
    
    # Parse HTML, then delete
    with open(webpage, "r", encoding="utf-8") as f:
        doc = BeautifulSoup(f, "html.parser")
    deleteHTML()

    # Check if lyrics exist
    lyrics = doc.findAll(class_ = "NHVfxGs2HwmI_fly2JC4")
    if lyrics == []:
        print("Lyrics don't exist!")
        return None

    # Store lyrics (without empty elements)
    lyricsText = ""
    for i, lyric in enumerate(lyrics):
        if lyrics[i].text != "":
            lyricsText += lyrics[i].text + "\n"
    lyrics = lyricsText[0:-1]  # Removing last line-ending

    # Store lyrics in a text file
    if not os.path.isdir("lyrics"):
        os.mkdir("lyrics")
    fileName = os.path.basename(webpage)[0:-5]
    lyricsPath = os.path.abspath(f"lyrics/{fileName}.txt")
    with open(lyricsPath, "w", encoding="utf-8") as f:
        f.write(lyrics)

    # Open in explorer
    subprocess.Popen(f'explorer /select,"{lyricsPath}"')

    return lyrics

if __name__ == "__main__":
    print(getLyrics())