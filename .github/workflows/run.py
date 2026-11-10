#!/usr/bin/env python3
"""Pembuat video animasi dokumenter 2D otomatis.

Contoh:
  python run.py --mode test                          # video percobaan 30 detik
  python run.py --mode file --storyboard storyboards/video_saya.json
  python run.py --mode topik --topik "Kenapa langit berwarna biru?" --menit 6
"""
import argparse
import json
import os
import shutil
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from src import storyboard as SB          # noqa: E402
from src.render import log, prepare, render_video   # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["test", "file", "topik"], default="test")
    ap.add_argument("--storyboard", default="", help="path file storyboard .json (mode file)")
    ap.add_argument("--topik", default="", help="judul/topik video (mode topik)")
    ap.add_argument("--menit", type=float, default=6.0, help="target durasi (mode topik)")
    ap.add_argument("--keluaran", default=os.path.join(ROOT, "output", "video.mp4"))
    ap.add_argument("--work", default=os.path.join(ROOT, "work"))
    ap.add_argument("--workers", type=int, default=0, help="jumlah proses paralel (0 = otomatis)")
    ap.add_argument("--ai-latar", action="store_true", help="coba buat latar dengan layanan gambar gratis")
    ap.add_argument("--detik-maks", type=float, default=0, help="render hanya N detik pertama (uji cepat)")
    ap.add_argument("--skala", type=float, default=1.0, help="1.0 = 1920x1080; 0.5 = pratinjau cepat")
    ap.add_argument("--crf", type=int, default=19)
    args = ap.parse_args()

    t0 = time.time()
    if args.mode == "test":
        sbn = SB.load_storyboard(os.path.join(ROOT, "storyboards", "contoh_30detik.json"))
    elif args.mode == "file":
        if not args.storyboard:
            sys.exit("Isi nama file storyboard. Contoh: storyboards/video_saya.json")
        path = args.storyboard if os.path.isabs(args.storyboard) else os.path.join(ROOT, args.storyboard)
        if not os.path.exists(path):
            sys.exit("File storyboard tidak ditemukan: %s" % path)
        sbn = SB.load_storyboard(path)
    else:
        if not args.topik.strip():
            sys.exit("Isi topik video.")
        from src import llm
        try:
            raw = llm.generate_storyboard(args.topik.strip(), args.menit, log=log)
        except Exception as e:   # layanan gratis gagal -> pesan jelas untuk pemula
            sys.exit("\n[GAGAL] %s" % e)
        os.makedirs(os.path.join(ROOT, "storyboards"), exist_ok=True)
        with open(os.path.join(ROOT, "storyboards", "terakhir_dari_topik.json"), "w", encoding="utf-8") as f:
            json.dump(raw, f, ensure_ascii=False, indent=1)
        sbn = SB.normalize(raw, args.topik)

    total = SB.total_seconds(sbn)
    log("[info] judul: %s | %d adegan | durasi %.1f detik (%.1f menit)" % (sbn["title"], len(sbn["scenes"]), total, total / 60))
    if args.mode != "test" and not (300 <= total <= 600):
        log("[peringatan] durasi di luar 5-10 menit. Tambah/kurangi adegan di storyboard.")

    prepare(sbn, args.work, ai_bg=args.ai_latar)
    render_video(args.work, args.keluaran, workers=args.workers or None, crf=args.crf,
                 max_seconds=args.detik_maks or None, scale=args.skala)
    log("[selesai] total %.1f menit. Hasil: %s" % ((time.time() - t0) / 60, args.keluaran))


if __name__ == "__main__":
    main()
