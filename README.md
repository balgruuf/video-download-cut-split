# video-download-cut-split


## Contribute and donate

If you found this script helpful, please consider to contribute or make a donation.
**BTC: 1AbC41w4EDCFj1sWTqsbdYDRr4Jp8f4jSa**

## Requirements

This script requires the followings:

- youtube-dl
- ffmpeg
- (python)

The listed programs must be installed and inserted into the path environement variable.

This script have been tested only on Window's Ubuntu subsystem, but should work fine on any OS, if not, please report it.

## Introduction

This is a very simple python script designed for **gathering material** for producing **face sets** starting from videos.

This script allows you to automatize the downloading, cutting and splitting process.

All you have to do is browse for videos you want to use, save the URL and write down the time at the start and end of the pieces you need from those videos.

Once you have all you can insert everything into the `vids.json` file. I made one just as a demonstration using Nic Cage interviews.

The all you have to do is to move inside the script directory and  type 

```
python video_download_cut_split.py
```
This will start the downloading and cutting process.
All the results will be inside the `downloaded` and `cutted` directories.

For splitting all the videos into single frames type 
```
python video_download_cut_split.py --split-frames
```

Type `python video_download_cut_split.py --help` for more options.

## The vids.json file

The `vids.json` file will contain all the informations needed for the **downloading** and **cutting** process.

Here's the content of the default `vids.json` file containing pieces of Nic Cage's interviews.

```json
[
	{
		"name": "nic1",
		"url": "https://www.youtube.com/watch?v=caxMBk1__-Y",
		"chuncks": 
			[
				{
					"start": "00:00:50.0",
					"end": "00:01:10.0"
				},
				{
					"start": "00:01:50.0",
					"end": "00:01:54.0"
				},
				{
					"start": "00:02:41.0",
					"end": "00:02:50.0"
				},
				{
					"start": "00:03:07.0",
					"end": "00:03:19.0"
				}
			]
	},
	{
		"name": "nic2",
		"url": "https://www.youtube.com/watch?v=6RRvDarJsHA",
		"chuncks":
			[
				{
					"start": "00:00:11.0",
					"end": "00:00:56.0"
				},
				{
					"start": "00:01:01.0",
					"end": "00:01:48.0"
				},
				{
					"start": "00:01:53.0",
					"end": "00:02:24.0"
				}
			]
	}
]
```
You can add as many videos as you want and as many chuncks as you want.

The URL can be from any site supported by youtube-dl.