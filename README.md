# Casa Luma Shop

Sourcing storefront, shopping cart, saved purchase-order drafts and purchasing workspace for Casa Luma, Koh Phangan, Thailand 84280.

## Open and share

Published catalog: https://oroofarm-lang.github.io/Casa-Luma-Shop/

The catalog includes 154 products and leads across 13 categories. Use English for employee handoff and English or Thai supplier order drafts. Prices and promotions are observations, not live quotes. Shipping and invoice eligibility require supplier confirmation.

Choices are saved in each browser, not synchronized between users. Export an employee HTML snapshot or JSON work file to transfer selections. No order is sent automatically.

## Project knowledge

Resume with [handoff](handoff.md), [project map](MAP.md) and [current tasks](entities/casa-luma/tasks.md). Context organization is complete; authenticated shared cart and orders are approved, with local code present and production deployment still unverified. See the [organization report](vault/Context-Organization-Report-2026-10-20.md).

Architecture: [Internal purchasing storefront](vault/Internal-Shop-Architecture.md).

Start with [Vault Home](vault/Home.md) and [Ordering Guide](research/Ordering-Guide.md).

## Update the hosted catalog

The published site is only `docs/`. After rebuilding the research catalog, copy `research/order-page.html` to `docs/index.html`, commit and push. GitHub Pages publishes main /docs.

Original conversations, presentations, PDFs, private backups and extracted source text are excluded from this public repository. A full local ZIP backup is stored in `backups/`; keep it in private storage.

## Local requisition and supplier verification

Updated 23 October 2026: budget estimates are locked by default. Transfer selected cart rows as frozen requisitions, complete the employee supplier checklist, then submit for owner approval. Final supplier prices are separate from the original estimates. See [workflow and validation](vault/Procurement-Verification-Workflow.md). This local implementation has not been verified as a live shared deployment.

```sh
python3 research/order_renderer.py --copy-to-docs
node research/test-order-core.cjs
.venv/bin/python -m unittest server.test_app -v
```

The renderer updates local HTML only. It does not publish or contact suppliers. HTTP tests require the server requirements plus `httpx` in a local virtual environment and use isolated synthetic users and SQLite.
