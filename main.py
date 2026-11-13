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
        print(json.dumps(list(audit(csv.DictReader(stream))), indent=2))


if __name__ == "__main__":
    main()
