
import os
import os.path
import glob
import json 
import struct
import Crypto
import Crypto.Cipher
import Crypto.Cipher.AES
import Crypto.Util
import Crypto.Util.Counter
import Crypto.Util.Padding
import Crypto.Protocol.KDF
import Crypto.Hash

# Implementation without salt length restriction
def csharp_PBKDF1(password, salt):
	hashAlgo = Crypto.Hash.SHA1
	password = Crypto.Util.py3compat.tobytes(password)
	pHash = hashAlgo.new(password+salt)
	digest = pHash.digest_size
	for i in Crypto.Util.py3compat.iter_range(100-1):
		pHash = pHash.new(pHash.digest())
	return pHash.digest()[:16]

def decrypt_file(path, path_local):
	path = path.replace("\\", "/")

	password = salt = path_local.encode("utf8")

	print(path_local)

	if len(salt) < 8:
		salt = salt + salt + b"\0"

	key = csharp_PBKDF1(password, salt) # C# PasswordDeriveBytes.InterationCount = 100
	file_size = os.path.getsize(f'./{path}')

	with open(path, "rb") as file:

		decrypter = Crypto.Cipher.AES.new(
			key,
			Crypto.Cipher.AES.MODE_ECB,
		)

		path_escaped = path_local.replace("/", "_").replace("\\", "_")

		file_output = open(f'decrypted/{path_escaped}', "wb")

		while file_size - file.tell() > 0:
			
			pos = file.tell()
			block_number = int(pos / 16 + 1) 
			block = bytearray(file.read(16))
			mask = bytearray(decrypter.encrypt(struct.pack("<qq", block_number, 0)))
			data = bytearray(block)

			for offset in range(len(data)):
				data[offset] ^= mask[offset]

			file_output.write(data)

def find_asset_by_path(path):
	for asset in database["assetBundles"]:
		if asset["publishPath"] == path:
			return asset
	
decrypt_file("com.konami.android.jubeat/files/ab/ablist.json", "ablist.json")
decrypt_file("com.konami.android.jubeat/files/Play/MusicList", "Play/MusicList")

database = json.loads(open("decrypted/ablist.json", "r").read())

for path in glob.glob("com.konami.android.jubeat/files/ab/**/*", recursive=True):

	if not os.path.isfile(path): continue
	if "ablist.json" in path: continue

	path = path.replace("\\", "/")

	path_publish = path.replace("com.konami.android.jubeat/files/ab/", "")
	asset = find_asset_by_path(path_publish)

	if not asset:
		print("missing asset", path_publish)
		continue

	path_escaped = asset["bundleName"].replace("/", "_").replace("\\", "_")

	if os.path.isfile(f'decrypted/{path_escaped}'): continue

	decrypt_file(path, asset["bundleName"])