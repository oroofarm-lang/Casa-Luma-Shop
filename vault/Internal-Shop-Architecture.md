# Casa Luma — Internal purchasing storefront

## Purpose and experience

A curated purchasing store for the owner and employee: browse → edit unit price/variant → add to cart → review selected rows → prepare separate supplier/channel drafts → track the employee's actions. The Casa Luma cream, sand, charcoal and sage identity is retained. Prices are THB only; 250 THB is a warning/filter, not an arbitrary ban.

The price input appears directly on **every product card before adding to cart**, with a second editable price in every cart row. The supplier's observed reference price is a separate, dated label. Product draft changes do not silently rewrite existing cart rows or historic orders.

## Boundaries

The deployed GitHub Pages frontend and its catalog are public. Actual cart, buyer information and order history stay in browser storage or explicitly exported files. This implementation does not claim authentication, access restriction or multi-user synchronization. A question about shared authenticated work versus local-file handoff was sent to the owner; no answer has been assumed.

No payment, supplier message, tax invoice or marketplace purchase is sent or created automatically. “Sent”, “confirmed” and “ordered” are employee-reported tracking states.

## Runtime layers

1. **Catalog repository**: `research/catalog-data.json`, rebuilt into standalone HTML. Stable product IDs; identified supplier channels; evidence dates; source links. Factory identity, invoice eligibility and island delivery remain separately unverified where noted.
2. **Domain service**: `research/order-core.js`, browser-independent. Validates quantities, sources, THB prices and variants; separates cart from product draft and order snapshot; splits checkout by the actual supplier plus channel.
3. **Workspace repository**: version-2 local-storage document, JSON backup/import and employee snapshot. Compatible with prior work files. Three save/reload rounds cover both old selections and saved purchase orders.
4. **Storefront presentation**: `research/order-page.js`, `.css`, `.html.in`, rendered by `order_renderer.py`. Product, Cart, Orders and Suppliers views; Hebrew/English UI; English/Thai supplier messages. Responsive layout.
5. **Publishing**: complete local HTML and identical `docs/index.html`; GitHub Pages publishes only `/docs`.

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

## Authenticated shared deployment — next architecture if selected

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

A hosting provider, login method and shared-workspace requirement must be selected before this service is provisioned. The current static site is not mislabeled as that completed deployment.
