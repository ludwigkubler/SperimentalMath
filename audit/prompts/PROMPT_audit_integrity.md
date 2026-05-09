# Prompt — AUDIT 1 di 2: integrità del codice (multi-agente)

Apri una nuova sessione di Claude Code (con accesso ssh a `ludo@sec`) e incolla esattamente questo prompt.

---

# Audit di integrità del codice del server `ludo@sec`

Sei un audit-conductor. Il tuo compito è coordinare un audit multi-agente di
**tutto il codice sorgente** presente sul server `ludo@sec`, identificando
problemi di integrità, codice morto, ridondanza e bug.

## Vincoli di sicurezza

- **Solo lettura**. Non modificare, non rinominare, non eliminare nulla.
- Non esfiltrare credenziali, chiavi private, file `.env`, `id_rsa`, ecc.
  Se trovi qualcosa che sembra un secret, **non includerlo nei report** —
  segnala solo "secret leak detected at <path>:<line>" senza riprodurre il
  contenuto.
- Non eseguire codice estraneo. Se serve eseguire un linter su un file,
  fallo solo con tool standard installati di sistema (`python3 -m pyflakes`,
  `ruff`, `mypy`, `shellcheck`, `eslint` se disponibile).
- I report finali vanno scritti in `~/Scrivania/SEC/research/git_mirrors/SperimentalMath/audit/code_integrity/`
  sul server (crea la cartella se manca).

## Scope di file da includere

Estensioni programming language (in ordine di prevalenza attesa sul server):

```
.py .js .ts .tsx .jsx .lean .sh .bash .zsh .fish
.rs .go .c .cpp .cc .h .hpp .java .kt .rb .php
.lua .pl .r .R .swift .nim .zig .elm .clj .cljs
.ex .exs .erl .hs .ml .vue .svelte .scala
.css .scss .sass .html .htm .xml
.tex .bib .toml .yaml .yml .ipynb
.sql .dockerfile Makefile CMakeLists.txt
```

Anche file senza estensione che iniziano con shebang (`#!/usr/bin/env ...`,
`#!/bin/bash`, ecc.).

## Scope di file da ESCLUDERE

- Immagini: `.png .jpg .jpeg .gif .bmp .svg .webp .tif .tiff .ico .heic`
- Video: `.mp4 .mov .avi .mkv .webm .flv .wmv .m4v`
- Audio: `.mp3 .wav .flac .ogg .m4a .aac .opus`
- Binari: `.so .o .a .dll .exe .pyc .class .jar .wasm`
- Cartelle: `.git/ node_modules/ __pycache__/ .venv/ venv/ env/ dist/ build/ target/ .cache/ .mypy_cache/ .pytest_cache/ .ruff_cache/`
- Lockfile: `*.lock package-lock.json yarn.lock Cargo.lock poetry.lock`
- Database: `.sqlite .sqlite3 .db` (flagga ma non aprire)
- Modelli ML: `.pt .pth .ckpt .safetensors .gguf .onnx .h5 .pb` (flagga
  solo per dimensione totale)

## Cartelle root da scansionare

- `~/Scrivania/SEC/` (sistema SEC, autonomous research engine)
- `~/kissat/pvnp_lab/` (PvsNP Lab, P-vs-NP autonomous engine)
- `~/Scrivania/future/` (sperimentalmath playground)
- `~/Scrivania/pubblicazioni/` (output reports / paper drafts)
- `~/tools/` (Wav2Lip, ecc.)
- Qualsiasi altra cartella sotto `~/` che contenga >100 file sorgente
  (rilevala con un primo `find ~/ -maxdepth 3 -type d` e decidi).

L'utente menziona quattro sistemi principali: **SEC**, **PvsNP Lab**,
**ENTITY**, **sperimentalmath**. Cerca attivamente "ENTITY" — può essere
un agent runtime non in `~/Scrivania/SEC/`. Pattern di ricerca:
`grep -rln "class Entity\|ENTITY_\|entity_runtime" ~/ --include="*.py"`.

## Architettura multi-agente

Spawna **6 sub-agent in parallelo** usando il tool `Agent` (subagent_type
default), ciascuno con un compito specifico. Tutti operano in read-only
e producono un report markdown sotto la propria cartella.

### Agent 1 — Inventory
- Conta i file source per (sistema × estensione × LOC)
- Produce `code_integrity/01_inventory.md` con tabella e size totals
- Tempo stimato: 5 min

### Agent 2 — Static analysis (Python only, perché è il bulk del codice)
- Esegue `python3 -m pyflakes <file>` su ogni `.py` (skip se >2000 LOC)
- Esegue `python3 -m py_compile <file>` per beccare SyntaxError
- Se `ruff` o `mypy` sono disponibili (`which ruff`), eseguili in modalità
  conservativa (`ruff check --select=E,F,W` senza autofix)
