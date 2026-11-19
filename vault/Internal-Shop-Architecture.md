# Casa Luma — Internal purchasing storefront

## Purpose and experience

A curated purchasing store for the owner and employee: browse → deliberately unlock a budget estimate if needed → add variants and quantities to cart → transfer locked requisitions by supplier/channel → employee supplier verification → owner final approval. The Casa Luma cream, sand, charcoal and sage identity is retained. Prices are THB only; 250 THB is a warning/filter, not an arbitrary ban.

The price input appears directly on **every product card before adding to cart**, with a second estimate in every cart row; both are read-only until deliberately unlocked. The employee records final prices in a separate supplier checklist. The supplier's observed reference price is a separate, dated label. Product draft changes do not silently rewrite existing cart rows or historic orders.

## Approved target and current status

The owner selected authenticated shared work: one cart and order workspace for owner and employee. This decision supersedes the earlier open question about local-file handoff.

The existing GitHub Pages catalog is public and static. In static mode, cart, buyer information and order history stay in browser storage or explicitly exported files; GitHub Pages does not provide authenticated shared storage. The live website was not rechecked during this documentation work.

Local shared-mode code exists in `server/app.py` and `research/order-page.js`. It has not been verified here as a production deployment. No production accounts, durable cloud database or successful live synchronization are claimed.

No payment, supplier message, tax invoice or marketplace purchase is sent or created automatically. “Sent”, “confirmed” and “ordered” are employee-reported tracking states.

## Runtime layers

1. **Catalog repository**: `research/catalog-data.json`, rebuilt into standalone HTML. Stable product IDs; identified supplier channels; evidence dates; source links. Factory identity, invoice eligibility and island delivery remain separately unverified where noted.
2. **Domain service**: `research/order-core.js`, browser-independent. Validates quantities, sources, THB prices and variants; separates cart from product draft and order snapshot; splits checkout by the actual supplier plus channel.
3. **Workspace repository**: version-2 local-storage document, JSON backup/import and employee snapshot. Compatible with prior work files. Three save/reload rounds cover both old selections and saved purchase orders.
4. **Storefront presentation**: `research/order-page.js`, `.css`, `.html.in`, rendered by `order_renderer.py`. Product, Cart, Orders and Suppliers views; Hebrew/English UI; English/Thai supplier messages. Responsive layout.
5. **Publishing**: local HTML and `docs/index.html` are identical in the 20 October file audit; the documented GitHub Pages target is main `/docs`. Local equality does not verify the deployed website.
6. **Shared-mode code**: FastAPI serves authenticated pages and a versioned workspace API; the frontend has shared save/refresh/conflict handling. The server stores workspace JSON, revisions, request IDs and audit events. SQLite is available locally; production mode requires PostgreSQL via `DATABASE_URL`. This describes code present, not a verified live service.

## Entities and ownership

| Entity | Key | Fields and invariant |
|---|---|---|
| CatalogProduct | stable product ID | name, SKU, category, sources, reference THB price, images, evidence; source observations are not editable supplier quotes |
| SupplierChannel | supplier + channel | seller identity, product/store URL, contact; unverified marketplace sellers remain separate |
| ProductDraft | product ID in workspace | chosen channel, unit price, quantity, unit, model, size, colour, pack, note; editing does not add to cart |
| CartLine | generated line ID | copied draft, selected flag; identical variant/price/source merges quantities; different variants remain distinct |
| SupplierFacts | product ID in workspace | stock, invoice status/type, supplier notes, timestamp; reported by team, not automatically verified |
| OrderBatch | batch ID | one checkout action, split into separate PurchaseOrders |
| PurchaseOrder | generated order ID and number | supplier/channel, immutable product/source/line snapshots, buyer/delivery snapshot, creation time, kind=order/quote, mutable tracking state |

## Checkout rules

- Only selected cart rows are processed. Excluded rows stay in the cart.
- A purchase-order draft requires valid source, positive integer quantity, valid THB price, non-out-of-stock status and product variant details. Clothing needs a size (including an explicitly confirmed one-size option).
- Missing prices or model details can be handled through **quotation requests**, clearly worded as not being confirmed purchase orders.
- Cart grouping is a viewing choice. Supplier messages always split by actual supplier/channel, even when cart is grouped by category or promotion.
- Successful purchase-order preparation moves selected rows into order history. Quotation requests retain the cart rows for later confirmation.
- Order snapshots retain the exact price, variant, source and buyer details at creation. Later catalog/cart edits cannot rewrite them.
- Repeat-order action adds copied variants to the current cart as reference prices, requiring a fresh review.

## Authenticated shared deployment — approved direction

The following is the target architecture and review checklist. It is not a list of completed server features: the current server stores one versioned workspace JSON document rather than the normalized business tables proposed below. Validate authorization, transaction boundaries and retry behavior before production deployment.

Use the same domain boundaries with an authenticated API and transactional database instead of publishing workspace JSON:

- Web frontend → session-authenticated API → PostgreSQL.
- Tables: organizations, memberships, catalog_products, suppliers, supplier_channels, product_drafts, carts, cart_lines, order_batches, purchase_orders, order_lines, supplier_facts, audit_events.
- Every business row is scoped to organization_id; API checks membership, object ownership and permissions on every read/write.
- Owner manages product overrides and preparation permissions. Employee can edit assigned draft orders, stock/invoice facts and tracking status. No anonymous access to buyer, cart, messages or orders.
- Optimistic versions/ETags avoid overwriting concurrent employee edits. Conflicts are shown explicitly.
- Transactional checkout takes a locked cart revision, creates immutable order snapshots and removes exactly the processed lines in one transaction. Idempotency keys prevent duplicate orders after retries.
- HTTPS, secure HttpOnly session cookies, CSRF protection for mutations, login rate limits and server-side input validation. No keys in public HTML.
- Database backups and restore testing; private invoice attachments with authorized downloads and retention policy. Audit history records actor, object, changed fields and time.
- Source-marketplace price/stock scraping is not represented as live integration. Only explicit future connectors or team-entered verified data should change those facts.

Shared work is selected. Hosting, durable database operations, production account setup and deployment verification remain pending. The local implementation uses password login and sessions; its production readiness still requires review and full two-user verification. See [current tasks](../entities/casa-luma/tasks.md).

## Procurement verification update — 23 October 2026

The local implementation now separates frozen requisition estimates from supplier-confirmed final prices. See [workflow, permissions and validation evidence](Procurement-Verification-Workflow.md). New requisitions cannot reach final approval without the mandatory checklist. `server/procurement.py` independently checks transitions and owner permissions. Eight HTTP integration tests use synthetic owner/employee accounts; browser completion and production deployment remain unverified. Rebuild only the storefront with `python3 research/order_renderer.py --copy-to-docs`; this updates local artifacts without publishing.
