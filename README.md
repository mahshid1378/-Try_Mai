# Linear Interpolation — Implementation Comparison

Linear interpolation implemented by **three different LLM models** —
**MAI-Code-1-Flash**, **GPT 5.5**, and **Claude Opus 4.8** — each producing its
own demo in its own directory. The three implementations were then evaluated by
three independent LLM judges on **completeness**, **correctness**, and
**succinctness**.

## Prompt

Each model was given the same task (with its own target directory name):

> In a new directory named `<model>`, create sample data and a script to
> demonstrate linear interpolation. Do not reference and be influenced by any
> existing scripts in the working directory.

The judging step used the following prompt:

> You are an unbiased LLM judge. Review all 3 implementations of linear
> interpolation in the current working directory and vote on completeness,
> correctness and succinctness.

## Implementations

| Source | Model | Script | Data | Out-of-range | Lookup | Demo queries |
|--------|-------|--------|------|--------------|--------|--------------|
| **mai** | MAI-Code-1-Flash (Medium thinking) | [mai/interpolate.py](mai/interpolate.py) | 3 pts | raises `ValueError` | linear scan | 1 |
| **codex** | GPT 5.5 (Medium thinking) | [codex/linear_interpolation.py](codex/linear_interpolation.py) | 5 pts | raises `ValueError` | linear scan | 4 |
| **claude** | Claude Opus 4.8 | [claude/linear_interpolation.py](claude/linear_interpolation.py) | 11 pts | clamps to endpoint | `bisect` (O(log n)) | 8 |

All three share the same core formula and were verified to run successfully:

```
y = y0 + (y1 - y0) * (x - x0) / (x1 - x0)
```

## Consolidated Judge Results

Each judge's vote per category ([judge/claude.json](judge/claude.json),
[judge/codex.json](judge/codex.json), [judge/mai.json](judge/mai.json)):

| Category | claude (judge) | codex (judge) | mai (judge) | **Verdict** |
|----------|:--------------:|:-------------:|:-----------:|:-----------:|
| Completeness  | claude | claude | claude | **claude** (unanimous) |
| Correctness   | codex  | codex  | codex  | **codex** (unanimous) |
| Succinctness  | mai    | mai    | mai    | **mai** (unanimous) |
| Overall       | codex  | codex  | — | **codex** |

### Overall winner: **codex** 🏆

The judges were unanimous on every category and on the overall winner. Codex
strikes the best balance — correct with the most robust input validation
(explicit range and minimum-point guards), complete enough to be genuinely
demonstrative, and still concise.

## Per-Implementation Summary

- **codex** (GPT 5.5, Medium thinking) — *Best overall & most correct.* Standard
  formula, sorts input, validates dataset size and range with helpful error
  messages, handles exact endpoint matches. Lean and well-structured.
- **claude** (Claude Opus 4.8) — *Most complete.* Docstrings explaining the math,
  the largest dataset, a formatted result table, and demonstrated edge cases
  (out-of-range, exact match). Drawbacks: least succinct and silently *clamps*
  out-of-range inputs, which is debatable semantics for strict interpolation.
- **mai** (MAI-Code-1-Flash, Medium thinking) — *Most succinct.* The tightest
  script, but the least complete: a single in-range demo value and no guard for
  empty / single-point datasets.

## Running

```bash
python mai/interpolate.py
python codex/linear_interpolation.py
python claude/linear_interpolation.py
```
