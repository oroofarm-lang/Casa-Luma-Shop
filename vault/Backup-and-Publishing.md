# Backup and publishing

Public Git repository: https://github.com/oroofarm-lang/Casa-Luma-Shop

The documented GitHub Pages source is main branch, `/docs`. Only public catalog artifacts belong there; the shared server requires separate hosting. No push, publication or remote-settings check was performed during the closing documentation work in steps 6–9.

## Private local backups — verified 20 October 2026

- `../_backup-Casa-Luma-Shop-2026-10-20/`: full pre-organization copy. All 188 file entries currently match the sizes and SHA-256 values in `BACKUP-MANIFEST.json`; zero mismatches. This verifies the saved snapshot, not equality with the now-edited project.
- `backups/Casa-Luma-full-backup-2026-10-19.zip`: older private archive, 22,505,503 bytes and 25 ZIP entries. ZIP CRC testing passed. It predates the current organization work and is not a backup of these latest edits.
- Public Git snapshot from step 1: commit `b478c1a356a2246c9ba938984a7b271f203f1df9`. The current local branch and locally cached origin reference for `backup/casa-luma-2026-10-20-step1` point to `0bbd99a416e3449d588038644e797431020ff077`. No fresh remote verification was performed. Public Git is not a substitute for the private full backup.

The latest context-organization edits remain local and uncommitted; neither older backup contains them. Keep private originals and archives out of the public repository. For audit details, see [organization report](Context-Organization-Report-2026-10-20.md).

## Workspace data

Browser choices require an explicit JSON export; these filesystem backups do not capture browser storage. A different site origin has separate browser storage. Shared-mode production data will require private database backups and restore testing after provisioning; no such operational backup is claimed here.
