# Digital Signature for Text File
## Semester I Tahun 2021/2022

### Tugas Kecil V IF4020 Kriptografi

*Program Studi Teknik Informatika* <br />
*Sekolah Teknik Elektro dan Informatika* <br />
*Institut Teknologi Bandung* <br />

*Semester I Tahun 2021/2022*

## Description
Aplikasi berbasis Web untuk membuat dan memverifikasi tanda-tangan digital pada dokumen (file) 
elektronis, dalam hal ini file teks. Dalam hal ini, anda sebagai pemilik dokumen mempunyai sepasang 
kunci, yaitu kunci publik dan kunci privat. <br>
Tanda tangan dapat disimpan di dalam dokumen terpisah atau digabung di dalam file yang ditandatangani 
(tanda tangan digital diletakkan pada akhir dokumen). Pengguna dapat memilih apakah tanda-tangan 
disimpan di dalam dokumen terpisah atau disatukan di dalam file pesan. <br>
Tanda tangan digital bergantung pada isi file dan kunci. Tanda-tangan digital direpresentasikan 
sebagai karakter-karakter heksadesimal. Untuk membedakan tandatangan digital dengan isi dokumen, maka tanda-tangan digital diawali dan diakhiri dengan suatu tag.

## Author
1. Gde Anantha Priharsena (13519026)
2. Reihan Andhika Putra (13519043)
3. Reyhan Emyr Arrosyid (13519167)

## Requirements
- [Python 3](https://www.python.org/downloads/)

## Installation And Run
Clone the repository
```bash
git clone https://github.com/hokkyss/Stima03_OTOBOT.git
cd src
```
### Automatic Setup
#### First Time Setup
1. Open `setup.bat`
2. Wait until the installation is finished
3. The setup will automatically open the web browser
4. If the page failed to load, wait a moment then refresh the page

#### Run
1. Open `run.bat`
2. It will automatically open the web browser
3. If the page failed to load, wait a moment then refresh the page

#### Manual Setup
After cloning the repository
```bash 
cd src
python -m venv virt
virt\Scripts\activate
pip install -r requirements.txt
python app.py
```
Then open your web browser and go to [localhost:5000](http://localhost:5000)

## Screen Capture 
### Generate Key

### Generate Digital Signature

### Verify Digital Signature