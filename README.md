# divine paradox

A tiny, static site for the tac0de philosophy.

- tac0de ai: mastermind architecture (Deep mode is optional)
- tac0de-cascade: Deep Thinking protocol language (Trace-only, no side effects)

This site is intentionally simple.

## Live demo

GitHub Pages: https://tac0de.github.io/divineparadox/

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

## Optional: OpenAI via GCP bridge (no OpenAI key in Netlify)
If you want to call OpenAI without storing `OPENAI_API_KEY` in Netlify, you can:
- deploy a bridge on GCP Cloud Run (stores `OPENAI_API_KEY` in GCP Secret Manager),
- keep only a short `DEPLOY_TOKEN` in Netlify env vars,
- forward requests from a Netlify Function to the GCP bridge.

Netlify env vars:
- `OPENAI_BRIDGE_URL` = your Cloud Run base URL (example: `https://openai-bridge-xxxxx-<region>.a.run.app`)
- `DEPLOY_TOKEN` = the shared Bearer token used to call the bridge

Netlify function:
- `POST /.netlify/functions/openai_responses` forwards to `${OPENAI_BRIDGE_URL}/v1/responses`.
