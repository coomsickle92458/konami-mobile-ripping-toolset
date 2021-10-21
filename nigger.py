import requests 
import json

def download(url, path):
	file = open(path, "wb")
	response = requests.get(url)
	for chunk in response.iter_content(chunk_size=1024):
		file.write(chunk)
	file.close()

database = json.loads(open("decrypted/ablist.json", "r").read())

for asset in database["assetBundles"]:
	if asset["bundleName"].startswith("playables/full/music"):
		download(
			f'http://d3u9qu1rz2zw6v.cloudfront.net/assetbundles/android/1632984632/{asset["publishPath"]}', 
			f'com.konami.android.jubeat/files/ab/{asset["publishPath"]}'
		)