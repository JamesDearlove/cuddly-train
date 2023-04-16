import re
from pydub import AudioSegment

MATCH = "(\d{1,2}):(\d{2}) (.+)"

print("Loading input audio")
song = AudioSegment.from_file("input/input.m4a", "m4a")

timestamps = []

print("Parsing timestamps")
with open('input/timestamps.txt') as f:
  contents = f.read()
  timestamps = re.findall(MATCH, contents)

location = 0
workingTitle = ""
trackNumber = 1

for minute, second, title in timestamps:
  if workingTitle != "":
    print(f"Processing {trackNumber}: {workingTitle}")
    newLocation = 1000 * (int(minute) * 60 + int(second))
    segment = song[location:newLocation]
    segment.export(f"output/Track {trackNumber}.m4a", format="mp4", tags={'title': workingTitle})
      
    location = newLocation
    trackNumber += 1

  workingTitle = title

# end
print(f"Processing {trackNumber}: {workingTitle}")
segment = song[location:]
segment.export(f"output/Track {trackNumber}.m4a", format="mp4", tags={'title': workingTitle}) 

print("Done!")
