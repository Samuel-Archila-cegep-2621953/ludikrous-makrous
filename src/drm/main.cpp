#include <iostream>
#include <cryptopp/modes.h>
#include <string>
#include <cryptopp/files.h>
#include <cryptopp/aes.h>
#include <cryptopp/gcm.h>
#include <cryptopp/osrng.h>
#include <cryptopp/filters.h>
#include <fstream>

#define PRODUCTION // enlever le commentaire durant les tests

const unsigned char CLE[] = {
(unsigned char)0x3c,
(unsigned char)0x23,
(unsigned char)0x46,
(unsigned char)0xeb,
(unsigned char)0xf2,
(unsigned char)0x0c,
(unsigned char)0x9d,
(unsigned char)0xa8,
(unsigned char)0x9d,
(unsigned char)0x30,
(unsigned char)0x52,
(unsigned char)0x5e,
(unsigned char)0x21,
(unsigned char)0x3e,
(unsigned char)0x76,
(unsigned char)0x2a,
(unsigned char)0xcb,
(unsigned char)0xe3,
(unsigned char)0xb9,
(unsigned char)0x25,
(unsigned char)0xac,
(unsigned char)0x35,
(unsigned char)0xb6,
(unsigned char)0x08,
(unsigned char)0xce,
(unsigned char)0xd7,
(unsigned char)0xa5,
(unsigned char)0x0a,
(unsigned char)0x68,
(unsigned char)0xdf,
(unsigned char)0xed,
(unsigned char)0x52
};

#ifndef PRODUCTION
using namespace CryptoPP;
void encryptFile(const std::string& inputFile,
                 const std::string& outputFile,
                 const SecByteBlock& key) {
    using namespace CryptoPP;

    AutoSeededRandomPool rng;

    // Generate random IV
    byte iv[12];
    rng.GenerateBlock(iv, sizeof(iv));

    // Set up encryption
    GCM<AES>::Encryption enc;
    enc.SetKeyWithIV(key, key.size(), iv, sizeof(iv));

    // Write IV to output file first, then encrypted data
    std::ofstream outFile(outputFile, std::ios::binary);
    outFile.write(reinterpret_cast<const char*>(iv), sizeof(iv));

    FileSource(inputFile.c_str(), true,
        new AuthenticatedEncryptionFilter(enc,
            new FileSink(outFile)
        )
    );
}

int construire(int argc, char** argv) {
    std::string fichier;
    std::cout << "Entrez le nom du fichier que vous voulez encrypter: ";
    std::cin >> fichier;

    SecByteBlock cle{CLE, 32};

    encryptFile(fichier, "jeu.dat", cle);

    return 0;
}
#endif

#ifdef PRODUCTION
using namespace CryptoPP;
void decryptFile(const std::string& inputFile,
                 const std::string& outputFile,
                 const SecByteBlock& key) {
    using namespace CryptoPP;

    // Read IV from beginning of file
    std::ifstream inFile(inputFile, std::ios::binary);
    byte iv[12];
    inFile.read(reinterpret_cast<char*>(iv), sizeof(iv));

    // Set up decryption
    GCM<AES>::Decryption dec;
    dec.SetKeyWithIV(key, key.size(), iv, sizeof(iv));

    // Decrypt remaining data
    FileSource(inFile, true,
        new AuthenticatedDecryptionFilter(dec,
            new FileSink(outputFile.c_str())
        )
    );
}

int production(int argc, char** argv) {
    SecByteBlock cle{CLE, 32};

    decryptFile("jeu.dat", "temp/jeu.exe", cle);

    system("start temp/jeu.exe");

    return 0;
}
#endif

int main(int argc, char** argv) {
    #ifdef PRODUCTION
    return production(argc, argv);
    #else
    return construire(argc, argv);
    #endif
}