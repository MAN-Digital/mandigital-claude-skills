#!/usr/bin/env python3
"""
Encode a PNG sequence to video, with profiles chosen for where the file is going.

Default is ProRes 422 HQ, not H.264 -- this material goes into an editor, and 8-bit
4:2:0 is a poor intermediate for flat-colour graphics with hard edges.

Usage:
  python encode.py --frames frames/ --fps 25 --profile edit --out animation.mov
  python encode.py --frames frames/ --fps 25 --profile edit-alpha --out overlay.mov
  python encode.py --frames frames/ --fps 25 --subframes 4 --out blurred.mov
  python encode.py --frames frames/ --fps 25 --profile web --out preview.mp4

Requires ffmpeg on PATH.
"""

import argparse
import pathlib
import shutil
import subprocess
import sys

BT709 = ["-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709"]

PROFILES = {
    # ProRes 422 HQ -- the default intermediate for cutting into a timeline
    "edit": {
        "ext": ".mov",
        "args": ["-c:v", "prores_ks", "-profile:v", "3", "-vendor", "apl0",
                 "-pix_fmt", "yuv422p10le"],
        "desc": "ProRes 422 HQ, 10-bit 4:2:2 -- editing intermediate",
    },
    # ProRes 4444 -- carries alpha, for overlays composited over footage
    "edit-alpha": {
        "ext": ".mov",
        "args": ["-c:v", "prores_ks", "-profile:v", "4444", "-alpha_bits", "16",
                 "-vendor", "apl0", "-pix_fmt", "yuva444p10le"],
        "desc": "ProRes 4444 + alpha, 10-bit 4:4:4 -- compositing intermediate",
    },
    # H.264 -- delivery and previews only
    "web": {
        "ext": ".mp4",
        "args": ["-c:v", "libx264", "-preset", "slow", "-crf", "18",
                 "-pix_fmt", "yuv420p", "-movflags", "+faststart"],
        "desc": "H.264 CRF 18 -- preview / YouTube / sharing",
    },
    # VP9 -- transparency that plays in a browser
    "web-alpha": {
        "ext": ".webm",
        "args": ["-c:v", "libvpx-vp9", "-crf", "24", "-b:v", "0", "-pix_fmt", "yuva420p"],
        "desc": "VP9 + alpha -- transparency in a browser",
    },
}


def main():
    p = argparse.ArgumentParser(description="Encode a PNG sequence to video.")
    p.add_argument("--frames", required=True, help="directory of f-%%06d.png frames")
    p.add_argument("--fps", type=int, default=25, help="output frame rate (default 25)")
    p.add_argument("--profile", default="edit", choices=list(PROFILES), help="output profile")
    p.add_argument("--out", required=True, help="output file")
    p.add_argument("--pattern", default="f-%06d.png", help="input filename pattern")
    p.add_argument("--subframes", type=int, default=1,
                   help="frames rendered per output frame; blends them for motion blur "
                        "(e.g. rendered at 100fps for a 25fps target -> --subframes 4)")
    p.add_argument("--shutter", type=int, default=180, choices=[90, 180, 270, 360],
                   help="shutter angle when --subframes > 1 (default 180)")
    p.add_argument("--dry-run", action="store_true", help="print the ffmpeg command and exit")
    args = p.parse_args()

    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg not found on PATH")

    frames = pathlib.Path(args.frames)
    found = sorted(frames.glob("*.png"))
    if not found:
        sys.exit(f"no PNGs in {frames}/")

    prof = PROFILES[args.profile]
    out = pathlib.Path(args.out)
    if out.suffix.lower() != prof["ext"]:
        print(f"note: profile '{args.profile}' expects {prof['ext']}, got {out.suffix} "
              f"-- ffmpeg may refuse or produce an unexpected container")

    # Input rate is the rate frames were rendered at; output rate is the target.
    in_fps = args.fps * args.subframes
    vf = []
    if args.subframes > 1:
        blend = max(1, round(args.subframes * args.shutter / 360))
        vf.append(f"tmix=frames={blend}")
        vf.append(f"framestep={args.subframes}")
        vf.append(f"fps={args.fps}")
        print(f"motion blur: blending {blend} of {args.subframes} subframes "
              f"({args.shutter}deg shutter)")

    cmd = ["ffmpeg", "-y", "-framerate", str(in_fps), "-i", str(frames / args.pattern)]
    if vf:
        cmd += ["-vf", ",".join(vf)]
    cmd += prof["args"] + BT709 + ["-r", str(args.fps), str(out)]

    print(f"profile: {prof['desc']}")
    print(f"input:   {len(found)} frames @ {in_fps}fps")
    print(f"output:  {out} @ {args.fps}fps\n")
    print(" ".join(cmd) + "\n")

    if args.dry_run:
        return

    r = subprocess.run(cmd)
    if r.returncode != 0:
        sys.exit(f"ffmpeg failed ({r.returncode})")

    size = out.stat().st_size / 1e6
    dur = len(found) / in_fps
    print(f"\nwrote {out} -- {size:.1f} MB, {dur:.2f}s, {args.fps}fps")
    if args.profile.startswith("edit"):
        print("Keep the PNG sequence until the edit is locked; it's the lossless master.")
    if args.profile == "edit-alpha":
        print("Premiere: if you see green/magenta tearing, Interpret Footage -> "
              "conform alpha premultiplication. Not a bad render.")


if __name__ == "__main__":
    main()
