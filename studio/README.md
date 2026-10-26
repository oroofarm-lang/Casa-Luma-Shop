# Casa Luma Shop Studio

Independent internal sourcing and purchasing workspace. All UI in English. Lives separately from the original public sourcing catalog at `docs/`.

## Deploy to Railway
1. Create a **private** Railway project connected to this GitHub repository; set service **Root Directory** to `/studio`.
2. Add a Railway **PostgreSQL** database and link `DATABASE_URL` to the web service.
3. Set a strong random `SESSION_SECRET` (32+ characters) in Railway Variables.
4. Set `OWNER_NAME` and `OWNER_PASSWORD` as one-time account bootstrap values. Choose a strong password (at least 12 characters). Remove `OWNER_PASSWORD` after successful first sign-in; changing it later does not reset the stored password.
5. Deploy, use the generated HTTPS domain, sign in as owner and add individual team members.
6. Optional: attach your own domain in Railway.

Only verified collaborators should know logins. Do not commit secrets. Team passwords are individually hashed; no plaintext passwords are stored. The owner may reset a teammate's password.

## Data model
Catalog of 154 sourcing leads is imported exactly once on initial empty database from `data/catalog-seed.json` with unverified reference prices distinct from confirmed order costs. Supplier directory imports 36 entries. Every catalog product starts in `Research` status with zero confirmed inventory. All records belong to this private workspace.

## Safety and migration
The original Higgsfield database had zero records in users/products/suppliers/tasks at time of inspection (2026-10-26); there are no real account/password hashes to migrate. Create new accounts. The preexisting GitHub Pages catalog remains unchanged. If you have unexported browser-local decisions from that catalog, export JSON locally before you stop using it.

## Local
Requires Node 20+ and PostgreSQL. Copy `.env.example` values into your execution environment (Node does not load .env automatically); run `npm install`, then `npm start`. The application requires `DATABASE_URL`, `SESSION_SECRET`, `OWNER_NAME`, and `OWNER_PASSWORD` for first-time setup.

API is same-origin, cookie authenticated, cross-site writes rejected, and all SQL uses bound parameters. Server reports `GET /health`.
