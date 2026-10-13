# -*- coding: utf-8 -*-
"""fill_prompt - fuellt [Platzhalter] in KI-Prompt-Vorlagen und warnt vor Luecken.

Kein Netzwerk. Liest Dateien, schreibt nur mit --out (und nur eine neue Datei,
ausser --force). Standard: Ausgabe auf dem Bildschirm.

Beispiele:
  python fill_prompt.py --list
  python fill_prompt.py --prompt 2 --placeholders
  python fill_prompt.py --prompt 2 --set "Vorname Kunde=Anna" --set "Betrag=1.450,00 EUR"
  python fill_prompt.py --prompt 2 --values kunde.txt --out text.txt
"""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_FILE = os.path.join(HERE, "prompts", "zahlungserinnerung.md")
PLACEHOLDER = re.compile(r"\[([^\[\]\n]+)\]")


def load_prompts(path):
    """Gibt Liste (Titel, Text) zurueck; Abschnitte beginnen mit '## '."""
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    prompts, title, body = [], None, []
    for line in lines:
        if line.startswith("## "):
            if title is not None:
                prompts.append((title, "\n".join(body).strip()))
            title, body = line[3:].strip(), []
        elif title is not None:
            body.append(line)
    if title is not None:
        prompts.append((title, "\n".join(body).strip()))
    return prompts


def placeholders(text):
    seen = []
    for m in PLACEHOLDER.findall(text):
        if m not in seen:
            seen.append(m)
    return seen


def read_values(path):
    values = {}
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                print("Warnung: %s Zeile %d ohne '=' uebersprungen" % (path, n), file=sys.stderr)
                continue
            k, v = line.split("=", 1)
            values[k.strip().lower()] = v.strip()
    return values


def fill(text, values):
    def repl(m):
        return values.get(m.group(1).strip().lower(), m.group(0))
    return PLACEHOLDER.sub(repl, text)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Platzhalter in Prompt-Vorlagen fuellen.")
    ap.add_argument("--file", default=DEFAULT_FILE, help="Vorlagen-Datei (.md mit '## Titel'-Abschnitten)")
    ap.add_argument("--list", action="store_true", help="Prompts der Datei auflisten")
    ap.add_argument("--prompt", type=int, help="Nummer des Prompts (siehe --list)")
    ap.add_argument("--placeholders", action="store_true", help="nur die Platzhalter des Prompts zeigen")
    ap.add_argument("--set", action="append", default=[], metavar="NAME=WERT",
                    help="Platzhalter setzen (Gross-/Kleinschreibung egal), mehrfach nutzbar")
    ap.add_argument("--values", help="Textdatei mit Zeilen NAME=WERT (# = Kommentar)")
    ap.add_argument("--out", help="Ergebnis in neue Datei schreiben (ueberschreibt nichts ohne --force)")
    ap.add_argument("--force", action="store_true", help="bestehende --out-Datei ueberschreiben")
    args = ap.parse_args(argv)

    if not os.path.isfile(args.file):
        print("Datei nicht gefunden: %s" % args.file, file=sys.stderr)
        return 2
    prompts = load_prompts(args.file)

    if args.list or args.prompt is None:
        for i, (title, text) in enumerate(prompts, 1):
            print("%d. %s  (%d Platzhalter)" % (i, title, len(placeholders(text))))
        return 0

    if not 1 <= args.prompt <= len(prompts):
        print("Prompt-Nummer 1-%d erwartet." % len(prompts), file=sys.stderr)
        return 2
    title, text = prompts[args.prompt - 1]

    if args.placeholders:
        for p in placeholders(text):
            print(p)
        return 0

    values = {}
    if args.values:
        if not os.path.isfile(args.values):
            print("Werte-Datei nicht gefunden: %s" % args.values, file=sys.stderr)
            return 2
        values.update(read_values(args.values))
    for item in args.set:
        if "=" not in item:
            print("--set erwartet NAME=WERT, bekam: %s" % item, file=sys.stderr)
            return 2
        k, v = item.split("=", 1)
        values[k.strip().lower()] = v.strip()

    result = fill(text, values)
    missing = placeholders(result)

    if args.out:
        if os.path.exists(args.out) and not args.force:
            print("Abbruch: %s existiert schon (--force zum Ueberschreiben)." % args.out, file=sys.stderr)
            return 2
        with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(result + "\n")
        print("Geschrieben: %s" % args.out, file=sys.stderr)
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(result)

    if missing:
        print("\nNoch offen (%d): %s" % (len(missing), ", ".join("[%s]" % m for m in missing)), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
