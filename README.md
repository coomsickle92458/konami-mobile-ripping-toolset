# Konami Mobile Ripping Toolset

![kagemasa](misc/kagemasa.png)

A set of tools for ripping music from Konami mobile games


## Contents

- **nigger.py** for niggering konami's website, ripping all remote assets 
- **fuck.py** for fucking encryption on assets
- **fuck.cs** for fucking encryption on other files (static assets)
- **cum.py** for gluing artwork, titles and music together

## Support

Only tested on jubeat

## Technicals/Structure

- Static assets are decrypted using fuck.cs with a hardcoded key/iv

- Original file path (bundlePath) is used for both salt and password 
- PBKDF1 used for derivation [(C# implementation)](https://docs.microsoft.com/en-us/dotnet/api/system.security.cryptography.passwordderivebytes?view=net-5.0) the C# implementation is out of spec and allows salts of arbitrary lengths!
- AES-128-ECB is used for implementing custom AES-CTR mode. Block counter is used for CTR nonce
- Assets are distributed encrypted via amazon storage instance `http://d3u9qu1rz2zw6v.cloudfront.net/`
- `/sdcard/Android/data/com.konami.android.jubeat/files/ab/ablist.json` - stores list of assets and their original paths (encrypted)

```json
{
	"assetBundles": [
		{
			"bundleName": "playables/preview/music_321201404",
			"assetPaths": [
				"konami/assetbundles/playables/audio/previews/321201404_preview.wav"
			],
			"dependencies": [],
			"crc": 649798932,
			"hash": "5c5044e712f1c4340e673307b42245efc0aeebfa",
			"size": 632921,
			"expire": "",
			"label": "playable_preview_music",
			"publishPath": "f/f00f46786073ead6f28282f667371d148d5d26f2"
		},
		{
			"bundleName": "playables/preview/music_321201501",
			"assetPaths": [
				"konami/assetbundles/playables/audio/previews/321201501_preview.wav"
			],
			"dependencies": [],
			"crc": 2050081105,
			"hash": "62882dad67b528ac17d3ad4b776126379cb04a96",
			"size": 595706,
			"expire": "",
			"label": "playable_preview_music",
			"publishPath": "1/15979d60adbf2392c771a4f3da4508bd3a4d19b8"
		},
	]
}
....
```
- 4 different decryption functions for your pleasure. Fuck konami

![kagemasa](misc/konamiisfuckinginsane.png)

