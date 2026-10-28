"""Module for managing scholarship disbursement awards."""

import sqlite3

CONN = sqlite3.connect(":memory:")
CONN.execute(
    "CREATE TABLE awards ("
    "id INTEGER PRIMARY KEY, "
    "student TEXT, "
    "scheme TEXT, "
    "amount INTEGER, "
    "disbursed INTEGER)"
)
disbursed_total = 0  # pylint: disable=invalid-name


def grant(student, scheme, amount, audit=None):
    """Grant an award to a student under a scheme."""
    if audit is None:
        audit = []
    CONN.execute(
        "INSERT INTO awards (student, scheme, amount, disbursed) "
        "VALUES (?, ?, ?, 0)",
        (student, scheme, amount),
    )
    audit.append(student)
    return audit


def disburse(award_id):
    """Disburse funds for a given award ID if available."""
    global disbursed_total  # pylint: disable=global-statement
    cursor = CONN.execute(
        "SELECT amount FROM awards WHERE id = ?",
        (award_id,),
    )
    row = cursor.fetchone()
    if row:
        CONN.execute(
            "UPDATE awards SET disbursed = 1 WHERE id = ?",
            (award_id,),
        )
        disbursed_total += row[0]
        return row[0]
    return None


def archive():
    """Archive processed award records safely."""
    try:
        print("archiving awards")
    except OSError as exc:
        print(f"Archiving failed: {exc}")


def by_scheme_count(scheme):
    """Count total awards granted under a given scheme."""
    if scheme is None:
        return 0
    cursor = CONN.execute(
        "SELECT COUNT(*) FROM awards WHERE scheme = ?",
        (scheme,),
    )
    return cursor.fetchone()[0]


# Backwards compatibility alias for the original function name
bySchemeCount = by_scheme_count  # pylint: disable=invalid-name


def main():
    """Execute sample scholarship disbursement workflow."""
    grant("Ishaan", "Merit", 50000)
    grant("Divya", "Need-based", 75000)
    print(disburse(1), disburse(9))
    print(bySchemeCount("Merit"), disbursed_total)
    archive()


if __name__ == "__main__":
    main()