- Aggrega per (file, error_type). Top-30 file per error count.
- Produce `code_integrity/02_static_python.md`

### Agent 3 — Static analysis (shell + lean + altri)
- `shellcheck` su tutti gli script `.sh`/`.bash` (se installato)
- Per `.lean`: `lean --json` per controllare type-checking (skip se
  >500 LOC, e solo se `lean` è in PATH)
- Per `.js/.ts`: se `node_modules/` ha `eslint`, eseguilo; altrimenti
  segnala "no JS linting available"
- Produce `code_integrity/03_static_other.md`

### Agent 4 — Dead code & orphans
- Per ogni `.py` definito in `~/Scrivania/SEC/src/research/`,
  `~/kissat/pvnp_lab/system_v2/src/`, etc., grepperà se la sua funzione
  pubblica (definizioni `def NAME` non in `_NAME`) è importata altrove.
- File orfani: nessun import esterno → "potenzialmente non usato"
- Imports non usati: `pyflakes` already cattura
- Produce `code_integrity/04_dead_code.md` con due tabelle: file orfani,
  funzioni morte (con caveat: forse usate dinamicamente)

### Agent 5 — Code duplication / redundancy
- Per `.py`: identifica blocchi >20 LOC duplicati (anche con piccole
  differenze) tramite confronto di n-gram di token. Strumento: `jscpd`
  se installato, altrimenti algoritmo manuale (hash di window di 30 token).
- Output: top-15 cluster di duplicazione, con paths e suggerimento di
  refactor (es. "estrai in modulo comune").
- Produce `code_integrity/05_duplication.md`

### Agent 6 — Anti-pattern e bug
- Pattern da cercare (regex grep ricorsivo, esclusi `.venv/` ecc.):
  - `bare except:` (Python anti-pattern)
  - `def fn(x=[])` (mutable default arg)
  - `eval(` `exec(` (security)
  - `os.system(` `subprocess.*shell=True` (shell injection)
  - hardcoded secret pattern `(api_key|password|token|secret)\s*=\s*["'][A-Za-z0-9_-]{16,}`
  - `TODO|FIXME|XXX|HACK` (technical debt count)
  - `pickle.loads(` (deserialization risk)
  - `assert` usato come check di runtime (Python optimize disables)
  - `print(` in moduli library (debug leftover)
- Per ogni pattern: file:line, severity (HIGH/MED/LOW), max 30 occorrenze
  per pattern.
- Produce `code_integrity/06_antipatterns.md`

## Coordinatore (tu)

Dopo che tutti i 6 sub-agent hanno consegnato:

1. **Aggregazione**: leggi i 6 file e produci `code_integrity/SUMMARY.md`
   (max 200 righe) con:
   - Top 5 issue cross-cutting (es. "32 bare excepts in pvnp_lab")
   - Per-system health score (su 5 scale: SEC, PvsNP Lab, ENTITY,
     sperimentalmath, altri) basato su (errors per LOC, dead-code ratio,
     antipattern density)
   - Top 10 file più problematici (ranked by total issues)
   - Quick wins: 5 fix che ridurrebbero il debito tecnico al 50% del lavoro
   - Discovery: cose inaspettate (es. ENTITY trovato in `<path>` con
     architettura X)

2. **Commit del report**: lo stage di tutti i file in
   `~/Scrivania/SEC/research/git_mirrors/SperimentalMath/audit/code_integrity/`,
   commit message: `audit: code integrity full scan (multi-agent)`,
   firma: `Signed: Ludovico Kubler`. Push origin/main.

3. **Final summary all'utente** (≤300 parole): top finding, dimensione
   del corpus scansionato, principali raccomandazioni.

## Note operative

- Stima budget tempo totale: 30-45 minuti. Se un agent supera 15 minuti,
  abortilo e fai con il dato parziale.
- Se l'agent inventory rivela >200K file source (improbabile), restringi
  a `~/Scrivania/SEC/` e `~/kissat/pvnp_lab/` solo, e nota la riduzione
  di scope nel SUMMARY.
- Tutti i sub-agent devono operare via `ssh ludo@sec` — il tuo ambiente
  locale è solo coordinatore.
- Se trovi codice che sembra essere parte del sistema **ENTITY** menzionato
  dall'utente ma non documentato, **flagga separatamente** in
  `code_integrity/00_DISCOVERIES.md` con descrizione di cosa hai trovato
  e dove.

## Output finale richiesto

- Cartella `audit/code_integrity/` in github SperimentalMath con 7 file
  markdown (00_DISCOVERIES, 01-06, SUMMARY).
- Commit + push fatto.
- Risposta finale all'utente con i 5 top finding e il link al SUMMARY.

Inizia ora.
