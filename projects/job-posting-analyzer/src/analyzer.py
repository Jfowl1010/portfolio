import argparse
import os
import sys

try:
    import exctract
    import scoring
except ImportError:  # pragma: no cover - fallback for direct execution
    from . import exctract  # type: ignore
    from . import scoring  # type: ignore


def _format_experience(signals):
    parts = []
    min_years = signals.get("min_years")
    max_years = signals.get("max_years")
    if min_years is not None:
        if max_years is not None and max_years != min_years:
            parts.append(f"Years required: {min_years}-{max_years}")
        elif max_years is not None:
            parts.append(f"Years required: {min_years}")
        else:
            parts.append(f"Years required: {min_years}+")
    if signals.get("senior_signals"):
        parts.append(
            "Seniority signals: " + "; ".join(signals.get("senior_signals", []))
        )
    if signals.get("entry_signals"):
        parts.append(
            "Entry-level signals: " + "; ".join(signals.get("entry_signals", []))
        )
    if not parts:
        return "None"
    return " | ".join(parts)


def format_report(skills, signals, verdict):
    lines = []
    if skills:
        lines.append("Skills detected: " + ", ".join(skills))
    else:
        lines.append("Skills detected: None")
    lines.append("Experience signals: " + _format_experience(signals))
    lines.append(f"VERDICT: {verdict['verdict']}")
    lines.append("Reasons:")
    for reason in verdict.get("reasons", []):
        lines.append(f"- {reason}")
    return "\n".join(lines)


def analyze_text(text):
    skills = exctract.extract_skills(text)
    signals = exctract.extract_signals(text)
    verdict = scoring.score(signals)
    return format_report(skills, signals, verdict)


def analyze_file(path):
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        return analyze_text(handle.read())


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Analyze a .txt job posting for skills and entry-level signals."
    )
    parser.add_argument("path", help="Path to a .txt job posting file")
    args = parser.parse_args(argv)

    if not args.path or not os.path.isfile(args.path):
        print("Error: input file not found. Provide a valid .txt file path.", file=sys.stderr)
        return 1

    if not args.path.lower().endswith(".txt"):
        print("Error: input must be a .txt file.", file=sys.stderr)
        return 1

    try:
        report = analyze_file(args.path)
    except OSError as exc:
        print(f"Error: unable to read file ({exc}).", file=sys.stderr)
        return 1

    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
