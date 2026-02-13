#!/usr/bin/env python3
"""
tac0de-cascade (minimal local implementation)

This is a trace generator for the "Deep mode contract":
- Input: structured JSON (prompt + claims/assumptions/open_questions)
- Output: trace JSON scaffold (no side effects, no external calls)

This file exists to make the demo reproducible even when the real
`tac0de-cascade` binary is not installed.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List


def _as_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        out: List[str] = []
        for item in value:
            if item is None:
                continue
            out.append(str(item))
        return out
    return [str(value)]


def _classify_domain(prompt: str, claims: List[str], assumptions: List[str], open_questions: List[str]) -> str:
    text = " ".join([prompt] + claims + assumptions + open_questions).lower()

    devops_markers = [
        "github",
        "pages",
        "workflow",
        "actions",
        "ci",
        "deploy",
        "deployment",
        "branch protection",
        "cancelled",
        "concurrency",
        "check run",
        "merge",
        "required checks",
    ]
    if any(m in text for m in devops_markers):
        return "devops"

    return "general"


def generate_trace(input_obj: Dict[str, Any]) -> Dict[str, Any]:
    prompt = str(input_obj.get("prompt", "")).strip()
    claims = _as_list(input_obj.get("claims"))
    assumptions = _as_list(input_obj.get("assumptions"))
    open_questions = _as_list(input_obj.get("open_questions"))

    domain = _classify_domain(prompt, claims, assumptions, open_questions)

    if domain == "devops":
        contradiction_findings = [
            "If cancellations are common, using a cancelled check as a merge gate contradicts the goal of avoiding blocks on non-failures.",
            "A cancelled Pages run is weak evidence: treat the latest successful deploy (or environment URL) as the source of truth, especially during outages.",
        ]
        bias_notes = [
            "Automation bias: assuming the CI system is 'right' can downplay contributor confusion; treat clarity as a first-class requirement.",
            "Availability bias: a recent success can hide intermittent failures; ensure cancellations do not mask real build regressions.",
        ]
        dignity_notes = [
            "Assume contributors act in good faith; wording should explain cancellations as expected concurrency behavior, not blame.",
            "Provide concrete next steps (where to find the latest successful run/deploy URL) instead of vague 'check Actions' instructions.",
        ]
        harm_risks = [
            "A cancelled run may be misread as a failure, wasting maintainer time and reducing contributor trust.",
            "Cancellations can hide flaky failures unless the 'latest successful deploy' signal is obvious and easy to locate.",
            "Disabling cancellation may increase queue time and CI spend without meaningful reliability gains.",
        ]
        counterfactual = {
            "opposite_position": "Treat any cancellation as a deployment integrity risk; disable cancellation and require every Pages build to complete.",
            "strongest_argument": "Cancellations can reduce observability and mask flaky failures; forcing completion improves auditability and simplifies debugging.",
        }
        synthesis = {
            "minimize_harm": (
                "Keep cancellation behavior, but prevent it from blocking merges: do not require a cancelled check as a gate. "
                "Add a short README/CONTRIBUTING note: cancellations can occur when a newer Pages request is queued. "
                "Point to the latest successful run/deploy URL as the source of truth."
            ),
            "preserve_dignity": (
                "Normalize the cancelled outcome in documentation and status messaging; focus on guidance and remediation, not fault."
            ),
            "tradeoffs": [
                "Clarity vs. minimalism in docs",
                "Observability vs. CI cost/latency",
                "Strict gating vs. developer velocity",
            ],
        }
    else:
        contradiction_findings = [
            "Possible contradiction: goals, constraints, and values may be interleaved; separate them explicitly before selecting actions."
        ]
        bias_notes = [
            "Bias check: restate the prompt in neutral terms; watch for framing that privileges a default viewpoint."
        ]
        dignity_notes = [
            "Dignity check: describe stakeholders with agency and respect; avoid coercive framing."
        ]
        harm_risks = [
            "Harm projection: list plausible downstream harms (direct and indirect) if the chosen action is taken."
        ]
        counterfactual = {
            "opposite_position": "Avoid synthesis and keep competing positions separate until constraints are clarified.",
            "strongest_argument": "Premature synthesis can hide tradeoffs and increase the risk of avoidable harm.",
        }
        synthesis = {
            "minimize_harm": "Minimize harm by validating constraints early, documenting uncertainties, and choosing the least irreversible steps.",
            "preserve_dignity": "Preserve dignity by using respectful language and incorporating affected parties' perspectives.",
            "tradeoffs": [
                "Speed vs. thoroughness",
                "Strict validation vs. flexibility",
            ],
        }

    return {
        "claims": claims,
        "assumptions": assumptions,
        "contradiction_scan": {"findings": contradiction_findings},
        "bias_check": {"notes": bias_notes},
        "dignity_check": {"notes": dignity_notes},
        "harm_projection": {"risks": harm_risks},
        "counterfactual": counterfactual,
        "synthesis": synthesis,
        "open_questions": open_questions,
    }


def cmd_trace(args: argparse.Namespace) -> int:
    with open(args.input_json, "r", encoding="utf-8") as f:
        input_obj = json.load(f)

    if not isinstance(input_obj, dict):
        raise SystemExit("Input must be a JSON object.")

    trace = generate_trace(input_obj)
    json.dump(trace, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(prog="tac0de-cascade")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_trace = sub.add_parser("trace", help="Generate a trace JSON from input JSON.")
    p_trace.add_argument("input_json", help="Path to input JSON.")
    p_trace.set_defaults(func=cmd_trace)

    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

