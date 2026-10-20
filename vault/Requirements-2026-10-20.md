# Purchasing requirements — 20 October 2026

Implemented in the local and hosted catalog:

- THB only; foreign-currency references become unpriced and require a THB supplier quotation. Previous approvals involving foreign prices return to shortlist.
- 250 THB budget per order unit, inclusive at 250; filters for within / over / missing price, with over-budget warnings in cards, order rows and supplier messages.
- Editable manual line prices and price-basis selection.
- Reversible local product deletion; deletes order lines, does not delete other users’ data or shared catalog sources.
- Named clickable platform, email and phone links; a Lazada link on every product and supplier row. Unlocated direct shops use an explicitly unverified search, never an invented official shop. Staff may enter a Lazada link.
- Editable stock availability, invoice status/type and supplier notes, with update timestamp. Out-of-stock blocks approval; preorder invalidates old approval.
- State round trips through browser persistence and JSON; employee snapshots carry these fields. CSV includes status fields. This remains a static site without live multi-user synchronization.

Sources for new supplier channels:
- https://phutawanshop.com/en/store-branch/
- https://linktr.ee/Elegant_Kids

Existing product price observation dates were preserved. Discovering a shop link does not confirm its stock, checkout price, invoice capability or Koh Phangan delivery.
