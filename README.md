# divine paradox

A tiny, static site for the tac0de philosophy.

- tac0de ai: mastermind architecture (Deep mode is optional)
- tac0de-cascade: Deep Thinking protocol language (Trace-only, no side effects)

This site is intentionally simple.

## tac0de-cascade (static attachment)

This site includes a pre-generated tac0de-cascade trace under `assets/tac0de/`.

Regenerate:

```bash
./scripts/gen-tac0de-trace.sh
```

If you do not have `tac0de-cascade` on your PATH, set `TAC0DE_CASCADE_MANIFEST`:

```bash
export TAC0DE_CASCADE_MANIFEST=/path/to/tac0de-cascade/Cargo.toml
./scripts/gen-tac0de-trace.sh
```

View locally (required for `fetch()` to work):

```bash
python3 -m http.server 8000
```
