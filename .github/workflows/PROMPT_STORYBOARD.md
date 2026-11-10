# Prompt untuk meminta storyboard ke Claude

Salin semua teks di bawah garis, ganti bagian <TOPIK> dan <MENIT>, lalu kirim ke Claude di chat.

---

Buatkan storyboard JSON untuk video dokumenter animasi 2D berbahasa Indonesia.
Topik: <TOPIK>. Target durasi: <MENIT> menit (5–10). Setiap adegan 6 detik, jadi butuh sekitar <MENIT> x 10 adegan.

Aturan:
- Balas HANYA satu blok JSON valid, tanpa penjelasan.
- Bentuk: {"title": "...", "accent": "#e8344a", "cast": {...}, "scenes": [...]}
- "cast": 2–4 tokoh, tiap tokoh: {"skin":"#hex","hair":"#hex","hair_style":"bob|short|long","outfit":"#hex","outfit_style":"sweater|shirt|suit","glasses":true|false,"clip":true|false}
- Tiap adegan: {"duration":6,"setting":..,"mood":..,"subtitle":"..","characters":[..],"props":[..],"camera":{..},"effects":[..],"transition":".."}
- subtitle: satu kalimat Indonesia akurat, maksimal 70 karakter. Narasi harus mengalir dari hook, penjelasan bertahap, sampai penutup.
- setting: spotlight_room, desk_topdown, galaxy, office, living_room, street, lab, bedroom_night, abstract, void
- mood: neutral, warm, cool, dramatic, dream, alert, night
- expression: neutral, happy, sad, surprised, angry, worried, sleepy, laugh, smug, scared, pain
- actions (tiap aksi {"do":..,"t":detik,"dur":detik}): wave, cheer, think, panic, point, surprised, sad, laugh, nod, shake, look, talk, scared, shrug, hold, press
- props.kind: phone, book, clock, brain, bulb, magnifier, newspaper, gear, red_button, coin, question, laptop, flask, hourglass, chart, heart, warning, bubble (opsional "text" pendek, "x","y" 0–1, "scale" 0.5–1.6, "anim": float|pulse|swing|none, "glow": true|false, "appear": detik)
- Karakter: "x" 0.28–0.72, "y" 1.04, "scale" 0.85–1.05; dua karakter berhadapan: yang kanan "flip": true.
- camera: {"from":{"zoom":1.0,"x":0.5,"y":0.5},"to":{"zoom":1.1–1.3,"x":..,"y":..},"punch":[[detik,0.08]]}
- transition: dissolve, wipe, glitch, fade_black, flash, cut. effects: ["particles"] atau ["dust"] atau [].
- Variasikan latar, kamera, properti, dan aksi di setiap adegan. Pilih properti yang cocok dengan narasi.
- Boleh karakter tidak ada di adegan yang menampilkan benda (mis. desk_topdown dengan properti saja).
