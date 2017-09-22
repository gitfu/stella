# stella
Automated generation of variable segment times  for hls via ffmpeg

## Want the first 10 seconds of hls segments 2 second long, and the rest of the segments 4 seconds long? Try this.

```python

if __name__=='__main__':

	media_file = sys.argv[1]
	# first ten seconds get 2 second sgments
	pre_stop =10
	pre_segment_time = 2
  	# other segments are 4 seconds
	reg_segment_time = 4
```
