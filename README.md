# dMSA Delegation

Review OU delegation records for rights relevant to dMSA provisioning.

## Quick start

Use Python 3.10 or newer. The CLI runs locally with the standard library. From the repository root, run:

```sh
python3 main.py example.csv
```

The example surfaces the standard-tier helpdesk entry with an applicable CreateChild right and skips the privileged-tier entry.

## Input and output

| Input | Format | Output or purpose |
| --- | --- | --- |
| ACL CSV | `principal,ou,right,child_class,effect,inherited,tier` | Candidate allow entries for review |
| `right` | One resolved right per row | GenericAll, WriteDacl, WriteOwner, or applicable CreateChild |
| `child_class` | `*` or resolved LDAP class name | CreateChild class scope |

Results are JSON on stdout. Redirect to a file when you want to save the review.

## Interpreting results

This is triage over exported ACEs. Resolve GUIDs and composite masks before export. Group membership, deny entries, inheritance applicability, and actual DC patch state require separate review.

## Troubleshooting

- Use the included fixture first to confirm the command and working directory.
- Check the input path and required fields if the CLI exits with status 2.
- Keep real assessment exports and generated reports in your private workspace.

## Verify locally

```sh
python3 -m unittest discover -s tests -v
```
