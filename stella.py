#!/usr/bin/env python3

import sys,re,subprocess

#Duration: 00:01:09.06
redur=re.compile(r'Duration\: (\d{2}:\d{2}:\d{2}\.\d{2})')

def found_to_seconds(found):
	hours,mins,secs=found[0].split(':')
	seconds=float(secs)+(int(mins)*60)+(int(hours)*360)
	print('media duration ',seconds)
	return seconds


def find_time(pdata):
	found=redur.findall(pdata)
	if found: return found_to_seconds(found)
	return 0


def probe_media_for_seconds(media_file):
	ffprobe_args=['ffprobe', media_file]
	pdata=subprocess.Popen(ffprobe_args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()[0].decode('utf-8')
	total_seconds=find_time(pdata)
	return total_seconds


def mk_segments_times(start,stop,seg_time):
	while start < stop:
		if (start+ seg_time) < stop: start+=seg_time
		else: start+=(stop -start)
		segment_times.append(start)
	return stop


def stringify(alist):
	return str(alist)[1:-1].replace(" ","")


def mk_segments(media_file,segment_times,key_frames):
	args=['ffmpeg','-y','-v','0','-hide_banner', '-i', media_file, '-map', '0', '-copy_unknown',
		'-c', 'copy', '-f', 'segment', '-segment_times',stringify(segment_times),
		'-force_key_frames', stringify(key_frames), '-segment_list', 'index.m3u8', '%03d.ts']
	subprocess.call(args)


if __name__=='__main__':
	media_file = sys.argv[1]
	# first ten seconds get 2 second sgments
	pre_stop =10
	pre_segment_time = 2
  	# other segments are 4 seconds
	reg_segment_time = 4
	segment_times=[]
	stop = probe_media_for_seconds(media_file)
	start=0
	current_time=mk_segments_times(start,pre_stop,pre_segment_time)
	mk_segments_times(current_time,stop,reg_segment_time)
	# pop off the last time in segment_times, it's the end of the video
	segment_times.pop()
	# copy segment_times for forced key frames
	key_frames=segment_times
	print('segment times set to ',stringify(segment_times))
	# generate segments and index.m3u8
	mk_segments(media_file,segment_times,key_frames)
