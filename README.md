# meine-app

[![CI](https://github.com/GitGitRice/meine-app/actions/workflows/ci.yml/badge.svg)](https://github.com/GitGitRice/meine-app/actions/workflows/ci.yml)

Eine kleine Python-Anwendung (`src/rechner.py`) mit Tests (`tests/test_rechner.py`) und einer CI-Pipeline mit GitHub Actions.

## Was die Pipeline macht

Die Pipeline liegt in `.github/workflows/ci.yml`. Sie startet automatisch bei jedem **Push** und bei jedem **Pull Request**.

Sie hat zwei Jobs, die parallel laufen:

### Job `test`

Läuft auf `ubuntu-latest` mit einer Python-Version. Die Version steht in der Workflow-Variable `PYTHON_VERSION` (aktuell **3.12**). Die Variable `APP_ENV` legt die Umgebung fest (aktuell `staging`).

Schritte:

1. **Repository auschecken** – `actions/checkout` holt den Code auf den Runner.
2. **Python installieren** – `actions/setup-python` installiert die Python-Version aus `PYTHON_VERSION`.
3. **Dependencies installieren** – `python -m pip install -r requirements.txt` (installiert `pytest`).
4. **Tests ausführen** – `python -m pytest -v`. Schlägt ein Test fehl, wird der Job rot.
5. **Konfiguration anzeigen** – gibt `PYTHON_VERSION` und `APP_ENV` im Log aus.

### Sicherheit

- Alle Actions sind auf einen festen Commit-SHA gepinnt (nicht `@main`). So ändert sich das Verhalten der Pipeline nicht unbemerkt.
- `permissions: {}` auf Workflow-Ebene. Jeder Job bekommt nur die Rechte, die er braucht.
- `persist-credentials: false` beim Checkout.
- Die Workflow-Datei wurde mit [zizmor](https://github.com/zizmorcore/zizmor) geprüft.

### Commit-SHA für eine Action finden

Ein Tag wie `v4` kann sich ändern. Ein Commit-SHA ändert sich nie. Darum steht im Workflow der SHA und die Version nur als Kommentar:

```yaml
uses: actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a # v7.0.1
```

Voraussetzung: [GitHub CLI](https://cli.github.com/) (`gh`) ist installiert und angemeldet (`gh auth login`).

1. Neueste Version finden:

   ```bash
   gh api repos/actions/upload-artifact/releases/latest --jq .tag_name
   ```

   Alle Tags einer Hauptversion (hier `v4`) zeigen:

   ```bash
   git ls-remote --tags https://github.com/actions/upload-artifact 'v4.*'
   ```

2. Commit-SHA für genau diese Version holen:

   ```bash
   gh api repos/actions/upload-artifact/commits/v7.0.1 --jq .sha
   ```

   Der Befehl gibt immer den SHA des Commits aus, auch bei annotierten Tags. Ohne `gh` geht es mit `git ls-remote`. Bei annotierten Tags gibt es dort zwei Zeilen. Dann gilt der SHA der Zeile mit `^{}` am Ende.

3. Im Workflow `@v7.0.1` durch `@<SHA> # v7.0.1` ersetzen.

Für eine andere Action `actions/upload-artifact` durch `<besitzer>/<repo>` ersetzen, zum Beispiel `actions/download-artifact`. Immer eine genaue Version (`v7.0.1`) nehmen, nicht nur die Hauptversion (`v7`). Sonst passt der Kommentar nicht sicher zum SHA.

## Lokal ausführen

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python -m pytest -v
```

Erwartete Ausgabe: `3 passed`.

> Tests immer mit `python -m pytest` aus dem Projektordner starten. Sonst findet Python das Modul `src` nicht.

## Challenge: rote Pipeline wieder grün

Die Pipeline war nach der Challenge aus zwei Gründen rot:

| Fehler                                                 | Seite     | Log-Meldung                            | Fix                                                                    |
| ------------------------------------------------------ | --------- | -------------------------------------- | ---------------------------------------------------------------------- |
| `requirement.txt` statt `requirements.txt` im Workflow | Workflow  | `Could not open requirements file`     | Dateinamen korrigiert                                                  |
| `assert summe(2, 3) == 6` im Test                      | Anwendung | `assert 5 == 6` · `1 failed, 2 passed` | Erwartung auf `5` korrigiert – der Test war falsch, nicht die Funktion |

Danach sind alle Jobs grün mit `3 passed`.

Die korrigierten Challenge-Dateien liegen als Kopie im Ordner `challenge/`:

- `challenge/ci-challenge.yml` – der Challenge-Workflow (liegt bewusst nicht in `.github/workflows/`, damit er nicht als zweite Pipeline läuft)
- `challenge/challenge_test_rechner.py` – die Challenge-Tests (Name beginnt bewusst nicht mit `test_`, damit pytest sie nicht doppelt ausführt)
