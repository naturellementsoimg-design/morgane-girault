'use strict';
const menuButton = document.querySelector('.mobile-menu-btn');
const menu = document.getElementById('primary-navigation');
function closeMenu() { menu?.classList.remove('is-open'); menuButton?.setAttribute('aria-expanded', 'false'); }
menuButton?.addEventListener('click', () => {
  const opened = menu.classList.toggle('is-open');
  menuButton.setAttribute('aria-expanded', String(opened));
});
menu?.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => { if (event.key === 'Escape' && menu?.classList.contains('is-open')) { closeMenu(); menuButton.focus(); } });
document.querySelectorAll('[data-year]').forEach(element => { element.textContent = new Date().getFullYear(); });
const inquiry = document.getElementById('inquiry-form');
if (inquiry) {
  const service = document.getElementById('service');
  const requested = new URLSearchParams(window.location.search).get('service');
  if ([...service.options].some(option => option.value === requested)) service.value = requested;
  inquiry.addEventListener('submit', event => {
    event.preventDefault();
    if (!inquiry.reportValidity()) return;
    const data = new FormData(inquiry);
    const topic = service.options[service.selectedIndex].text;
    const french = document.documentElement.lang === 'fr';
    const body = `${french ? 'Prénom' : 'Name'}: ${data.get('name')}\nEmail: ${data.get('email')}\nService: ${topic}\n\n${data.get('message')}`;
    const href = `mailto:feminine.escapes.awakens@gmail.com?subject=${encodeURIComponent(topic + (french ? ' — Demande depuis le site' : ' — Website inquiry'))}&body=${encodeURIComponent(body)}`;
    window.location.href = href;
    document.getElementById('form-status').textContent = french
      ? 'Ton application e-mail s’ouvre avec un brouillon. Vérifie-le et envoie-le, ou utilise le lien WhatsApp si elle ne s’ouvre pas.'
      : 'Your email app opens with a draft. Review it and send it, or use the WhatsApp link if your email app does not open.';
  });
}

// Only prepare a draft. Answers are neither uploaded nor stored in the browser.
const soulmapForm = document.getElementById('soulmap-form');
if (soulmapForm) {
  const french = document.documentElement.lang === 'fr';
  const birthTime = document.getElementById('birth_time');
  const unknownTime = document.getElementById('birth_time_unknown');
  const preview = document.getElementById('soulmap-email-preview');
  const status = document.getElementById('soulmap-status');
  function updateTimeRequirement() {
    birthTime.disabled = unknownTime.checked;
    birthTime.required = !unknownTime.checked;
  }
  unknownTime.addEventListener('change', updateTimeRequirement);
  updateTimeRequirement();
  soulmapForm.addEventListener('submit', event => {
    event.preventDefault();
    if (!soulmapForm.reportValidity()) return;
    const data = new FormData(soulmapForm);
    const labels = french
      ? { first_names: 'Tous les prénoms', surname: 'Nom', checkout_email: 'E-mail du paiement', birth_date: 'Date de naissance (AAAA-MM-JJ)', birth_time: 'Heure de naissance', birth_city: 'Ville de naissance', birth_country: 'Pays de naissance', current_context: 'Situation actuelle', professional_context: 'Activité, offres et clientes', main_question: 'Question ou répétition à comprendre' }
      : { first_names: 'All first names', surname: 'Surname', checkout_email: 'Checkout email', birth_date: 'Date of birth (YYYY-MM-DD)', birth_time: 'Time of birth', birth_city: 'City of birth', birth_country: 'Country of birth', current_context: 'Current situation', professional_context: 'Activity, offers and clients', main_question: 'Question or repeating pattern to understand' };
    const lines = Object.entries(labels).flatMap(([key, label]) => {
      if (key === 'birth_time' && unknownTime.checked) return [`${label}: ${french ? 'Inconnue' : 'Unknown'}`];
      if (!data.has(key)) return [];
      return [`${label}: ${String(data.get(key) || '').trim()}`];
    });
    const subject = `${soulmapForm.dataset.offer} — ${french ? 'Questionnaire (livre en anglais)' : 'English book questionnaire'}`;
    preview.value = `${subject}\n\n${lines.join('\n\n')}`;
    document.getElementById('soulmap-email-link').href = `mailto:feminine.escapes.awakens@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(preview.value)}`;
    document.getElementById('soulmap-draft').hidden = false;
    status.textContent = french
      ? 'Ton brouillon est prêt. Relis-le, ouvre ton application e-mail et envoie-le. Tes réponses ne sont pas encore envoyées.'
      : 'Your draft is ready. Review it, open your email app and send it. Your answers have not been sent yet.';
  });
  document.getElementById('copy-soulmap-draft').addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(preview.value);
      status.textContent = french ? 'Réponses copiées. Colle-les dans ton e-mail et envoie-les à Morgane.' : 'Answers copied. Paste them into your email and send them to Morgane.';
    } catch {
      preview.focus();
      preview.select();
      status.textContent = french ? 'Sélectionne et copie le texte du brouillon, puis colle-le dans ton e-mail.' : 'Select and copy the draft text, then paste it into your email.';
    }
  });
}
