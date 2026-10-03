# Morgane Girault

Static bilingual website: English at `/`, French at `/fr/`, explicit language switches on corresponding pages. Published files are in `public/`; Vercel is configured to serve that directory.

## Current services

| Service | Price | Delivery scope |
|---|---:|---|
| Intuitive Career & Business Clarity | 79 USD | Short questionnaire, 45-minute session, one-page synthesis, one next step |
| Professional Bio & Offer Writing | 119 USD | One bio and one existing offer; agreed correction round |
| Booking Flow Fix | 149 USD | One defined issue; compatibility and scope checked before payment |
| Practical AI | 99 USD | One task, a working session and a reusable process |
| Lyrics and melody commissions | Personal quote | Deliverables, language, revisions, timing and use agreed before payment |

The service buttons lead to contact, with the service preselected. USD payment links and the new session questionnaire are not yet connected. No existing EUR checkout is presented as a USD checkout. The contact form opens an email draft; it does not claim to submit through a backend. WhatsApp is also available.

## Edit and verify

Edit `scripts/build_site.py` for copy, routes and service definitions. Edit `public/assets/css/global.css` for styling and `public/assets/js/main.js` for navigation and the contact draft. The original French architecture essay and legal documents are preserved in `scripts/legacy/`; the full architecture essay remains published at its French approach URL.

```sh
python3 scripts/build_site.py
python3 scripts/check_site.py
node --check public/assets/js/main.js
python3 -m http.server 8765 --directory public
```

SEO includes self-canonical pages, reciprocal `en`/`fr`/`x-default` alternatives, descriptive metadata, Person/WebPage/Service/Breadcrumb structured data, an XML sitemap, useful internal links, redirects for older routes and noindex on existing post-purchase pages. Sitemap entries contain only the 22 public bilingual pages. Existing legal text has been preserved; English and French legal documents retain their own wording.

## Operational limits from the initial offer brief

These are internal planning limits, not additional customer-facing promises: clarity 1h15 total; bio/offer 1h30; booking fix 2h; practical AI 1h30. Confirm scope and delivery dates before payment for each digital intervention. Commission pricing and usage rights are determined in the written quotation.

Preliminary Ubersuggest research used English / United States as an international comparison: `career clarity`, `professional bio writing service` and `custom songwriting`. No search-volume or ranking promises are made to customers. Da Nang is a starting distribution channel; the services remain available internationally.
