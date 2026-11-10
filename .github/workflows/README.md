# Generator Video Animasi Dokumenter 2D

Membuat video animasi dokumenter 2D (1920x1080, MP4, subtitle Indonesia, tanpa suara) secara otomatis
di GitHub Actions. Karakter, latar, dan properti digambar otomatis oleh kode. Tanpa API berbayar.

## Cara pasang (sekali saja, semua dari HP)

Buka **github.com** lewat browser HP (Chrome). Jika tampilan kecil, buka menu titik tiga lalu centang **Situs desktop**.

1. **Buat akun GitHub** (gratis) dan login.
2. **Buat repo baru**: tombol **+** → **New repository**. Isi nama `video-dokumenter`, pilih **Public**
   (Actions gratis tanpa batas untuk repo publik), centang **Add a README file**, lalu **Create repository**.
3. **Unggah proyek**: di halaman repo tekan **Add file → Upload files**, pilih file `proyek.zip`
   dari HP, tunggu selesai, lalu **Commit changes**. (Jangan di-unzip. Cukup unggah zip-nya.)
4. **Buat file workflow**: **Add file → Create new file**. Pada kolom nama ketik persis:
   `.github/workflows/video.yml` (garis miring otomatis membuat folder).
   Tempel isi file `video.yml` (ada di pesan chat dan di dalam zip folder `github/`), lalu **Commit changes**.

## Cara membuat video

1. Buka tab **Actions** → pilih **Buat Video** di kiri → tombol **Run workflow**.
2. **Video percobaan 30 detik**: biarkan `mode = test`, tekan **Run workflow** hijau.
3. Tunggu sampai ada tanda centang hijau (percobaan 30 detik sekitar 5–10 menit).
4. Ambil hasilnya:
   - Menu **Releases** di halaman repo (bagian kanan/bawah) → unduh `video.mp4` langsung, atau
   - Buka run yang selesai → bagian **Artifacts** → `video-mp4` (berbentuk zip).

## Membuat video 5–10 menit

**Cara A (kualitas terbaik, disarankan): storyboard dari Claude**
1. Di chat Claude, minta: *"Buat storyboard JSON untuk video 6 menit tentang <topik Anda>"* dan tempel
   isi file `PROMPT_STORYBOARD.md`.
2. Salin JSON jawabannya. Di GitHub: **Add file → Create new file**, nama `storyboards/video_saya.json`, tempel, Commit.
3. **Actions → Buat Video → Run workflow**: `mode = file`, `storyboard = video_saya.json`.

**Cara B (otomatis dari topik)**: `mode = topik`, isi `topik` dan `menit` (5–10). Program meminta naskah ke layanan teks
gratis. Layanan gratis bisa sibuk atau berubah. Jika gagal, pesan di log akan menyuruh memakai Cara A.

Waktu render sekitar 1–3 detik komputasi per detik video. Repo publik memakai 4 inti, jadi video 6 menit biasanya selesai dalam 15–30 menit.

## Isi proyek

| Folder/file | Fungsi |
|---|---|
| `run.py` | Titik masuk: storyboard → aset → render → MP4 |
| `src/chargen.py` | Menggambar karakter berlapis (kepala, rambut, badan, lengan, mata, mulut) |
| `src/rig.py` | Kerangka gerak: IK lengan, 16 aksi (melambai, berpikir, panik, menunjuk, dll.), kedip, ekspresi |
| `src/props.py` | 18 properti (ponsel, buku, otak, jam, lampu, grafik, dll.) |
| `src/backgrounds.py` | 10 latar (ruang sorot, meja, galaksi, kantor, jalan, lab, dll.) + pencahayaan |
| `src/engine.py` | Kamera, parallax, transisi, efek, subtitle |
| `src/render.py` | Render paralel + FFmpeg |
| `src/storyboard.py` | Validasi storyboard (nilai salah diganti nilai aman) |
| `src/llm.py` | Naskah otomatis dari topik (layanan gratis) |
| `storyboards/` | Storyboard JSON (contoh 30 detik tersedia) |
| `assets/fonts/` | Font Inter (lisensi OFL) |

## Skema storyboard

Lihat `storyboards/contoh_30detik.json`. Nilai yang didukung:

- **setting**: `spotlight_room, desk_topdown, galaxy, office, living_room, street, lab, bedroom_night, abstract, void`
- **mood**: `neutral, warm, cool, dramatic, dream, alert, night`
- **expression**: `neutral, happy, sad, surprised, angry, worried, sleepy, laugh, smug, scared, pain`
- **actions**: `wave, cheer, think, panic, point, surprised, sad, laugh, nod, shake, look, talk, scared, shrug, hold, press`
- **props.kind**: `phone, book, clock, brain, bulb, magnifier, newspaper, gear, red_button, coin, question, laptop, flask, hourglass, chart, heart, warning, bubble`
- **transition**: `cut, dissolve, fade_black, wipe, glitch, flash`
- **effects**: `particles, dust, glitch@detik, shake@detik`
- Posisi `x`, `y` adalah pecahan lebar/tinggi layar (0–1). `y` karakter ≈ 1.04 (pinggang di tepi bawah).
- Karakter dapat memegang properti: `"attach": {"hand": "both", "who": "tokoh"}`.
- Durasi adegan otomatis menyesuaikan panjang subtitle (sekitar 15 huruf per detik).

## Mencoba di komputer (opsional)

```
pip install -r requirements.txt     # perlu FFmpeg terpasang
python run.py --mode test --skala 0.5 --detik-maks 6    # pratinjau cepat
```
