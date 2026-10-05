'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('public/assets/js/analytics.js', 'utf8');
const id = 'G-049S97BX69';
const key = 'mg-analytics-consent-v1';

function visit({choice, age = 0, blockedStorage = false, lang = 'en'} = {}) {
  const state = {scripts: [], cookiesDeleted: [], reloads: 0, listeners: {}, saved: choice ? JSON.stringify({choice, at:Date.now()-age}) : null};
  class Element {
    constructor(tag) { this.tagName = tag; this.dataset = {}; this.listeners = {}; this.isConnected = true; }
    setAttribute() {}
    addEventListener(name, fn) { this.listeners[name] = fn; }
    focus() { state.focused = this; }
    click() { this.listeners.click?.(); }
    set innerHTML(value) {
      this.buttons = [...value.matchAll(/data-mg-choice="([^"]+)">([^<]+)</g)].map(match => {
        const button = new Element('button'); button.dataset.mgChoice = match[1]; button.textContent = match[2]; return button;
      });
    }
    querySelector() { return this.buttons[0]; }
    querySelectorAll() { return this.buttons; }
  }
  const document = {
    currentScript: {dataset: {measurementId:id}}, documentElement: {lang}, activeElement: null,
    referrer: 'https://example.com/page?email=private@example.com',
    createElement: tag => new Element(tag),
    head: {appendChild: tag => state.scripts.push(tag)},
    body: {append: (banner, settings) => { state.banner = banner; state.settings = settings; }}
  };
  Object.defineProperty(document, 'cookie', {get: () => '_ga=visitor; _ga_049S97BX69=session; necessary=keep', set: value => state.cookiesDeleted.push(value)});
  const window = {addEventListener: (name, fn) => {state.listeners[name] = fn;}};
  const localStorage = {
    getItem: () => {if(blockedStorage) throw Error('blocked'); return state.saved;},
    setItem: (_, value) => {if(blockedStorage) throw Error('blocked'); state.saved = value;}
  };
  const location = {hostname:'www.morgane-girault.com', origin:'https://www.morgane-girault.com', pathname:'/en/contact.html', reload: () => {state.reloads++;}};
  vm.runInNewContext(source, {window, document, localStorage, location, URL, Date});
  state.window = window;
  state.choose = value => state.banner.buttons.find(button => button.dataset.mgChoice === value).click();
  state.configs = () => (window.dataLayer || []).filter(args => args[0] === 'config');
  return state;
}

let page = visit();
assert.equal(page.scripts.length, 0, 'No Google request before consent');
assert.equal(page.configs().length, 0, 'No page view queued before consent');
assert.equal(page.banner.hidden, false);
page.choose('refused');
assert.equal(page.scripts.length, 0, 'Refusal does not load Google');
assert.equal(JSON.parse(page.saved).choice, 'refused');
assert.equal(page.window[`ga-disable-${id}`], true);

page = visit({lang:'fr'});
assert.match(page.banner.buttons[1].textContent, /Accepter/);
page.choose('accepted');
assert.equal(page.scripts.length, 1);
assert.equal(page.scripts[0].src, `https://www.googletagmanager.com/gtag/js?id=${id}`);
assert.equal(page.configs().length, 1, 'One default page view');
assert.equal(page.configs()[0][1], id);
assert.equal(page.configs()[0][2].page_referrer, 'https://example.com');
assert.equal(page.configs()[0][2].allow_google_signals, false);
page.settings.click();
page.choose('accepted');
assert.equal(page.configs().length, 1, 'Reopening preferences does not duplicate page views');
page.settings.click();
page.choose('refused');
assert.equal(page.window[`ga-disable-${id}`], true, 'Withdrawal disables measurement');
assert.equal(page.reloads, 1, 'Withdrawal unloads the Google library');
assert.ok(page.cookiesDeleted.every(value => !value.startsWith('necessary=')), 'Necessary cookies survive');
assert.ok(page.cookiesDeleted.some(value => value.includes('_ga_049S97BX69=; Max-Age=0')));

assert.equal(visit({choice:'accepted'}).scripts.length, 1, 'Remembered acceptance starts measurement');
assert.equal(visit({choice:'refused'}).scripts.length, 0, 'Remembered refusal stays off');
assert.equal(visit({choice:'accepted', age:181*86400000}).scripts.length, 0, 'Expired acceptance needs a new choice');
page = visit({blockedStorage:true});
page.choose('accepted');
assert.equal(page.scripts.length, 1, 'The choice still works when storage is blocked');
page = visit({choice:'refused'});
page.listeners['open-cookie-settings']();
assert.equal(page.banner.hidden, false, 'Privacy-page preferences button reopens choices');
console.log('PASS: GA4 consent, refusal, persistence, expiry, withdrawal, translations and one page view.');
