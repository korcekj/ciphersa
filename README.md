# Cipher
A simple commandline app for encrypting and decrypting your files
# Installation

## Manual
```bash
  $ git clone https://github.com/korcekj/ciphersa.git
  $ cd ciphersa
  $ python setup.py install
```
# Usage
```bash
$ ciphersa --help
```
## Encryption
* `-k <file_path> - Cesta k súboru public RSA kľúča` 
* `-in <file_path> [required] - Cesta k súboru určeného na šifrovanie` 
* `-out <file_path> - Cesta k výstupnému súboru, výsledok šifrovania` 
```bash
$ ciphersa e -in your_dir/file.txt -k your_dir/id_rsa.pubk
```
## Decryption
* `-k <file_path> [required] - Cesta k súboru private RSA kľúča`
* `-in <file_path> [required] - Cesta k zašifrovanému súboru`
* `-out <file_path> - Cesta k vústupnému súboru, výsledok dešifrovania`
```bash
$ ciphersa d -in your_dir/file.txt.enc -k your_dir/id_rsa.pk
```
## Generating RSA keypair
* `-out <dir_path> - Cesta k vústupnému priečinku, ak nie je uvedený, bude vygenerovaný v aktuálnom priečinku`
```bash
$ ciphersa rsa -out your_dir
```