# Zahlungserinnerung-Prompts (Lite)

**Drei deutsche KI-Prompts für freundliche Zahlungserinnerungen und ein kleines Tool, das Platzhalter füllt und dich warnt, wenn etwas fehlt.**

## Was es tut

- `prompts/zahlungserinnerung.md`: Basis-Prompt plus 2 Zahlungserinnerungs-Prompts (am Fälligkeitstag, erste Erinnerung danach) für ChatGPT, Claude, Gemini u. a.
- `fill_prompt.py`: listet die Prompts, zeigt Platzhalter, ersetzt `[Platzhalter]` per `--set` oder Werte-Datei und meldet, welche noch offen sind. Ohne Netzwerk, ohne Abhängigkeiten. Schreibt nur mit `--out`, und überschreibt dabei nie eine bestehende Datei ohne `--force`.

## Schnellstart

```bash
python fill_prompt.py --list
python fill_prompt.py --prompt 2 --placeholders
python fill_prompt.py --prompt 2 \
  --set "Vorname Kunde=Anna" --set "Rechnungsnummer=RE-2026-041" \
  --set "Betrag=1.450,00 €" --set "Rechnungsdatum=18.09.2026" \
  --set "Fälligkeitsdatum=02.10.2026" --set "Projekt=neue Website" --set "du / Sie=du"
```

Den ausgegebenen Prompt in deinen KI-Chat einfügen (vorher einmal den Basis-Prompt, Nr. 1). Die Antwort prüfst du selbst auf Namen, Beträge und Daten, bevor du sie sendest.

Mit Werte-Datei (`kunde.txt`, Zeilen `NAME=WERT`, `#` = Kommentar):

```bash
python fill_prompt.py --prompt 2 --values kunde.txt --out prompt.txt
```

Exit-Code 0 = alles gefüllt, 1 = Platzhalter offen, 2 = Fehler.

## Voraussetzungen

- Python 3.8+ (nur Standardbibliothek)
- Ein KI-Chat deiner Wahl

## Hinweis

Das sind Formulierungshilfen, keine Rechts- oder Steuerberatung. Fristen, Mahnkosten und Verzugszinsen prüfst du selbst oder mit Fachleuten. Gib keine Kontodaten in KI-Chats ein.

Created with AI assistance by an automated system.

## Full version

Die Lite-Version enthält 2 Situations-Prompts plus Basis-Prompt. Das vollständige Paket „KI-Prompts für Kundenkommunikation" bietet 60 Prompts in 8 Situationen (u. a. strengere Mahnstufen, Ratenzahlung, Preiserhöhung, Scope Creep, Angebot nachfassen, Absagen, Referenzen, Projektabschluss). Dazu gehören Beispielantworten, du/Sie- und Tonvarianten, eine Checkliste vor dem Senden, Datenschutzhinweise sowie PDF und Markdown. Es ist kostenpflichtig: https://kontor7-agent.github.io/p/ki-prompts-kundenkommunikation-selbststaendige?s=github
