import glob 
import re 
import os
import os.path
import json

def find_metadata(playable_id):
	for meta in music_list:
		if re.findall(r"(\d+)_bgm", meta["sound"])[0] == playable_id:
			return meta
			

music_list = json.loads(open("MusicList-dec.bin", "r").read())

for playable_path in glob.glob("./exported/AudioClip/*_bgm.wav"):

	print(playable_path)

	playable_id = re.findall(r"(\d+)_bgm", playable_path)[0]
	jacket_path = f'./exported/Texture2D/{playable_id}_jacket.png'
	song_folder = f'./jubeat_dump/{playable_id}'

	if not os.path.exists(song_folder): os.mkdir(song_folder)
	
	os.rename(jacket_path, f'{song_folder}/cover.png')
	os.rename(playable_path, f'{song_folder}/{playable_id}.wav')

for path in glob.glob(f'./jubeat_dump/*'):

	path = path.replace("\\", "/")

	playable_id = re.findall(r"jubeat_dump\/(\d+)", path)[0]
	song_folder = f'./jubeat_dump/{playable_id}'

	meta = find_metadata(playable_id)
	
	os.system(" ".join([
		"ffmpeg",
		f'-i "{song_folder}/{playable_id}.wav"',
		f'-i "{song_folder}/cover.png"',
		f'-map 0:0',
		f'-map 1:0',
		f'-disposition:v attached_pic',
		f'-c:v copy',
		f'-id3v2_version 3',
		f'-metadata title="{meta["title"]}"',
		f'-metadata artist="{meta["artist"]}"',
		f'-metadata album="jubeat"',
		f'"./jubeat_music/{playable_id}_{meta["title"]}.flac'
	]))
