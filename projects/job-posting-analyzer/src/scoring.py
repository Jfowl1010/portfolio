def _cap_reasons(reasons):
    if len(reasons) < 2:
        reasons.append(
            "Conservative default: treat as non-entry-level unless clearly signaled."
        )
    return reasons[:5]


def score(signals):
    senior_signals = signals.get("senior_signals", [])
    entry_signals = signals.get("entry_signals", [])
    min_years = signals.get("min_years")

    reasons = []

    if senior_signals:
        verdict = "NO-GO"
        reasons.append(
            f"Seniority signal detected: {', '.join(senior_signals[:2])}."
        )
        if min_years is not None:
            reasons.append(f"Minimum years required: {min_years}.")
        else:
            reasons.append("Senior roles are not entry-level by default.")
        return {"verdict": verdict, "reasons": _cap_reasons(reasons)}

    if min_years is not None and min_years >= 3:
        verdict = "NO-GO"
        reasons.append(
            "Experience requirement exceeds entry-level threshold (>=3 years)."
        )
        if entry_signals:
            reasons.append(
                "Entry-level signals present, but years requirement is too high."
            )
        else:
            reasons.append("No strong entry-level signals to offset experience.")
        return {"verdict": verdict, "reasons": _cap_reasons(reasons)}

    if entry_signals and (min_years is None or min_years <= 2):
        verdict = "GO"
        reasons.append(
            f"Entry-level signal detected: {', '.join(entry_signals[:2])}."
        )
        if min_years is None:
            reasons.append("No explicit years requirement found.")
        else:
            reasons.append(f"Years requirement within entry-level range: {min_years}.")
        return {"verdict": verdict, "reasons": _cap_reasons(reasons)}

    verdict = "NO-GO"
    if min_years is None:
        reasons.append("No explicit years requirement found.")
    else:
        reasons.append(f"Minimum years required: {min_years}.")
    if entry_signals:
        reasons.append("Entry-level signals are insufficient to be decisive.")
    else:
        reasons.append("No entry-level signals detected; conservative default applies.")
    return {"verdict": verdict, "reasons": _cap_reasons(reasons)}
