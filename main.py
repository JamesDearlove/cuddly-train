import re
from pydub import AudioSegment

from mutagen.mp4 import MP4
from mutagen.m4a import M4ACover

MATCH = "(\d{1,2}):(\d{2}) (.+)"

ARTIST_NAME = ""
ALBUM_NAME = ""
ALBUM_ARTIST = ""
YEAR = 2023

COVER_ART = "input/coverart.png"
loaded_art = open(COVER_ART, 'rb').read()
formattedArt = M4ACover.FORMAT_PNG if COVER_ART.endswith('png') else M4ACover.FORMAT_JPEG

print("Loading input audio")
song = AudioSegment.from_file("input/input.m4a", "m4a")

timestamps = []

print("Parsing timestamps")
with open('input/timestamps.txt') as f:
  contents = f.read()
  timestamps = re.findall(MATCH, contents)

location = 0

for index in range(len(timestamps)):
  _, _, title = timestamps[index]
  trackNo = index + 1
  print(f"Processing {trackNo}: {title}")

  if index + 1 >= len(timestamps):
    newLocation = len(song)
  else:
    minute, second, _ = timestamps[index + 1]
    newLocation = 1000 * (int(minute) * 60 + int(second))

  # Metadata tags
  tags = {'title': title, 'artist': ARTIST_NAME, 'album': ALBUM_NAME, 'track': trackNo }

  # Split the main loaded file and export it
  segment = song[location:newLocation]
  fileName = f"output/Track {trackNo}.m4a"
  segment.export(fileName, format="mp4", tags=tags)
  
  # And now to embed the album art
  exportedFile = MP4(fileName)
  exportedFile.tags['covr'] = [M4ACover(loaded_art, formattedArt)]
  exportedFile.save()

  location = newLocation

print("Done!")
