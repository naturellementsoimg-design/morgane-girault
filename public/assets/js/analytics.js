/* Google Analytics 4: load only after an explicit audience-measurement choice. */
(() => {
  'use strict';
  const measurementId = document.currentScript?.dataset.measurementId;
  if (!/^G-[A-Z0-9]+$/.test(measurementId || '') || window.mgAnalyticsInstalled) return;
  window.mgAnalyticsInstalled = true;
  const storageKey = 'mg-analytics-consent-v1';
  const duration = 180 * 24 * 60 * 60 * 1000;
  const disableKey = `ga-disable-${measurementId}`;
  let started = false;
  let focusBeforeSettings;
  window[disableKey] = true;
  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  const denied = { analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' };
  window.gtag('consent', 'default', denied);
  window.gtag('set', 'ads_data_redaction', true);

  function readChoice() {
    try {
      const saved = JSON.parse(localStorage.getItem(storageKey));
      if (saved && ['accepted', 'refused'].includes(saved.choice) && Number.isFinite(saved.at)
          && Date.now() >= saved.at && Date.now() - saved.at < duration) return saved.choice;
    } catch (_) { /* The current visit still works when browser storage is unavailable. */ }
    return null;
  }

  function clearAnalyticsCookies() {
    const domains = [null];
    const parts = location.hostname.split('.');
    for (let i = 0; i < parts.length - 1; i++) domains.push('.' + parts.slice(i).join('.'));
    document.cookie.split(';').forEach(cookie => {
      const name = cookie.split('=')[0].trim();
      if (!/^_ga(?:_|$)/.test(name)) return;
      domains.forEach(domain => {
        document.cookie = `${name}=; Max-Age=0; path=/; SameSite=Lax${domain ? '; domain=' + domain : ''}`;
      });
    });
  }

  function applyChoice(choice) {
    const accepted = choice === 'accepted';
    window[disableKey] = !accepted;
    window.gtag('consent', 'update', { ...denied, analytics_storage: accepted ? 'granted' : 'denied' });
    if (!accepted) {
      clearAnalyticsCookies();
      return;
    }
    if (started) return;
    started = true;
    window.gtag('js', new Date());
    window.gtag('config', measurementId, {
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
      cookie_expires: duration / 1000,
      page_location: location.origin + location.pathname,
      page_referrer: (() => { try { return document.referrer ? new URL(document.referrer).origin : ''; } catch (_) { return ''; } })()
    });
    const tag = document.createElement('script');
    tag.id = 'mg-google-tag';
    tag.async = true;
    tag.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;
    document.head.appendChild(tag);
  }

  const french = document.documentElement.lang.toLowerCase().startsWith('fr');
  const copy = french ? {
    title: 'Mesure d’audience',
    text: 'Peut-on utiliser Google Analytics pour comprendre les visites et améliorer ce site ? La mesure commence uniquement si tu acceptes. Tu peux changer ton choix à tout moment.',
    accept: 'Accepter la mesure', refuse: 'Refuser la mesure', settings: 'Préférences cookies',
    privacy: 'Confidentialité et cookies', privacyUrl: '/legal/confidentialite-cookies.html'
  } : {
    title: 'Audience measurement',
    text: 'May we use Google Analytics to understand visits and improve this site? Measurement starts only if you accept. You can change your choice at any time.',
    accept: 'Accept analytics', refuse: 'Refuse analytics', settings: 'Cookie settings',
    privacy: 'Privacy and cookies', privacyUrl: '/privacy-policy.html'
  };
  const banner = document.createElement('section');
  banner.className = 'mg-consent';
  banner.hidden = true;
  banner.setAttribute('role', 'region');
  banner.setAttribute('aria-label', copy.title);
  banner.innerHTML = `<div class="mg-consent-copy"><strong>${copy.title}</strong><p>${copy.text}</p><a href="${copy.privacyUrl}">${copy.privacy}</a></div><div class="mg-consent-actions"><button type="button" data-mg-choice="refused">${copy.refuse}</button><button type="button" data-mg-choice="accepted">${copy.accept}</button></div>`;
  const settings = document.createElement('button');
  settings.type = 'button';
  settings.className = 'mg-cookie-settings';
  settings.textContent = copy.settings;
  settings.setAttribute('aria-expanded', 'false');
  settings.setAttribute('aria-controls', 'mg-analytics-choices');
  banner.id = 'mg-analytics-choices';
  document.body.append(banner, settings);

  function showSettings() {
    focusBeforeSettings = document.activeElement;
    banner.hidden = false;
    settings.hidden = true;
    settings.setAttribute('aria-expanded', 'true');
    banner.querySelector('button').focus();
  }
  function closeSettings() {
    banner.hidden = true;
    settings.hidden = false;
    settings.setAttribute('aria-expanded', 'false');
  }
  banner.querySelectorAll('[data-mg-choice]').forEach(button => {
    button.addEventListener('click', () => {
      const choice = button.dataset.mgChoice;
      try { localStorage.setItem(storageKey, JSON.stringify({ choice, at: Date.now() })); } catch (_) { /* Keep this visit's choice in memory. */ }
      applyChoice(choice);
      closeSettings();
      (focusBeforeSettings?.isConnected ? focusBeforeSettings : settings).focus();
      // Unload the Google library when a previously granted choice is withdrawn.
      if (choice === 'refused' && started) location.reload();
    });
  });
  settings.addEventListener('click', showSettings);
  window.addEventListener('open-cookie-settings', showSettings);
  window.addEventListener('storage', event => {
    if (event.key !== storageKey) return;
    const choice = readChoice();
    applyChoice(choice);
    if (choice === 'accepted' || choice === 'refused') closeSettings();
    else { banner.hidden = false; settings.hidden = true; }
    if (choice !== 'accepted' && started) location.reload();
  });
  const savedChoice = readChoice();
  if (savedChoice) applyChoice(savedChoice);
  else { clearAnalyticsCookies(); banner.hidden = false; settings.hidden = true; }
})();
