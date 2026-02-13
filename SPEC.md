# divineparadox TRACE (Spec)

This repository is a static research-oriented site. It hosts pre-generated JSON artifacts and renders them in the browser.

## Scope

- Demonstrate a trace-first interface for the `tac0de-cascade` protocol.
- Provide reproducible examples: `assets/tac0de/*.json`.
- Avoid server-side execution and avoid calling hosted models from the page.

## Trace Contract (high-level)

- Input: JSON
- Output: JSON (trace)
- Deterministic for a given implementation and input
- "Deep mode" is optional and should not perform external actions

## Non-goals

- Defining values, moral authority, or content filtering.
- Executing actions as a side effect of generating a trace.

