# Casa Shop Planning Studio (Solo Mode, v2)

Live path (once GitHub Pages publishes latest main/docs):
https://oroofarm-lang.github.io/Casa-Luma-Shop/solo-studio.html

## Two separate product areas

- **My Collection**: starts empty. Only the owner's newly added or explicitly selected products appear here. This is the only set counted on the Overview dashboard, Category Goals and Orders.
- **Product Research**: 154 pre-existing ideas across 13 English categories. Browse, filter and click **+ Add to my shop** to copy one into My Collection. The original research item stays in the library.
- The separate Suppliers directory retains the 36 research suppliers.

## Add items by product link

On **My Collection**, paste a Lazada, SHEIN or other product page URL and click **Read product link**. This opens an editable product form and attempts to fill the product name, seller/domain, image, unverified reference price and notes. The user can also press **Add product** and fill fields manually.

The page extraction is a best-effort feature using Jina Reader (`r.jina.ai`), a third-party service. The product URL is sent to Jina Reader only when the user clicks to fetch it. This depends on CORS support and whether a shop permits automated access. Lazada, SHEIN and dynamically loaded storefronts may refuse access; image and prices may be absent or inaccurate. If extraction fails, the pasted URL remains and the user can fill the other fields. **Always review variants, stock, price, currency, delivery and tax invoice with the supplier.** No orders are submitted automatically.

## Saving, backups, and future team migration

- Edits save in this browser's localStorage only, not to GitHub or a database.
- Visit **Backups** and download a full JSON backup regularly (includes separate Collection and Research, suppliers, tasks and category targets).
- Restore from both older v1 backups and v2 backups; previous manually added products from v1 are migrated into My Collection without dropping research products.
- CSV export includes **My Collection only**, not all research leads.
- There are no invitations and no shared live team edits in Solo Mode.
- GitHub Pages URL and baseline product research are **publicly reachable**. The app is not password protected. Do not enter private company data or contact details until private hosting is ready.
- Once private hosting becomes available, import the latest backup into a private authenticated database and test everything before sending team invitations.

Files:
- `docs/solo-studio.html` entry HTML.
- `docs/solo-v2-app.js` active JS, v1 preserved separately.
- `docs/solo-style.css` styling.
- `docs/solo-seed.json` 154 research leads and 36 suppliers.
