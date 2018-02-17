'''
REQUIREMENTS

youtube-dl
ffmpeg
'''

import sys
import os
import json
import subprocess
import argparse

path_slash = "\\" if os.name == 'nt' else "/"

videos_file = "vids.json"
downloads_folder = "downloaded"
output_folder = "cutted"
frames_folder = "frames"

parser = argparse.ArgumentParser()
parser.add_argument(
	'--ignore-keyframes', 
	action="store_true", 
	default=False, 
	help="with this option you might lose a few frames at the beginning of the cut but you will gain speed in cutting videos"
	)
parser.add_argument(
	'--extract-frames', 
	action="store_true", 
	default=False, 
	help="if you just want all the videos in the \"{}\" to be splitted into frames (default framerate 5)".format(output_folder)
	)
parsed_arguments = parser.parse_args(sys.argv[1:])
ignore_keyframes = getattr(parsed_arguments, 'ignore_keyframes')
extract_frames = getattr(parsed_arguments, 'extract_frames')

data = None

def parse_vids_file() :
	global data
	data = json.load(open(videos_file))

def create_diectory(directory) :
	if not os.path.exists(directory):
		os.makedirs(directory)

def exec_command(command) :
	print("Executing command: {}".format(command))
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	process.wait()
	return process.returncode

def download_video(url, output_name) :
	print("Downloading video {} ...".format(url))
	return exec_command("youtube-dl {} -f bestvideo[ext=mp4]/mp4+bestaudio --output \"{}\" --max-downloads=1".format(url, output_name))

def cut_video(video_path, start, end, output_path) :
	print("Cutting video {0} start: {1}, end: {2} ouput {3}".format(video_path, start, end, output_path))
	ignore_keyframes_command = ""
	if ignore_keyframes :
		ignore_keyframes_command = "-c copy"
	return exec_command("ffmpeg -i {0} {4} -ss {1} -to {2} {3}".format(video_path, start, end, output_path, ignore_keyframes_command))

def create_directories() :
	create_diectory(downloads_folder)
	create_diectory(output_folder)
	create_diectory(frames_folder)

def file_exists(file_path) :
	return os.path.isfile(file_path)

def get_frames(video_path, output_folder, video_name, framerate) :
	print("Extracting frames from {} moving to {} at framerate: {}".format(video_path, output_folder, framerate))
	return exec_command("ffmpeg -i {0} -vf fps={3} \"{1}{4}{2}_%d.png\"".format(video_path, output_folder, video_name, str(framerate), path_slash))

def download_and_cut_video(video_json, download = True) :
	downloaded_video_path = "{0}{2}{1}.mp4".format(downloads_folder, video_json["name"], path_slash)
	video_url = video_json["url"]
	if download :
		if not file_exists(downloaded_video_path) :
			download_video(video_url, downloaded_video_path)
		else :
			print("Video alredy downloaded! {} {}".format(video_url, downloaded_video_path))
	for index, chunck in enumerate(video_json["chuncks"]) :
		output_video_path = "{0}{3}{1}_{2}.mp4".format(output_folder, video_json["name"], str(index), path_slash)
		if not file_exists(output_video_path) :
			cut_video(
				downloaded_video_path, 
				chunck["start"], 
				chunck["end"], 
				output_video_path
				)
		else :
			print("Video alredy cutted! {}".format(output_video_path))


if extract_frames :
	print("Extracting frames from all videos in \"{}\" directory and saving them into \"{}\"".format(output_folder, frames_folder))
	for f in os.listdir(output_folder) :
		filename = f[:-4]
		get_frames(
			"{}{}{}".format(output_folder, path_slash, f),
			frames_folder,
			filename,
			5
			)
else:
	try : 
		parse_vids_file()
		create_directories()
		for el in data :
			download_and_cut_video(el)
	except ValueError as detail :
		print("Could not load vids.json! Probably you messed up json sintax. Details: " + str(detail))

