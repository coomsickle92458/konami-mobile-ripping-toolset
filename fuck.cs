using System;
using System.IO;
using System.Security.Cryptography;

class Decrypt
{
    private static string filename = "com.konami.android.jubeat/files/Play/MusicList";

    // These are stored within the global-metadata.dat file.
    // Load libil2cpp.so into IDA, load a script to annotate it and look at the JubeatPlus.CacheAssets.cctor method
    // sub_D3951C(&Field__PrivateImplementationDetails__5A3388CBB074822B17DC4803B4E6CDB4B1B7D3CF6B838D5B8EA3F7214C816A16);
    // sub_D3951C(&Field__PrivateImplementationDetails__936B6263B960F54C42A14CDECEAF2263923582E6606539F03983C22403CC2FB8);
    // Look for the two PID initializations, copy the hash at the end and scan for them in dump.cs
    // Read appropriate number of bytes from global-metadata.dat (offset is in dump.cs)
    
    private static byte[] cryptKey = new byte[] {
        0x79, 0xAA, 0x84, 0x26, 0xA3, 0x77, 0xDD, 0x9C,
        0x48, 0xB2, 0x4B, 0x14, 0x6E, 0xB7, 0x66, 0x62
    };
    private static byte[] cryptIV = new byte[] {
        0x34, 0x6E, 0x8B, 0x40, 0x9B, 0xFE, 0x9E, 0x4F,
        0xA5, 0xA1, 0xEE, 0xE2, 0x72, 0xBC, 0x72, 0x26
    };

    public static void Main(string[] args)
    {
        byte[] fileBytes = File.ReadAllBytes(filename);
        RijndaelManaged rijndaelManaged = new RijndaelManaged();
        rijndaelManaged.BlockSize = 128;
        rijndaelManaged.KeySize = 128;
        rijndaelManaged.Mode = CipherMode.CBC;
        rijndaelManaged.Padding = PaddingMode.PKCS7;
        rijndaelManaged.IV = cryptIV;
        rijndaelManaged.Key = cryptKey;
        ICryptoTransform decryptor = rijndaelManaged.CreateDecryptor(cryptKey, cryptIV);
        byte[] output = decryptor.TransformFinalBlock(fileBytes, 0, fileBytes.Length);
        File.WriteAllBytes(filename + "-dec.bin", output);
    }
}