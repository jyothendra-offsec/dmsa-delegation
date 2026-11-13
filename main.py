"""Triage exported OU delegations that could affect dMSA provisioning."""
import argparse
import csv
import json

RELEVANT = {"genericall", "writedacl", "writeowner"}


def audit(entries):
    for row in entries:
        right = row["right"].strip().casefold()
        child = row["child_class"].strip().casefold()
        if row["effect"].strip().casefold() != "allow":
            continue
        if row["tier"].strip().casefold() == "privileged":
            continue
        if right in RELEVANT or (right == "createchild" and child in
                                 {"*", "msds-delegatedmanagedserviceaccount"}):
            yield dict(principal=row["principal"], ou=row["ou"], right=row["right"],
                       child_class=row["child_class"], inherited=row["inherited"],
                       status="review-effective-access")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("acl_csv")
    args = parser.parse_args()
    with open(args.acl_csv, encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"principal", "ou", "right", "child_class", "effect", "inherited", "tier"}
        missing = required - set(reader.fieldnames or ())
        if missing:
            raise ValueError(f"missing CSV columns: {', '.join(sorted(missing))}")
        print(json.dumps(list(audit(reader)), indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, AttributeError, IndexError, csv.Error) as exc:
        import sys

        print(f"Invalid input: {exc}", file=sys.stderr)
        raise SystemExit(2) from None
