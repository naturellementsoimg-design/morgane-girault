# Morgane Girault

Static bilingual website: English at `/`, French at `/fr/`, explicit language switches on corresponding pages. Published files are in `public/`; Vercel is configured to serve that directory.

## Homepage and offer presentation

The homepage leads with the visitor's career or business problem, identifies creatives, practitioners and independent professionals as the audience, and links directly to the four services. The offer cards show the starting problem, concrete output and price together. Morgane's mediumship and energetic reading are explicit in the career clarity offer; music, listening and paid songwriting commissions follow the services and introduction. Work with me comes before Music in the shared navigation and footer, including the preserved French essay and legal navigation. English and French service pages use the same problem-led structure, descriptive titles and service-specific links. Stylesheets are versioned by their content hash.

The October 2026 wording review uses English / United States as a comparison for international clients. Ubersuggest autocomplete returned terms including `professional bio writing services`, `AI for small business owners`, `how to use AI for small business` and `AI workflows for small business`; its daily report quota prevented fresh volume and difficulty metrics. These phrases inform wording, without claims about volume or rankings. Market context: [The Muse's career-rut service](https://www.themuse.com/coaching/stuck-in-a-career-rut), [SCORE's May 2026 practical AI session](https://www.score.org/business-education/ai-small-business-find-opportunities-and-take-action/) and [LinkedIn / Ipsos 2026 early small business findings](https://business.linkedin.com/small-business/resources/2026-small-business-study). Descriptive page titles follow [Google Search Central guidance](https://developers.google.com/search/docs/appearance/title-link).

## Current services

| Service | Price | Delivery scope |
|---|---:|---|
| Intuitive Career & Business Clarity | 79 USD | Short questionnaire, 45-minute session, one-page synthesis, one next step |
| Professional Bio & Offer Writing | 111 USD | One bio and one existing offer; agreed correction round |
| Booking Flow Fix | 149 USD | One defined issue; compatibility and scope checked before payment |
| Practical AI | 99 USD | One task, a working session and a reusable process |
| Lyrics and melody commissions | Personal quote | Deliverables, language, revisions, timing and use agreed before payment |

Intuitive Career & Business Clarity links directly to its reservation page. Professional Bio & Offer Writing and Practical AI link to their respective Stripe payment pages, using the URLs supplied by Morgane in `SERVICE_CHECKOUTS`. Both English and French service pages use these links. Booking Flow Fix still begins with contact so compatibility and scope can be reviewed; music commissions remain by quotation. Contact is also available before booking or paying. The contact form opens an email draft for the visitor to review and send; WhatsApp is available as well.

## Music support

The standalone support page is at `/support.html` in English and `/fr/soutenir.html` in French. `/soutenir.html` redirects to the English page. It keeps the supplied pastel card design, displays Morgane’s portrait in a circle, and links to the four supplied Stripe contributions: 10, 20, 50 and 100 EUR. The 20 EUR option is visually featured. The main navigation (desktop and mobile), music pages and site footers link to the support page. Titles, descriptions and visible copy describe an online music fundraiser / cagnotte en ligne for Morgane’s creative projects. Copy and payment URLs are maintained in `scripts/build_site.py`; styling is in `public/assets/css/support.css`. No payment is processed by the site itself.

## Analytics

All non-empty published HTML pages use Google Analytics 4 measurement ID `G-049S97BX69`, installed by the final build pass. The shared loader in `public/assets/js/analytics.js` loads Google's tag only after an explicit analytics opt-in, remembers acceptance/refusal for 180 days, and lets visitors reopen their choice through Cookie settings or the privacy page. Refusal blocks the tag; withdrawing a previous acceptance disables measurement, removes GA cookies and reloads the page. Advertising consent stays denied, Google Signals and ad personalisation are disabled, and the code does not send form contents or URL query strings. English and French privacy pages describe the actual implementation. Old inline Google tags are removed to avoid duplicate or premature page views.

## Edit and verify

Edit `scripts/build_site.py` for copy, routes and service definitions. Edit `public/assets/css/global.css` for styling and `public/assets/js/main.js` for navigation and the contact draft. The original French architecture essay and legal documents are preserved in `scripts/legacy/`; the full architecture essay remains published at its French approach URL.

```sh
python3 scripts/build_site.py
python3 scripts/check_site.py
node --check public/assets/js/main.js
node --check public/assets/js/analytics.js
node tests/analytics.test.cjs
python3 -m http.server 8765 --directory public
```

SEO includes self-canonical pages, reciprocal `en`/`fr`/`x-default` alternatives, descriptive metadata, Person/WebPage/Service/Breadcrumb structured data, an XML sitemap, useful internal links, redirects for older routes and noindex on existing post-purchase pages. Sitemap entries contain only the 24 public bilingual pages. Existing legal text has been preserved; English and French legal documents retain their own wording.

## Operational limits from the initial offer brief

These are internal planning limits, not additional customer-facing promises: clarity 1h15 total; bio/offer 1h30; booking fix 2h; practical AI 1h30. Confirm scope and delivery dates before payment for each digital intervention. Commission pricing and usage rights are determined in the written quotation.

Preliminary Ubersuggest research used English / United States as an international comparison: `career clarity`, `professional bio writing service` and `custom songwriting`. No search-volume or ranking promises are made to customers. Da Nang is a starting distribution channel; the services remain available internationally.
