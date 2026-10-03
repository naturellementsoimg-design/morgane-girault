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
    const href = `mailto:morgane.girault@naturellement-soi.com?subject=${encodeURIComponent(topic + (french ? ' — Demande depuis le site' : ' — Website inquiry'))}&body=${encodeURIComponent(body)}`;
    window.location.href = href;
    document.getElementById('form-status').textContent = french
      ? 'Ton application e-mail s’ouvre avec un brouillon. Vérifie-le et envoie-le, ou utilise le lien WhatsApp si elle ne s’ouvre pas.'
      : 'Your email app opens with a draft. Review it and send it, or use the WhatsApp link if your email app does not open.';
  });
}
