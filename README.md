# stella
Automated generation of variable segment times  for hls via ffmpeg

Want the first 10 seconds of hls segments 2 second long, 
and the rest of the segments 4 seconds long? 

Try this.

### Usage:

```sh
python3 stella.py video.file
```

```
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-MEDIA-SEQUENCE:0
#EXT-X-ALLOW-CACHE:YES
#EXT-X-TARGETDURATION:5
#EXTINF:2.035367,
000.ts
#EXTINF:2.002000,
001.ts
#EXTINF:2.002000,
002.ts
#EXTINF:2.002000,
003.ts
#EXTINF:2.002000,
004.ts
#EXTINF:4.004000,
005.ts
#EXTINF:4.004000,
006.ts
#EXTINF:4.004000,
007.ts
#EXTINF:4.004000,
008.ts
#EXT-X-ENDLIST
```

### Want to tune it a bit ?

Adjust pre_stop and pre_segment_time for the initial segments,
and reg_segment_time for the rest of the segments in main


```python

if __name__=='__main__':

	media_file = sys.argv[1]
	# first ten seconds get 2 second sgments
	pre_stop =10
	pre_segment_time = 2
  	# other segments are 4 seconds
	reg_segment_time = 4
```
