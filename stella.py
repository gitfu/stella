#!/usr/bin/env python3

import sys,re,subprocess

#Duration: 00:01:09.06
redur=re.compile(r'Duration\: (\d{2}:\d{2}:\d{2}\.\d{2})')


def found_to_seconds(found):
	'''
	convert string in the format
	00:01:09.06 to seconds
	'''
	hours,mins,secs=found[0].split(':')
	found_seconds=float(secs)
	found_seconds+=(int(mins)*60)
	found_seconds+=(int(hours)*360)
	return found_seconds


def find_time(pdata):
	'''
	regex out duration time
	'''
	found=redur.findall(pdata)
	if found:
		return found_to_seconds(found)
	return 0


def probe_media_for_seconds(media_file):
	'''
	run ffprobe in subprocess to find duration
	'''
	ffprobe_args=['ffprobe', media_file]
	stdout=subprocess.PIPE
	stderr=subprocess.STDOUT
	pdata=subprocess.Popen(ffprobe_args,stdout=stdout,stderr=stderr).communicate()[0].decode('utf-8')
	total_seconds=find_time(pdata)
	return total_seconds


def mk_stage_segments(current_time,seg_stop,seg_time):
	'''
	generates segment times for a stage of segments
	and adjusts last segment to fit if needed
	ex:  to have the first 13 seconds in 2 second segments
			call:
			 mk_stage_segments(0,13,2)
			to add:
				2,4,6,8,10,12,13
			to the segment_times list
	'''

	while current_time < seg_stop:

		if (current_time+ seg_time) < seg_stop:current_time+=seg_time
		else: current_time+=(seg_stop -current_time)

		segment_times.append(current_time)
	return current_time


def stringify(alist):
	'''
	segment_times must be passed to ffmpeg as a string, without spaces
	'''
	return str(alist)[1:-1].replace(" ","")


def mk_segments(media_file,segment_times,key_frames):
	'''
	segments and inserts key frames at the start of each segment.
	No encoding is performed, all streams are mapped and codecs are copied
	'''
	args=['ffmpeg','-y','-hide_banner', '-i', media_file, '-map', '0', '-copy_unknown',
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

	total_seconds = probe_media_for_seconds(media_file)

	current_time=0
	current_time=mk_stage_segments(current_time,pre_stop,pre_segment_time)
	current_time=mk_stage_segments(current_time,total_seconds,reg_segment_time)
	# copy segment_times for forced key frames
	key_frames=segment_times
	# generate segments and index.m3u8
	mk_segments(media_file,segment_times,key_frames)



