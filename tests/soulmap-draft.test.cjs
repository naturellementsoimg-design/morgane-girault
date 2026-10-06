const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('public/assets/js/main.js', 'utf8');

function setup(lang, pro = false) {
  const ids = {};
  const values = { first_names: 'Alex Morgan', surname: 'Example', checkout_email: 'alex@example.com', birth_date: '1990-02-18', birth_time: '08:45', birth_city: 'York', birth_country: 'United Kingdom', current_context: 'A fictional life transition', main_question: 'A fictional recurring pattern' };
  if (pro) values.professional_context = 'A fictional independent business';
  function element(id) {
    return ids[id] ||= { value: '', hidden: true, checked: false, listeners: {}, addEventListener(type, callback) { this.listeners[type] = callback; }, focus() {}, select() {} };
  }
  const form = element('soulmap-form');
  form.dataset = { offer: pro ? 'SoulMap Pro' : 'SoulMap' };
  form.reportValidity = () => true;
  const location = { href: 'https://www.morgane-girault.com/post-achats/soulmap.html' };
  class DraftData {
    get(key) { return values[key]; }
    has(key) { return Object.hasOwn(values, key) && !(key === 'birth_time' && ids.birth_time.disabled); }
  }
  vm.runInNewContext(source, { document: { documentElement: { lang }, querySelector: () => null, querySelectorAll: () => [], addEventListener() {}, getElementById: id => id === 'inquiry-form' || id === 'primary-navigation' ? null : element(id) }, window: { location }, FormData: DraftData, Date, URLSearchParams, navigator: { clipboard: { writeText: async () => {} } } });
  return { ids, form, location, submit() { form.listeners.submit({ preventDefault() {} }); } };
}

const personal = setup('en');
assert.equal(personal.ids.birth_time.required, true);
personal.submit();
assert.equal(personal.ids['soulmap-draft'].hidden, false);
const draft = personal.ids['soulmap-email-preview'].value;
assert.match(draft, /All first names: Alex Morgan/);
assert.match(draft, /Date of birth \(YYYY-MM-DD\): 1990-02-18/);
assert.match(draft, /Time of birth: 08:45/);
assert.match(draft, /Country of birth: United Kingdom/);
assert.doesNotMatch(draft, /Activity, offers and clients/);
const url = new URL(personal.ids['soulmap-email-link'].href);
assert.equal(url.pathname, 'feminine.escapes.awakens@gmail.com');
assert.equal(url.searchParams.get('body'), draft);
assert.equal(personal.location.href, 'https://www.morgane-girault.com/post-achats/soulmap.html');
assert.match(personal.ids['soulmap-status'].textContent, /not been sent yet/);

const professional = setup('fr', true);
professional.ids.birth_time_unknown.checked = true;
professional.ids.birth_time_unknown.listeners.change();
assert.equal(professional.ids.birth_time.disabled, true);
assert.equal(professional.ids.birth_time.required, false);
professional.submit();
assert.match(professional.ids['soulmap-email-preview'].value, /SoulMap Pro/);
assert.match(professional.ids['soulmap-email-preview'].value, /Heure de naissance: Inconnue/);
assert.match(professional.ids['soulmap-email-preview'].value, /Activité, offres et clientes: A fictional independent business/);
assert.doesNotMatch(professional.ids['soulmap-email-preview'].value, /08:45/);
assert.match(professional.ids['soulmap-status'].textContent, /pas encore envoyées/);
console.log('PASS: EN/FR questionnaires, personal/pro fields, unknown birth time, exact email draft and no automatic transmission.');
