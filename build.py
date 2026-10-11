"""Build "No Exhaustion Blur.esp" from the plugins in a Skyrim SE Data folder.

Usage: python build.py "<path to Skyrim Special Edition/Data>"

The plugin overrides the four Survival Mode exhaustion "Imod" magic effects
(stages 2-5) and drops their VMAD (script) subrecord, which is what applies the
screen blur. Everything else in the records is copied unchanged.
"""
import os
import struct
import sys
import zlib

OUT_NAME = "No Exhaustion Blur.esp"
CC_SURVIVAL = "ccQDRSSE001-SurvivalMode.esl"
SMI = "SurvivalModeImproved.esp"
MASTERS = ["Skyrim.esm", "Update.esm", "Dawnguard.esm", "HearthFires.esm",
           "Dragonborn.esm", CC_SURVIVAL, SMI]
# form ID -> plugin whose version of the record is the winning one to patch
TARGETS = {
    0x050008EF: CC_SURVIVAL,  # Survival_ExhaustionStage2ImodEffect
    0x050008F0: SMI,          # Survival_ExhaustionStage3ImodEffect
    0x050008F1: SMI,          # Survival_ExhaustionStage4ImodEffect
    0x050008F2: SMI,          # Survival_ExhaustionStage5ImodEffect
}
ESL_FLAG = 0x200
COMPRESSED = 0x40000


def parse(path):
    """Return (masters, records) where records are (type, formid, flags, raw, data)."""
    b = open(path, "rb").read()
    assert b[:4] == b"TES4", path
    size = struct.unpack("<I", b[4:8])[0]
    masters = [v.rstrip(b"\0").decode("latin1")
               for t, v in subrecords(b[24:24 + size]) if t == b"MAST"]
    records = []

    def walk(start, end):
        i = start
        while i < end:
            if b[i:i + 4] == b"GRUP":
                group_size = struct.unpack("<I", b[i + 4:i + 8])[0]
                walk(i + 24, i + group_size)
                i += group_size
            else:
                data_size, flags, formid = struct.unpack("<III", b[i + 4:i + 16])
                data = b[i + 24:i + 24 + data_size]
                if flags & COMPRESSED:
                    data = zlib.decompress(data[4:])
                records.append((b[i:i + 4], formid, flags, b[i:i + 24 + data_size], data))
                i += 24 + data_size

    walk(24 + size, len(b))
    return masters, records


def subrecords(data):
    out, i = [], 0
    while i < len(data):
        length = struct.unpack("<H", data[i + 4:i + 6])[0]
        out.append((data[i:i + 4], data[i + 6:i + 6 + length]))
        i += 6 + length
    return out


def sub(tag, value):
    return tag + struct.pack("<H", len(value)) + value


def build(data_dir):
    parsed = {name: parse(os.path.join(data_dir, name)) for name in (CC_SURVIVAL, SMI)}
    # form IDs are copied verbatim, so the source plugins must share our master order
    for name, (masters, _) in parsed.items():
        expected = MASTERS[:len(masters)]
        if [m.lower() for m in masters] != [m.lower() for m in expected]:
            sys.exit(f"{name} has unexpected masters: {masters}")

    patched = []
    for formid, source in TARGETS.items():
        rec_type, _, flags, raw, data = next(
            r for r in parsed[source][1] if r[1] == formid and r[0] == b"MGEF")
        if flags & COMPRESSED:
            sys.exit(f"{formid:08X} is compressed; not supported")
        kept = [(t, v) for t, v in subrecords(data) if t != b"VMAD"]
        body = b"".join(sub(t, v) for t, v in kept)
        patched.append(raw[:4] + struct.pack("<I", len(body)) + raw[8:24] + body)

    records = b"".join(patched)
    group = b"GRUP" + struct.pack("<I", 24 + len(records)) + b"MGEF" + bytes(12) + records
    header = sub(b"HEDR", struct.pack("<fII", 1.7, len(patched), 0x800))
    header += sub(b"CNAM", b"custom\0")
    header += sub(b"SNAM", b"Removes the exhaustion screen blur; penalties unchanged.\0")
    for master in MASTERS:
        header += sub(b"MAST", master.encode("latin1") + b"\0") + sub(b"DATA", bytes(8))
    tes4 = b"TES4" + struct.pack("<IIIIHH", len(header), ESL_FLAG, 0, 0, 44, 0) + header
    return tes4 + group


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    plugin = build(sys.argv[1])
    with open(OUT_NAME, "wb") as f:
        f.write(plugin)
    print(f"wrote {OUT_NAME} ({len(plugin)} bytes)")
