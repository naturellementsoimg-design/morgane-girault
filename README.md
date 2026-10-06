# Morgane Girault

Static bilingual website: English at `/`, explicit French switch to `/fr/` and corresponding pages. Vercel serves `public/`. This repository is `naturellementsoimg-design/morgane-girault`; Naturellement Soi is a separate repository and remains unchanged.

## Current positioning

The English market is served through personalised written work, with no live calls or appointments. The homepage leads with SoulMap and the reader’s life transition: feeling disconnected from herself, repeating patterns or outgrowing an old role. SoulMap Pro follows for women with a business or defined professional project. Both book covers supplied by Morgane appear on the homepage, their respective offer pages, social metadata and Stripe checkouts. Practical writing and website services come afterwards; music and paid songwriting remain visible further down the homepage, in navigation and footers.

The two SoulMap readings are adapted from the current personal and professional pages in Naturellement Soi, rather than merged into a single promise. Mediumship and energetic reading are explicit. The copy uses plain English phrases such as “personalised written soul reading”, “life transition”, “professional identity” and “recurring business patterns”. No keyword volumes or ranking claims are invented. First-party market wording was checked against [StarLore’s explanation of written PDF readings](https://www.starlorereadings.com/blog/how-written-pdf-readings-work/). Existing Ubersuggest quota limits prevented fresh volume or difficulty metrics.

## Offers and payment

| Offer | One-time price | Delivery |
|---|---:|---|
| SoulMap personal | 77 USD | Personal English PDF; within 7 business days after complete questionnaire and verified payment |
| SoulMap Pro — Out of the Fog | 144 USD | Professional English PDF; within 7–10 business days after complete questionnaire and verified payment |
| Professional Bio & Offer Writing | 111 USD | One bio and one existing offer; written brief and agreed correction round |
| Booking Flow Fix | 149 USD | One defined issue; scope and compatibility reviewed by email before payment |
| Custom lyrics / melody | Written quotation | Format, revisions, timing and usage rights agreed in writing |

New live Stripe products and Payment Links were created specifically for these English books, in USD. Existing Naturellement Soi EUR products and older session links were left intact.

- Personal: `https://buy.stripe.com/00w00c7DP5Uu9PUa4j8k83Q` (`prod_VOGOmrLfihGeF6`, `price_1UNTrZ2N8OzSgRf7Jubgwitc`, `plink_1UNTrj2N8OzSgRf719Ov5bhW`).
- Pro: `https://buy.stripe.com/4gMeV64rDfv43rw4JZ8k83R` (`prod_VOGm2XDajTN3MS`, `price_1UNUET2N8OzSgRf7HItH2AGN`, `plink_1UNUEk2N8OzSgRf7QFXkFiXN`).
- Bio retains Morgane’s supplied Stripe link. Booking fixes and music commissions begin with a written inquiry.

The French pages translate the presentation of this USD catalog; both SoulMap books in this catalog are written in English. The former career clarity and practical AI session pages redirect permanently to the relevant written catalog and are excluded from the sitemap.

## SoulMap fulfillment

Stripe redirects purchasers to `/post-achats/soulmap.html` or `/post-achats/soulmap-pro.html`. French questionnaire presentations are available at the corresponding `-fr.html` URL. These pages are noindex and excluded from the sitemap.

The questionnaire gathers all first names, surname, checkout email, birth date, time if known, city and country, current context and main question. Pro also requests the activity, offers and client context. An unknown birth time can be indicated explicitly. The form prepares a reviewable email draft with a copy fallback: **the visitor must send the email**. It does not upload, store or automatically email the answers. The recipient is `feminine.escapes.awakens@gmail.com`. General inquiries also prepare email drafts; WhatsApp remains available.

Fulfillment is manual. Morgane must match the email with the order, verify successful payment in Stripe, request missing information if needed, then prepare and email the PDF. A static success-page visit is not evidence of payment. There is no instant download, automated fulfillment or purchase-conversion event claimed by the site. Questionnaire data is not sent to analytics.

## Music support and analytics

The music support pages remain `/support.html` and `/fr/soutenir.html`, with Morgane’s circular portrait and the supplied Stripe contributions of 10, 20, 50 and 100 EUR. Support is linked from the main navigation, music pages and footers.

Every non-empty HTML page uses consent-gated GA4 `G-049S97BX69`. Google’s tag loads only after opt-in. Refusal, expiry and withdrawal are handled by the shared loader; ad consent stays denied. Form contents and URL queries are not sent to analytics. Privacy pages explain the draft-only SoulMap questionnaires.

## Edit and verify

Copy, routes and page generation live in `scripts/build_site.py`. Shared styling and draft preparation are in `public/assets/css/global.css` and `public/assets/js/main.js`. Original French architecture and legal sources are maintained in `scripts/legacy/`.

```sh
python3 scripts/build_site.py
python3 scripts/check_site.py
node --check public/assets/js/main.js
node --check public/assets/js/analytics.js
node tests/analytics.test.cjs
node tests/soulmap-draft.test.cjs
```

SEO includes 24 canonical bilingual public pages, reciprocal EN/FR/x-default links, descriptive metadata, Person/WebPage/Service/Breadcrumb structured data with exact USD prices, relevant book imagery, an XML sitemap and redirects for old routes. Post-purchase questionnaires remain noindex.
