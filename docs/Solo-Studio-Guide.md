# Casa Shop Planning Studio (Solo Mode)

This is the owner's **draft-only**, English-language product planning studio. No account invitation, order placement, or collaboration occurs here.

## Open
GitHub Pages path after Pages deployment updates:
https://oroofarm-lang.github.io/Casa-Luma-Shop/solo-studio.html

Files:
- `docs/solo-studio.html`: entry page
- `docs/solo-style.css`: styling
- `docs/solo-app.js`: solo editing functions
- `docs/solo-seed.json`: baseline of 154 sourcing leads, 36 suppliers, 3 draft tasks

## Working solo
- Categorize, add and edit products and suppliers.
- Change planning status and order stage.
- View category balance; define category targets.
- Keep a planning checklist.
- Download a complete JSON backup from **Backups** regularly.
- Import a previous JSON backup to resume a draft in another browser.

## Important privacy and persistence limits
GitHub Pages serves public documents. The **page and initial public sourcing seed are publicly reachable** by anyone with the URL. The user's edits are NOT saved to GitHub: they stay in that browser's localStorage until exported. Do not store confidential information in this version. This is NOT a private authenticated app. It does not sync between devices and will lose local edits if browser storage is cleared without backup. Do not invite team members before moving to private authenticated hosting.

## Future migration
Import the latest solo JSON backup into a private centralized database once Railway (or another host) is connected and working. The independent server draft in `studio/` exists but has not yet been deployed or tested end-to-end. These are two separate phases.
