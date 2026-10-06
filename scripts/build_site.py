"""Build the bilingual public pages. No build dependencies or client framework."""
from pathlib import Path
import html
import hashlib
import json
import re
from urllib.parse import quote
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / 'public'
DOMAIN = 'https://morgane-girault.com'
EMAIL = 'feminine.escapes.awakens@gmail.com'
GA_MEASUREMENT_ID = 'G-049S97BX69'
WHATSAPP = 'https://wa.me/34631632482'
PORTRAIT = 'https://res.cloudinary.com/diapyc6q1/image/upload/v1788231361/ChatGPT_Image_19_aou%CC%82t_2026_a%CC%80_12_35_06_axw29g.png'
BANNER = 'https://res.cloudinary.com/diapyc6q1/image/upload/v1788231393/banner_artist_page_2_lcxbx6.png'
PHOTO = 'https://res.cloudinary.com/diapyc6q1/image/upload/v1785121138/ChatGPT_Image_27_juil._2026_a%CC%80_09_54_58_m5ycmr.png'
SPOTIFY = 'https://open.spotify.com/artist/5RRQR4lN2kZMziAEdCQOaW'
APPLE = 'https://music.apple.com/us/artist/morgane-girault/1888776066'
YOUTUBE = 'https://youtube.com/channel/UCpG8dORazPWWcVG-DhbBsqw'
INSTAGRAM = 'https://www.instagram.com/naturellement.soi.officiel'
SERVICE_CHECKOUTS = {
    'clarity': 'https://schedule.naturellement-soi.com/intuitive-career-and-business-clarity',
    'ai': 'https://book.stripe.com/bJe8wI7DPgz82nsccr8k83P',
    'bio': 'https://book.stripe.com/eVq7sEgal1Eegeia4j8k83O',
}
SUPPORT_LINKS = [
    (10, 'https://donate.stripe.com/00wcMY7DPgz89PUfoD8k83E'),
    (20, 'https://donate.stripe.com/7sY5kw4rDaaK3rw7Wb8k83H'),
    (50, 'https://donate.stripe.com/8x26oA9LXciS4vA7Wb8k83G'),
    (100, 'https://donate.stripe.com/5kQeV63nzgz85zEfoD8k83F'),
]
ROUTES = {
    'home': {'en': '/', 'fr': '/fr/'},
    'music': {'en': '/en/music.html', 'fr': '/fr/musique.html'},
    'support': {'en': '/support.html', 'fr': '/fr/soutenir.html'},
    'custom': {'en': '/en/custom-songwriting.html', 'fr': '/fr/creation-musicale-sur-mesure.html'},
    'services': {'en': '/en/services.html', 'fr': '/fr/services.html'},
    'clarity': {'en': '/en/intuitive-career-business-clarity.html', 'fr': '/fr/clarte-professionnelle-intuitive.html'},
    'bio': {'en': '/en/professional-bio-offer-writing.html', 'fr': '/fr/bio-professionnelle-presentation-offre.html'},
    'booking': {'en': '/en/booking-flow-fix.html', 'fr': '/fr/correction-parcours-reservation.html'},
    'ai': {'en': '/en/practical-ai-session.html', 'fr': '/fr/ia-pratique-activite.html'},
    'about': {'en': '/en/about.html', 'fr': '/fr/a-propos.html'},
    'approach': {'en': '/en/research.html', 'fr': '/fr/architecture-de-l-incarnation.html'},
    'contact': {'en': '/en/contact.html', 'fr': '/fr/contact.html'},
}

SERVICES = {
 'clarity': {
  'price':79,
  'en': {'name':'Intuitive Career & Business Clarity', 'title':'Intuitive Career & Business Clarity Session | US$79', 'description':'A 45-minute online session with medium Morgane Girault to connect your talents, clarify a career or business direction, and leave with a one-page map and a next step.', 'short':'You have several talents. Let’s find the thread that connects them.', 'audience':'For creatives, practitioners and independent professionals with several skills, plenty of ideas and a direction that still feels difficult to name.', 'intro':'You may know that your work needs to change without knowing what should come next. Or you may have several real strengths but struggle to see how they belong together. This session gives us a focused space to look at the person behind those possibilities.', 'body':'As a medium and soul cartographer, I bring my mediumship and energetic reading together with your actual experience, skills, desires and current circumstances. We look for a direction that feels recognisable to you and can become a real next step.', 'deliver':['A short questionnaire before we meet','A 45-minute individual video session in English','A one-page clarity map: core strengths, connections between your skills and a direction to explore','One concrete next step to test that direction'], 'facts':['45-minute session','Online · English','One-page synthesis'], 'fit':'This is a focused clarification session. If you need a complete business repositioning, a full offer strategy or a website built from scratch, we will discuss a separate scope.', 'cta':'Book my session — US$79', 'question':'Do I need to know exactly what I want to do?', 'answer':'No. You can arrive with a question, several ideas or a sense that your current direction no longer fits. The questionnaire helps us choose a useful focus before the session.', 'question2':'What does the one-page map include?', 'answer2':'Your main strengths, the links we identify between your skills, a direction worth exploring and one practical next step. It is a concise synthesis you can return to after the conversation.'},
  'fr': {'name':'Clarté professionnelle intuitive', 'title':'Séance de clarté professionnelle intuitive | 79 USD', 'description':'Une séance de 45 minutes avec Morgane Girault pour relier tes talents, clarifier une direction professionnelle et recevoir une carte de synthèse avec un premier pas concret.', 'short':'Tu as plusieurs talents. Retrouvons le fil qui les relie.', 'audience':'Pour les créatives, praticiennes et indépendantes qui possèdent plusieurs compétences, beaucoup d’idées et une direction encore difficile à nommer.', 'intro':'Tu peux sentir que ton activité doit évoluer sans savoir quelle forme lui donner. Ou reconnaître plusieurs forces en toi sans réussir à voir comment les réunir. Cette séance nous offre un espace ciblé pour regarder la personne derrière ces possibilités.', 'body':'En tant que médium et cartographe d’âmes, je relie ma lecture médiumnique et énergétique à ton parcours réel, tes compétences, tes envies et tes contraintes actuelles. Nous cherchons une direction dans laquelle tu peux te reconnaître et un premier mouvement concret.', 'deliver':['Un questionnaire court avant notre rencontre','Une séance individuelle de 45 minutes en visio','Une carte de synthèse d’une page : forces principales, liens entre tes compétences et direction à explorer','Un premier pas concret pour éprouver cette direction'], 'facts':['Séance de 45 minutes','En ligne · FR ou EN','Synthèse d’une page'], 'fit':'Ce format est une clarification ciblée. Un repositionnement complet, une stratégie d’offres approfondie ou la création d’un site font l’objet d’un périmètre distinct.', 'cta':'Réserver ma séance — 79 USD', 'question':'Dois-je déjà savoir précisément ce que je veux faire ?', 'answer':'Non. Tu peux venir avec une question, plusieurs idées ou le sentiment que ta direction actuelle ne te ressemble plus. Le questionnaire nous aide à choisir un point de départ utile.', 'question2':'Que contient la carte de synthèse ?', 'answer2':'Tes forces principales, les liens identifiés entre tes compétences, une direction à explorer et un premier pas concret. C’est un repère court auquel tu peux revenir après la séance.'}
 },
 'bio': {
  'price':111,
  'en': {'name':'Professional Bio & Offer Writing', 'title':'Professional Bio Writing & Offer Copy | US$111', 'description':'A professional bio and a clear presentation of one existing offer, rewritten in your voice by Morgane Girault. A focused online copywriting service for US$111.', 'short':'Explain what you do in words that sound like you.', 'audience':'For practitioners, creatives and independent professionals whose positioning is already defined but whose bio or offer presentation does not communicate it clearly.', 'intro':'You know what you do. Yet when someone asks you to explain it, your words become too vague, too long or too far from your voice. We work from your existing positioning to make the introduction easier to understand.', 'body':'I rewrite a professional bio and the presentation of one existing offer using the information and examples you share. The aim is to help a reader understand who you help, what they can receive and how to take the next step.', 'deliver':['A rewritten professional bio','A clear presentation of one existing offer','Language adapted to your voice and intended audience','One correction round within the agreed scope'], 'facts':['One bio + one offer','Remote collaboration','111 USD'], 'fit':'This service works from a positioning you have already chosen. If the offer itself still needs to be defined, we can start with a clarity session. A full website rewrite or complete brand strategy is a separate project.', 'cta':'Order my bio & offer — US$111', 'question':'Can we work in English or French?', 'answer':'Yes. We agree on the language and audience before the work begins. The quoted service covers one language; a bilingual version can be scoped separately.', 'question2':'What should I send you?', 'answer2':'Your existing bio, the offer you want to present, the audience it serves and a few examples of language that feels like you. We confirm the length and placement before payment.'},
  'fr': {'name':'Bio professionnelle & présentation d’offre', 'title':'Réécriture de bio professionnelle et d’offre | 111 USD', 'description':'Une bio professionnelle et la présentation d’une offre existante, réécrites dans ta voix par Morgane Girault. Une intervention ciblée à 111 USD.', 'short':'Des mots qui rendent ton travail compréhensible et te ressemblent.', 'audience':'Pour les praticiennes, créatives et indépendantes dont le positionnement est défini, mais dont la bio ou la présentation d’offre ne l’exprime pas encore clairement.', 'intro':'Tu sais ce que tu fais. Pourtant, au moment de le présenter, les mots deviennent trop vagues, trop longs ou trop éloignés de ta voix. Nous partons de ton positionnement existant pour rendre cette présentation plus claire.', 'body':'Je réécris une bio professionnelle et la présentation d’une offre existante à partir des éléments que tu me transmets. L’objectif : aider la personne qui te lit à comprendre qui tu accompagnes, ce qu’elle reçoit et comment avancer.', 'deliver':['Une bio professionnelle réécrite','Une présentation claire d’une offre existante','Des formulations adaptées à ta voix et à ton audience','Un retour de correction dans le périmètre convenu'], 'facts':['Une bio + une offre','À distance','111 USD'], 'fit':'Cette intervention part d’un positionnement déjà choisi. Si l’offre reste à définir, une séance de clarté peut être le premier pas. La réécriture d’un site complet ou une stratégie de marque demandent un autre périmètre.', 'cta':'Commander mes textes — 111 USD', 'question':'Peut-on travailler en français ou en anglais ?', 'answer':'Oui. Nous choisissons la langue et l’audience avant de commencer. Le tarif couvre une langue ; une version bilingue peut faire l’objet d’une proposition complémentaire.', 'question2':'Que dois-je te transmettre ?', 'answer2':'Ta bio actuelle, l’offre à présenter, son public et quelques exemples de formulations qui te ressemblent. Nous confirmons la longueur et l’usage des textes avant le paiement.'}
 },
 'booking': {
  'price':149,
  'en': {'name':'Booking Flow Fix', 'title':'Website Booking Flow Fix | Links, Forms & Buttons | US$149', 'description':'Fix one clearly defined booking problem: a broken link, form, button or disconnected step on a supported website. Scope confirmed before payment. US$149.', 'short':'Make the next step easy to find and easy to complete.', 'audience':'For independent professionals and practitioners with an existing website and one specific problem in the route from interest to booking.', 'intro':'Someone is ready to work with you, but a button leads to the wrong page, a form does not work or the booking step is hard to find. A small technical problem can interrupt a clear intention.', 'body':'We identify one precise issue on a website or tool I can work with, confirm the correction and verify the relevant journey after the change. I review compatibility before you pay.', 'deliver':['A correction to one agreed booking issue','Work on the relevant link, button, form or connection','Verification of the corrected journey','One correction round relating to the agreed intervention'], 'facts':['One defined problem','Compatibility checked first','149 USD'], 'fit':'A website rebuild, several unrelated errors, a new custom integration or work outside a supported setup requires a separate proposal. I confirm what is included and a realistic delivery date before payment.', 'cta':'Show me the issue — US$149', 'question':'Can you fix any website or booking tool?', 'answer':'I first review your setup and the problem. I accept the intervention only when it fits a website or tool I can work with and a clearly defined scope.', 'question2':'What should I send before we begin?', 'answer2':'The page URL, the step that should work, what happens instead and a screenshot if helpful. Please do not send passwords or secret keys through the inquiry form.'},
  'fr': {'name':'Correction du parcours de réservation', 'title':'Correction de lien, formulaire ou réservation | 149 USD', 'description':'Correction d’un problème précis de lien, formulaire, bouton ou réservation sur un site compatible. Périmètre confirmé avant paiement. 149 USD.', 'short':'Rendre le prochain pas facile à trouver et à réaliser.', 'audience':'Pour les indépendantes et praticiennes qui possèdent déjà un site et rencontrent un problème précis entre l’intérêt d’une cliente et sa réservation.', 'intro':'Une personne veut travailler avec toi, mais un bouton mène au mauvais endroit, un formulaire ne fonctionne pas ou la réservation est difficile à trouver. Un petit problème technique peut interrompre une intention claire.', 'body':'Nous identifions un problème précis sur un site ou un outil que je maîtrise, convenons de la correction et vérifions ensuite le parcours concerné. Je regarde la compatibilité avant que tu paies.', 'deliver':['La correction d’un problème de réservation défini ensemble','Une intervention sur le lien, bouton, formulaire ou raccordement concerné','La vérification du parcours corrigé','Un retour de correction lié à cette intervention'], 'facts':['Un problème défini','Compatibilité vérifiée avant paiement','149 USD'], 'fit':'Une refonte de site, plusieurs erreurs distinctes ou une nouvelle intégration complexe font l’objet d’une proposition séparée. Le contenu et un délai réaliste sont confirmés avant le paiement.', 'cta':'Te montrer le problème — 149 USD', 'question':'Peux-tu intervenir sur tous les sites et outils ?', 'answer':'Je regarde d’abord ton installation et le problème rencontré. L’intervention est acceptée lorsqu’elle correspond à un outil que je maîtrise et à un périmètre précis.', 'question2':'Que dois-je t’envoyer pour commencer ?', 'answer2':'L’URL de la page, l’étape attendue, ce qui se passe à la place et une capture si nécessaire. N’envoie pas de mot de passe ou de clé secrète dans le formulaire de contact.'}
 },
 'ai': {
  'price':99,
  'en': {'name':'Practical AI for Your Business', 'title':'Practical AI Session for Independent Professionals | US$99', 'description':'Build one reusable AI workflow for a real task in your business: organise notes, prepare a session or draft in your own voice. A practical online service at US$99.', 'short':'One real task. One useful process you can use again.', 'audience':'For practitioners, creatives and independent professionals who want to use AI in a specific part of their work without building a complicated new system.', 'intro':'You do not need another list of tools. You need a way to use the tools you have for a task that actually matters: preparing a session, organising notes or writing with more consistency.', 'body':'We choose one task and work through a reusable process together. The output is designed around your activity, your voice and the decisions you still need to make yourself.', 'deliver':['A practical online working session','One reusable workflow for one agreed task','Prompts or a concise process you can return to','One adjustment round within the agreed scope'], 'facts':['One practical workflow','Online working session','99 USD'], 'fit':'This format covers one task. A complete automation system, custom application or paid software subscriptions are outside this service. We confirm the tool, session length and scope before payment.', 'cta':'Pay for my AI session — US$99', 'question':'Do I need technical experience?', 'answer':'No. We start from the task you want to make easier and the tools you already use. The process should be simple enough for you to repeat.', 'question2':'Can we use client notes?', 'answer2':'We can work with anonymised examples or demonstration notes. You do not need to share identifiable or sensitive client information to learn the process.'},
  'fr': {'name':'IA pratique pour ton activité', 'title':'Séance IA pratique pour indépendantes | 99 USD', 'description':'Construire un processus IA réutilisable pour une tâche réelle : organiser ses notes, préparer une séance ou écrire dans sa voix. Une intervention pratique à 99 USD.', 'short':'Une tâche réelle. Un processus utile que tu peux réutiliser.', 'audience':'Pour les praticiennes, créatives et indépendantes qui veulent utiliser l’IA dans une partie précise de leur activité sans construire un système compliqué.', 'intro':'Tu n’as pas besoin d’une nouvelle liste d’outils. Tu as besoin d’une manière de les utiliser pour une tâche qui compte : préparer une séance, organiser tes notes ou écrire avec plus de cohérence.', 'body':'Nous choisissons une tâche et construisons ensemble un processus réutilisable. Le résultat part de ton activité, de ta voix et des décisions que tu souhaites garder entre tes mains.', 'deliver':['Une séance pratique de travail en ligne','Un processus réutilisable pour une tâche définie ensemble','Des instructions ou prompts que tu peux reprendre','Un retour d’ajustement dans le périmètre convenu'], 'facts':['Un processus concret','Séance de travail en ligne','99 USD'], 'fit':'Ce format couvre une tâche. Une automatisation complète, une application sur mesure ou les abonnements à des logiciels sont hors périmètre. Nous confirmons l’outil, la durée de séance et le contenu avant paiement.', 'cta':'Payer ma séance IA — 99 USD', 'question':'Faut-il déjà avoir des compétences techniques ?', 'answer':'Non. Nous partons de la tâche que tu souhaites simplifier et des outils que tu utilises déjà. Le processus doit rester assez simple pour que tu puisses le reproduire.', 'question2':'Peut-on travailler à partir de notes clientes ?', 'answer2':'Nous pouvons utiliser des exemples anonymisés ou des notes de démonstration. Tu n’as pas besoin de partager des informations identifiantes ou sensibles pour apprendre le processus.'}
 }
}

LABELS = {
 'en': {'music':'Music','services':'Work with me','about':'About','contact':'Contact','home':'Home','skip':'Skip to content','menu':'Menu','explore':'Explore','follow':'Listen & follow','terms':'Terms (French)','privacy':'Privacy','legal':'Legal notice','rights':'All rights reserved','based':'Based in Da Nang · Working online internationally','deliver':'What you receive','fit':'A clear scope','next':'How we begin','faq':'A few useful answers','related':'Other ways to work together','request':'Tell me about your project','quote':'Request a quote','approach':'Intuition, made practical'},
 'fr': {'music':'Musique','services':'Travailler ensemble','about':'À propos','contact':'Contact','home':'Accueil','skip':'Aller au contenu','menu':'Menu','explore':'Explorer','follow':'Écouter & suivre','terms':'CGV','privacy':'Confidentialité','legal':'Mentions légales','rights':'Tous droits réservés','based':'À Da Nang · À distance, à l’international','deliver':'Ce que tu reçois','fit':'Un périmètre clair','next':'Comment nous commençons','faq':'Quelques réponses utiles','related':'D’autres façons de travailler ensemble','request':'Parlons de ton projet','quote':'Demander un devis','approach':'L’intuition prend forme'}
}

LABELS['en']['support'] = 'Support my music'
LABELS['fr']['support'] = 'Soutenir ma musique'

# The visitor's starting problem and the concrete output lead the offer copy.
OFFER_COPY = {
    'clarity': {
        'en': {'problem':'Feeling stuck in your career or business?', 'heading':'Find your next career or business direction.', 'short':'Connect your talents, explore a direction that fits and leave with one next step to test.', 'card_deliver':['45-minute online session','One-page map of your strengths and direction','One practical next step'], 'card_cta':'Find my direction', 'quick':'Unsure what comes next?', 'title':'Intuitive Career & Business Clarity Session | US$79', 'description':'Feeling stuck in your career or business? Explore a direction with medium Morgane Girault in a 45-minute online session. One-page clarity map and next step. US$79.'},
        'fr': {'problem':'Ta direction professionnelle reste floue ?', 'heading':'Clarifier la suite de ton parcours ou de ton activité.', 'short':'Relier tes talents, explorer une direction qui te ressemble et repartir avec un premier pas à tester.', 'card_deliver':['Séance de 45 minutes en ligne','Carte de tes forces et de ta direction, sur une page','Un premier pas concret'], 'card_cta':'Clarifier ma direction', 'quick':'Quelle direction prendre ?', 'title':'Clarté professionnelle intuitive | Séance de 45 min', 'description':'Ta direction professionnelle reste floue ? Une séance de 45 minutes avec Morgane Girault, médium, pour relier tes talents et définir un premier pas. 79 USD.'},
    },
    'bio': {
        'en': {'problem':'Hard to explain what you do?', 'heading':'A professional bio that makes your work clear.', 'short':'Get a professional bio and a clear description of one existing offer, written in your voice.', 'card_deliver':['One professional bio','One existing offer rewritten clearly','One agreed correction round'], 'card_cta':'Make my words clearer', 'quick':'How do I explain my work?', 'title':'Professional Bio Writing Service & Offer Copy', 'description':'Help people understand what you do. A professional bio writing service and clear copy for one existing offer, in your voice. Online with Morgane Girault. US$111.'},
        'fr': {'problem':'Difficile d’expliquer ce que tu proposes ?', 'heading':'Une bio professionnelle qui rend ton activité claire.', 'short':'Une bio professionnelle et une présentation claire d’une offre existante, écrites dans ta voix.', 'card_deliver':['Une bio professionnelle','Une offre existante présentée clairement','Un retour de correction convenu'], 'card_cta':'Clarifier mes textes', 'quick':'Comment présenter mon activité ?', 'title':'Rédaction de bio professionnelle & présentation d’offre', 'description':'Rends ton activité facile à comprendre avec une bio professionnelle et la présentation d’une offre existante, dans ta voix. À distance avec Morgane Girault. 111 USD.'},
    },
    'booking': {
        'en': {'problem':'A booking link or form isn’t working?', 'heading':'Fix the step that stops clients from booking.', 'short':'Correct one broken link, button, form or booking connection on a compatible website.', 'card_deliver':['One specific issue corrected','Compatibility and scope checked before payment','The corrected booking journey tested'], 'card_cta':'Get my booking issue reviewed', 'quick':'Why can’t clients book?', 'title':'Booking Link & Form Fix for Your Website | US$149', 'description':'A booking link, button or form is blocking clients? Get one website booking issue reviewed, fixed and tested. Compatibility checked before payment. US$149.'},
        'fr': {'problem':'Un lien ou un formulaire bloque les réservations ?', 'heading':'Corriger l’étape qui empêche tes clientes de réserver.', 'short':'Corriger un lien, un bouton, un formulaire ou une connexion de réservation sur un site compatible.', 'card_deliver':['Un problème précis corrigé','Compatibilité et périmètre vérifiés avant paiement','Le parcours corrigé testé'], 'card_cta':'Faire examiner mon problème', 'quick':'Pourquoi la réservation bloque ?', 'title':'Correction de lien ou formulaire de réservation | 149 USD', 'description':'Un lien, bouton ou formulaire empêche tes clientes de réserver ? Un problème précis corrigé et testé sur un site compatible. Vérification avant paiement. 149 USD.'},
    },
    'ai': {
        'en': {'problem':'Want to use AI, but unsure where to start?', 'heading':'Learn to use AI for a real task in your business.', 'short':'Turn one everyday task into a simple AI workflow you can repeat: drafting, organising notes or preparing a session.', 'card_deliver':['One practical online working session','One task worked through together','Reusable prompts and a simple process'], 'card_cta':'Explore my practical AI session', 'quick':'How can AI help my work?', 'title':'Practical AI Session for Small Business | US$99', 'description':'Learn to use AI for one real task in your small business: drafting, organising notes or preparing a session. A personal online session and reusable workflow. US$99.'},
        'fr': {'problem':'Envie d’utiliser l’IA, sans savoir par où commencer ?', 'heading':'Utiliser l’IA pour une tâche réelle de ton activité.', 'short':'Créer un processus IA simple à réutiliser pour rédiger, organiser tes notes ou préparer une séance.', 'card_deliver':['Une séance pratique de travail en ligne','Une tâche réalisée ensemble','Des prompts et un processus réutilisables'], 'card_cta':'Découvrir ma séance IA', 'quick':'Comment l’IA peut m’aider ?', 'title':'Séance IA pratique pour ton activité | 99 USD', 'description':'Apprends à utiliser l’IA pour une tâche de ton activité : rédiger, organiser tes notes ou préparer une séance. Un processus simple à réutiliser. En ligne. 99 USD.'},
    },
}
for offer_key, languages in OFFER_COPY.items():
    for language, copy in languages.items():
        SERVICES[offer_key][language].update(copy)

def esc(value): return html.escape(str(value), quote=True)
def clean_blank_lines(value): return re.sub(r'(?m)^[ \t]+$', '', value)
def path(key,lang): return ROUTES[key][lang]
def link(href,label,cls='text-link',external=False):
    attrs=' target="_blank" rel="noopener noreferrer"' if external else ''
    return f'<a class="{cls}" href="{esc(href)}"{attrs}>{esc(label)}</a>'
def paragraph(text): return '<p>'+esc(text)+'</p>'
def bullet(items): return '<ul>'+''.join('<li>'+esc(i)+'</li>' for i in items)+'</ul>'
def request_url(key,lang): return path('contact',lang)+'?service='+key
def service_url(key,lang): return SERVICE_CHECKOUTS.get(key) or request_url(key,lang)
def header(key,lang):
    l=LABELS[lang]; other='fr' if lang=='en' else 'en'
    items=''.join(f'<li><a href="{path(k,lang)}"'+(' aria-current="page"' if k==key else '')+f'>{("Support" if lang=="en" else "Soutenir") if k=="support" else l[k]}</a></li>' for k in ['services','music','support','about','contact'])
    return f'''<a class="skip-link" href="#main">{l['skip']}</a><header class="site-header"><nav class="nav" aria-label="{'Main navigation' if lang=='en' else 'Navigation principale'}"><a class="logo" href="{path('home',lang)}">Morgane Girault</a><button class="mobile-menu-btn" type="button" aria-expanded="false" aria-controls="primary-navigation">{l['menu']}</button><ul class="nav-links" id="primary-navigation">{items}<li><a class="language" href="{path(key,other)}" lang="{other}" hreflang="{other}" aria-label="{'Lire cette page en français' if other=='fr' else 'Read this page in English'}">{other.upper()}</a></li></ul></nav></header>'''

def footer(lang):
    l=LABELS[lang]; legal='/legal-notice.html' if lang=='en' else '/legal/mentions-legales.html'; privacy='/privacy-policy.html' if lang=='en' else '/legal/confidentialite-cookies.html'
    return f'''<footer class="footer"><div class="container"><div class="footer-grid"><div class="footer-brand-block"><div class="footer-brand">Morgane<br>Girault</div><small>{l['based']}</small></div><div><h3>{l['explore']}</h3>{''.join(link(path(k,lang),l[k],'') for k in ['services','music','support','about','contact'])}</div><div><h3>{l['follow']}</h3>{link(SPOTIFY,'Spotify','',True)}{link(APPLE,'Apple Music','',True)}{link(YOUTUBE,'YouTube','',True)}{link(INSTAGRAM,'Instagram','',True)}</div></div><div class="footer-bottom"><span>© <span data-year>2026</span> Morgane Girault · {l['rights']}</span><div class="legal-links">{link(legal,l['legal'],'')}{link(privacy,l['privacy'],'')}{link('/legal/conditions-generales.html',l['terms'],'')}</div></div></div></footer>'''

def metadata(key,lang,title,description,service=None,stylesheet='global.css',include_script=True):
    url=DOMAIN+path(key,lang)
    css_version=hashlib.sha256((PUBLIC/'assets/css'/stylesheet).read_bytes()).hexdigest()[:12]
    stylesheet+='?v='+css_version
    script_version=hashlib.sha256((PUBLIC/'assets/js/main.js').read_bytes()).hexdigest()[:12]
    graph=[{'@type':'Person','@id':DOMAIN+'/#morgane','name':'Morgane Girault','url':DOMAIN+'/', 'image':PORTRAIT,'jobTitle':'Artist, songwriter, medium and soul cartographer','sameAs':[SPOTIFY,APPLE,YOUTUBE,INSTAGRAM]}, {'@type':'WebPage','@id':url+'#page','url':url,'name':title,'description':description,'inLanguage':lang,'isPartOf':{'@id':DOMAIN+'/#website'},'about':{'@id':DOMAIN+'/#morgane'}}]
    if key=='home': graph.append({'@type':'WebSite','@id':DOMAIN+'/#website','name':'Morgane Girault','url':DOMAIN+'/','inLanguage':['en','fr'],'publisher':{'@id':DOMAIN+'/#morgane'}})
    else:
        crumbs=[{'@type':'ListItem','position':1,'name':LABELS[lang]['home'],'item':DOMAIN+path('home',lang)}]
        if key in SERVICES or key=='custom':
            parent='music' if key=='custom' else 'services'
            crumbs.append({'@type':'ListItem','position':2,'name':LABELS[lang][parent],'item':DOMAIN+path(parent,lang)})
        crumbs.append({'@type':'ListItem','position':len(crumbs)+1,'name':title.split('|')[0].strip(),'item':url})
        graph.append({'@type':'BreadcrumbList','itemListElement':crumbs})
    if service:
        item={'@type':'Service','name':service[lang]['name'],'description':description,'url':url,'provider':{'@id':DOMAIN+'/#morgane'},'availableChannel':{'@type':'ServiceChannel','serviceUrl':url}}
        if service.get('price'): item['offers']={'@type':'Offer','price':str(service['price']),'priceCurrency':'USD','url':SERVICE_CHECKOUTS.get(key,url)}
        graph.append(item)
    alternates=''.join(f'<link rel="alternate" hreflang="{code}" href="{DOMAIN+path(key,code)}">' for code in ['en','fr'])
    script=f'<script src="/assets/js/main.js?v={script_version}" defer></script>' if include_script else ''
    return f'''<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} | Morgane Girault</title><meta name="description" content="{esc(description)}"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="author" content="Morgane Girault"><link rel="canonical" href="{url}">{alternates}<link rel="alternate" hreflang="x-default" href="{DOMAIN+path(key,'en')}"><meta property="og:type" content="website"><meta property="og:title" content="{esc(title)} | Morgane Girault"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{PORTRAIT}"><meta property="og:image:alt" content="Morgane Girault"><meta property="og:site_name" content="Morgane Girault"><meta property="og:locale" content="{'en_US' if lang=='en' else 'fr_FR'}"><meta property="og:locale:alternate" content="{'fr_FR' if lang=='en' else 'en_US'}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(description)}"><meta name="twitter:image" content="{PORTRAIT}"><meta name="theme-color" content="#110d0e"><link rel="icon" href="{PORTRAIT}"><link rel="preconnect" href="https://res.cloudinary.com"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="/assets/css/{stylesheet}"><script type="application/ld+json">{json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('</','<\\/')}</script>{script}'''

def write_page(key,lang,title,description,body,service=None):
    urlpath=path(key,lang)
    rel='index.html' if urlpath=='/' else ('fr/index.html' if urlpath=='/fr/' else urlpath.lstrip('/'))
    f=PUBLIC/rel; f.parent.mkdir(parents=True,exist_ok=True)
    page=f'<!doctype html>\n<html lang="{lang}"><head>{metadata(key,lang,title,description,service)}</head><body class="{key}">{header(key,lang)}<main id="main">{body}</main>{footer(lang)}</body></html>\n'
    f.write_text(page.replace('><','>\n<'))

def support(lang):
    en=lang=='en'
    copy = {
        'en': {
            'title':'Online Fundraiser for Music & Creative Projects',
            'description':'Support Morgane Girault’s music through her online fundraiser. Contributions of €10, €20, €50 or €100 help new songs, melodies and creative projects take shape.',
            'kicker':'Online music fundraiser',
            'heading':'Support my music<br>& creative projects.',
            'intro':'If a song, a melody or a few words of mine have stayed with you, this online fundraiser is a way to support my music and creative projects. Choose the contribution that feels right for you.',
            'labels':['A little encouragement','Support my next creation','A generous contribution','A beautiful boost'],
            'note':'Every contribution supports the time and space to write songs, compose melodies and bring my creative projects to life. Thank you for being part of the music.',
            'secure':'Secure payment via Stripe · EUR',
            'listen':'Listen to my music',
            'languages':'Page language',
        },
        'fr': {
            'title':'Cagnotte en ligne pour ma musique et mes projets',
            'description':'La cagnotte en ligne de Morgane Girault pour soutenir sa musique, ses chansons et ses projets créatifs. Contributions de 10, 20, 50 ou 100 € via Stripe.',
            'kicker':'Ma cagnotte en ligne',
            'heading':'Soutiens ma musique<br>et mes projets.',
            'intro':'Si une chanson, une mélodie ou quelques mots de moi ont accompagné un moment de ta vie, cette cagnotte en ligne te permet de soutenir ma musique et mes projets créatifs. Choisis la contribution qui te correspond.',
            'labels':['Un petit encouragement','Soutenir ma prochaine création','Un soutien précieux','Un bel élan pour mes projets'],
            'note':'Chaque contribution soutient le temps et l’espace nécessaires pour écrire des chansons, composer des mélodies et donner vie à mes projets créatifs. Merci de faire partie de cette aventure musicale.',
            'secure':'Paiement sécurisé via Stripe · EUR',
            'listen':'Écouter ma musique',
            'languages':'Langue de la page',
        },
    }[lang]
    switch=''.join(f'<a href="{path("support",code)}" lang="{code}" hreflang="{code}"'+(' class="active" aria-current="page"' if code==lang else '')+f' aria-label="{"Read this page in English" if code=="en" else "Lire cette page en français"}">{code.upper()}</a>' for code in ['en','fr'])
    contributions=''.join(f'<a class="support-option'+(' featured' if amount==20 else '')+f'" href="{url}" target="_blank" rel="noopener noreferrer"><span><span class="amount">{amount} €</span><span class="label">{esc(label)}</span></span><span class="arrow" aria-hidden="true">→</span></a>' for (amount,url),label in zip(SUPPORT_LINKS,copy['labels']))
    head=metadata('support',lang,copy['title'],copy['description'],stylesheet='support.css',include_script=False)
    head+='<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">'
    body=f'''<main class="support-page">
<nav class="language-nav" aria-label="{copy['languages']}"><div class="language-switch">{switch}</div></nav>
<section class="support-card" aria-labelledby="support-heading"><div class="support-content">
<div class="brand">Morgane Girault</div>
<img class="support-portrait" src="{PORTRAIT}" alt="Morgane Girault" width="136" height="136" fetchpriority="high">
<p class="support-kicker">{copy['kicker']}</p>
<h1 id="support-heading">{copy['heading']}</h1>
<p class="intro">{esc(copy['intro'])}</p>
<div class="support-links">{contributions}</div>
<p class="note">{esc(copy['note'])}</p>
<p class="secure"><svg width="12" height="14" viewBox="0 0 12 14" fill="none" aria-hidden="true"><path d="M3 6V4a3 3 0 0 1 6 0v2M2 6h8v7H2z" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/></svg>{esc(copy['secure'])}</p>
</div></section>
<footer class="support-footer"><a href="{path('home',lang)}">morgane-girault.com</a><a href="{path('music',lang)}">{copy['listen']}</a></footer>
</main>'''
    f=PUBLIC/path('support',lang).lstrip('/')
    f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(f'<!doctype html>\n<html lang="{lang}"><head>{head}</head><body>{body}</body></html>\n'.replace('><','>\n<'))

def hero(lang,title,intro,kicker,parent=None,facts=None):
    l=LABELS[lang]; crumbs=link(path('home',lang),l['home'],'')
    if parent: crumbs+=' <span aria-hidden="true">/</span> '+link(path(parent,lang),l[parent],'')
    facts_html='<div class="fact-row">'+''.join('<span>'+esc(x)+'</span>' for x in facts)+'</div>' if facts else ''
    return f'<section class="page-hero"><div class="container"><div class="breadcrumbs">{crumbs}</div><span class="eyebrow">{esc(kicker)}</span><h1>{esc(title)}</h1><p class="lead">{esc(intro)}</p>{facts_html}</div></section>'

def cards(lang,keys=None):
    keys=keys or list(SERVICES)
    return '<div class="offer-grid">'+''.join(f'<article class="offer-card'+(' featured' if k=='clarity' else '')+f'"><span class="eyebrow">{esc(SERVICES[k][lang]["name"])}</span><h3>{esc(SERVICES[k][lang]["problem"])}</h3><p>{esc(SERVICES[k][lang]["short"])}</p><p class="price">{SERVICES[k]["price"]}<small>USD</small></p>{bullet(SERVICES[k][lang]["card_deliver"])}{link(path(k,lang),SERVICES[k][lang]["card_cta"],"btn btn-dark")}</article>' for k in keys)+'</div>'

def home(lang):
    en=lang=='en'
    title='Career Clarity & Practical Business Help' if en else 'Clarté professionnelle & aide concrète pour ton activité'
    desc='Online help for creatives and independent professionals: intuitive career clarity, professional bio writing, booking fixes and practical AI with Morgane Girault.' if en else 'Pour créatives, praticiennes et indépendantes : clarté professionnelle intuitive, bio et offre, réservation et IA pratique. Avec Morgane Girault, en ligne.'
    h1='Feeling stuck in your<br>career or business?' if en else 'Tu te sens bloquée dans<br>ton parcours ou ton activité ?'
    intro='I help creatives, practitioners and independent professionals find their next direction, explain their offer and make everyday work easier.' if en else 'J’aide les créatives, praticiennes et indépendantes à trouver leur direction, présenter leur offre et simplifier leur travail au quotidien.'
    hero_html=f'''<section class="work-hero"><div class="container work-hero-grid"><div class="work-hero-copy"><span class="eyebrow">{'Intuitive career clarity & practical business help' if en else 'Clarté intuitive & aide concrète pour ton activité'}</span><h1>{h1}</h1><p class="lead">{esc(intro)}</p><div class="button-row">{link('#services','Choose what you need' if en else 'Choisir ce dont tu as besoin','btn btn-wine')}{link(path('clarity',lang),'Career clarity · US$79' if en else 'Clarté professionnelle · 79 USD','btn btn-outline')}</div><p class="work-hero-note">{'Online internationally · English & French' if en else 'En ligne, à l’international · Français & anglais'}</p></div><figure class="work-hero-portrait"><img src="{BANNER}" alt="Morgane Girault" fetchpriority="high" width="1536" height="1024"><figcaption><strong>Morgane Girault</strong><span>{'Medium · Soul cartographer · Creator' if en else 'Médium · Cartographe d’âmes · Créatrice'}</span></figcaption></figure></div><nav class="container need-links" aria-label="{'Find help for your situation' if en else 'Trouver une aide pour ta situation'}">{''.join(link(path(k,lang),SERVICES[k][lang]['quick'],'need-link') for k in SERVICES)}</nav></section>'''
    offers=f'''<section class="section offers-section" id="services"><div class="container"><div class="section-head"><span class="eyebrow">{'Four focused services · Prices in USD' if en else 'Quatre prestations ciblées · Tarifs en USD'}</span><h2 class="section-title">{'What is getting in your way?' if en else 'Qu’est-ce qui te freine aujourd’hui ?'}</h2><p class="lead">{'Start with the problem you want help with. Each service gives you a specific output: a clarity map, clearer words, a booking fix or a reusable AI workflow.' if en else 'Pars du problème pour lequel tu as besoin d’aide. Chaque prestation donne un résultat précis : une carte de clarté, des textes plus lisibles, une réservation corrigée ou un processus IA réutilisable.'}</p></div>{cards(lang)}<p class="offer-choice">{'Not sure? If your direction is unclear, start with career clarity. If your offer is already defined, choose writing, a booking fix or practical AI.' if en else 'Tu hésites ? Si ta direction est floue, commence par la clarté professionnelle. Si ton offre est déjà définie, choisis les textes, la réservation ou l’IA pratique.'} {link(path('contact',lang),'Ask me a question' if en else 'Me poser une question')}</p></div></section>'''
    about=f'''<section class="section wine"><div class="container split top"><div><span class="eyebrow">{'Who you will work with' if en else 'Avec qui tu travailles'}</span><h2 class="section-title">{'Intuition, connected<br>to your real life.' if en else 'L’intuition, reliée<br>à ta réalité.'}</h2></div><div><p class="lead">{'I’m Morgane, a medium, soul cartographer and creator. In the clarity session, I bring mediumship and energetic reading together with your skills, experience and current circumstances.' if en else 'Je suis Morgane, médium, cartographe d’âmes et créatrice. Dans la séance de clarté, je relie ma lecture médiumnique et énergétique à tes compétences, ton parcours et ta situation actuelle.'}</p><p>{'For writing, booking fixes and AI, I work directly on the text, website issue or task you bring. We agree on a clear focus and something you can use afterwards.' if en else 'Pour les textes, la réservation et l’IA, je travaille directement sur les mots, le problème technique ou la tâche que tu apportes. Nous définissons un objectif précis et un résultat utilisable ensuite.'}</p>{link(path('about',lang),'Meet Morgane' if en else 'Découvrir Morgane','btn btn-light')}</div></div></section>'''
    music_html=f'''<section class="section home-music" id="music"><div class="container"><div class="section-head"><span class="eyebrow">{'Music & creation' if en else 'Musique & création'}</span><h2 class="section-title">{'There is music here, too.' if en else 'Il y a aussi la musique.'}</h2><p class="lead">{'Soul, jazz and R&B are another part of my work. Listen to my releases, or tell me about a story you would like to turn into lyrics or a melody.' if en else 'La soul, le jazz et le R&B font aussi partie de mon travail. Écoute mes créations ou parle-moi d’une histoire que tu aimerais transformer en paroles ou en mélodie.'}</p></div><div class="entry-grid"><article class="entry music-entry"><span class="eyebrow">{'Listen' if en else 'Écouter'}</span><h3>{'Explore my music.' if en else 'Découvrir ma musique.'}</h3><p>{'Songs about love, freedom and finding your way back to yourself.' if en else 'Des chansons autour de l’amour, de la liberté et du retour à soi.'}</p>{link(path('music',lang),'Listen to the releases' if en else 'Écouter les créations')}</article><article class="entry"><span class="eyebrow">{'Paid custom songwriting · By quote' if en else 'Création musicale payante · Sur devis'}</span><h3>{'Your story, in a song.' if en else 'Ton histoire, en chanson.'}</h3><p>{'Personal lyrics and melodies for people, artists and creative projects. We agree on the format, price and intended use before I begin.' if en else 'Des paroles et des mélodies pour des personnes, des artistes et des projets créatifs. Le format, le tarif et l’usage sont convenus avant de commencer.'}</p>{link(path('custom',lang),'Explore a custom commission' if en else 'Découvrir une création sur mesure')}</article></div></div></section>'''
    write_page('home',lang,title,desc,hero_html+offers+about+music_html+featured_release(lang))

def featured_release(lang):
    en=lang=='en'
    cover='https://res.cloudinary.com/diapyc6q1/image/upload/v1788231980/Portrait_d_album_warm_and_deep_Morgane_Girault_du93g8.png'
    return f'<section class="section dark"><div class="container split"><img class="album-cover" src="{cover}" alt="Warm and Deep — Morgane Girault" width="1024" height="1024" loading="lazy"><div><span class="eyebrow">'+('Featured project' if en else 'À découvrir')+'</span><h2 class="section-title">Warm<br>and Deep</h2><p class="lead">'+('A warm dive into jazz, soul and rhythm & blues. Songs moving through love, choice and the quiet process of coming back to yourself.' if en else 'Une plongée chaleureuse dans le jazz, la soul et le rhythm & blues. Des chansons qui traversent l’amour, les choix et le mouvement intime du retour à soi.')+f'</p>{link("https://open.spotify.com/album/4h5PNmZXZ6yEeT6mp1CBAB","Listen on Spotify" if en else "Écouter sur Spotify","btn btn-light",True)}<div class="platform-links">{link(APPLE,"Apple Music","",True)}{link(YOUTUBE,"YouTube","",True)}</div></div></div></section>'

def music(lang):
    en=lang=='en'
    title='Music & Custom Songwriting' if en else 'Musique & création sur mesure'
    desc='Explore the soul, jazz and R&B music of Morgane Girault, then commission personalised lyrics, a melody or a song direction for your own story or creative project.' if en else 'Explore la musique soul, jazz et R&B de Morgane Girault et commande des paroles, une mélodie ou une direction de chanson pour ton histoire ou ton projet.'
    body=hero(lang,'Music to come back to yourself.' if en else 'La musique comme retour à soi.','Soul, jazz, rhythm & blues. Stories of love, freedom, desire and the transformations that change the direction of a life.' if en else 'Soul, jazz, rhythm & blues. Des histoires d’amour, de liberté, de désir et de transformations qui changent une trajectoire.','Music' if en else 'Musique')
    records=[('Warm and Deep','Album','https://res.cloudinary.com/diapyc6q1/image/upload/v1788231980/Portrait_d_album_warm_and_deep_Morgane_Girault_du93g8.png','https://open.spotify.com/album/4h5PNmZXZ6yEeT6mp1CBAB'),('Goddess Within','Single','https://res.cloudinary.com/diapyc6q1/image/upload/v1788232414/Goddess_within_album_morgane_girault_cover_nr3gvi.png',SPOTIFY),('The Color of Your Soul','Music' if en else 'Musique','https://res.cloudinary.com/diapyc6q1/image/upload/v1788233250/Cover_album_The_color_of_your_soul_Morgane_Girault_s0wjyb.png','https://open.spotify.com/album/1tJrqQ5KWXAEjjsTvyt3bG')]
    body+='<section class="section"><div class="container"><span class="eyebrow">'+('The catalogue' if en else 'Le catalogue')+'</span><h2 class="section-title">'+('Listen inside my universe.' if en else 'Entrer dans mon univers.')+'</h2><div class="record-grid">'+''.join(f'<article class="record"><a href="{u}" target="_blank" rel="noopener noreferrer"><div class="record-cover"><img src="{c}" alt="{esc(n)} — Morgane Girault" width="1024" height="1024" loading="lazy"></div><small>{t}</small><h3>{esc(n)}</h3><p>'+('Explore on Spotify' if en else 'Découvrir sur Spotify')+'</p></a></article>' for n,t,c,u in records)+'</div></div></section>'
    body+='<section class="section wine"><div class="container split"><div><span class="eyebrow">'+('Create with me' if en else 'Créer ensemble')+'</span><h2 class="section-title">'+('Your story can become a song.' if en else 'Ton histoire peut devenir une chanson.')+'</h2></div><div><p class="lead">'+('I write lyrics and compose melodies for people, artists and creative projects. We can begin with your story, an existing text, a feeling you want to express or a musical direction.' if en else 'J’écris des paroles et compose des mélodies pour des personnes, des artistes et des projets créatifs. Nous pouvons partir de ton histoire, d’un texte existant, d’une émotion ou d’une direction musicale.')+'</p><p>'+('A paid, personalised commission. The format, price, delivery date and intended use are agreed before we begin.' if en else 'Une création personnalisée payante. Le format, le tarif, le délai et l’usage prévu sont définis avant de commencer.')+f'</p>{link(path("custom",lang),"Explore a custom commission" if en else "Découvrir la création sur mesure","btn btn-light")}</div></div></section>'
    body+='<section class="section"><div class="container prose"><span class="eyebrow">'+('Keep the music growing' if en else 'Faire grandir la musique')+'</span><h2 class="section-title">'+('Support my music & creative projects.' if en else 'Soutenir ma musique et mes projets.')+'</h2><p class="lead">'+('If my music has been part of your story, you can help me keep writing songs, composing melodies and bringing new creations to life.' if en else 'Si ma musique a accompagné un moment de ton histoire, tu peux m’aider à continuer d’écrire, de composer et de donner vie à de nouvelles créations.')+f'</p>{link(path("support",lang),LABELS[lang]["support"],"btn btn-wine")}</div></section>'
    write_page('music',lang,title,desc,body)

def custom(lang):
    en=lang=='en'; l=LABELS[lang]
    title='Custom Songwriting, Lyrics & Melody Composition' if en else 'Écriture de paroles & composition de mélodies sur mesure'
    desc='Commission personalised lyrics or a melody from songwriter Morgane Girault. A paid music creation service for artists, personal stories and creative projects, available by quote.' if en else 'Commande des paroles ou une mélodie personnalisée à Morgane Girault. Une création musicale payante pour artistes, histoires personnelles et projets créatifs, sur devis.'
    body=hero(lang,'A song that begins with you.' if en else 'Une chanson qui part de toi.','Lyrics, a melody, or the two together: a personal creative collaboration shaped around what you want to express.' if en else 'Des paroles, une mélodie ou les deux : une collaboration créative qui part de ce que tu souhaites exprimer.','Custom songwriting' if en else 'Création musicale sur mesure','music',['Lyrics · Melody · Creative direction' if en else 'Paroles · Mélodie · Direction créative','Personal quote' if en else 'Devis personnalisé'])
    options=[('Lyrics written for you','From a story, a theme or a text you have started. We find the language, images and structure that carry what you want to say.'),('A melody for your words','A musical direction for an existing text, a voice or a feeling. We agree on the style and the form of the melody reference.'),('A song direction','Words and melody developed together around a personal story, an artistic project or a meaningful moment.') ] if en else [('Des paroles écrites pour toi','À partir d’une histoire, d’un thème ou d’un texte commencé. Nous cherchons les mots, les images et la structure qui portent ce que tu veux dire.'),('Une mélodie pour tes mots','Une direction musicale pour un texte existant, une voix ou une émotion. Nous définissons le style et la forme du repère mélodique.'),('Une direction de chanson','Des paroles et une mélodie développées ensemble autour d’une histoire personnelle, d’un projet artistique ou d’un moment important.')]
    body+='<section class="section"><div class="container detail-grid"><div class="prose"><h2>'+('What would you like to create?' if en else 'Qu’as-tu envie de créer ?')+'</h2>'+''.join('<h3>'+esc(t)+'</h3>'+paragraph(p) for t,p in options)+'<h2>'+('A clear creative brief' if en else 'Un cadre de création clair')+'</h2>'+paragraph('Before you pay, we agree on the language, musical references, deliverables, revisions, timeline and the personal or commercial use of the work. Recording, production and usage rights are discussed explicitly in the quote.' if en else 'Avant le paiement, nous définissons la langue, les références musicales, les livrables, les retours, le délai et l’usage personnel ou commercial de la création. L’enregistrement, la production et les droits d’utilisation sont précisés dans le devis.')+'</div><aside class="aside"><span class="eyebrow">'+('A paid commission' if en else 'Une commande payante')+'</span><p class="price">'+('By quote' if en else 'Sur devis')+'</p><p>'+('Send me the story or project, what you would like to receive and a few musical references. I will propose a clear scope before we begin.' if en else 'Envoie-moi ton histoire ou ton projet, ce que tu aimerais recevoir et quelques références musicales. Je te proposerai un périmètre clair avant de commencer.')+f'</p>{link(request_url("custom",lang),l["quote"],"btn btn-wine")}</aside></div></section>'
    body+=steps(lang,[('Tell me the intention','Your story, audience, preferred language and musical references.'),('Agree on the creation','We confirm the deliverables, price, revisions, timeline and intended use.'),('Let it take shape','I develop the work from the agreed brief and we use the planned feedback stage.')] if en else [('Me transmettre l’intention','Ton histoire, ton public, la langue souhaitée et tes références musicales.'),('Définir la création','Nous validons les livrables, le prix, les retours, le délai et l’usage prévu.'),('Laisser la création prendre forme','Je développe le travail à partir du brief convenu, avec l’étape de retour prévue.')])
    write_page('custom',lang,title,desc,body,{'en':{'name':'Custom songwriting, lyrics and melody composition'},'fr':{'name':'Création musicale, paroles et mélodies sur mesure'}})

def steps(lang,items):
    return '<section class="section"><div class="container"><span class="eyebrow">'+LABELS[lang]['next']+'</span><ol class="steps">'+''.join('<li><h3>'+esc(t)+'</h3>'+paragraph(p)+'</li>' for t,p in items)+'</ol></div></section>'

def services_page(lang):
    en=lang=='en'
    title='Career Clarity, Bio Writing & Practical AI' if en else 'Clarté professionnelle, rédaction & IA pratique'
    desc='Online services with Morgane Girault: intuitive career clarity at US$79, bio and offer writing at US$111, booking flow fixes at US$149 and practical AI sessions at US$99.' if en else 'Les prestations en ligne de Morgane Girault : clarté professionnelle à 79 USD, bio et offre à 111 USD, réservation à 149 USD et IA pratique à 99 USD.'
    body=hero(lang,'What do you need help with today?' if en else 'De quoi as-tu besoin aujourd’hui ?','Feeling stuck in your career, struggling to explain your offer, facing a broken booking link or unsure how to use AI? Choose the problem you want to work on, and see exactly what you will receive.' if en else 'Ta direction reste floue, ton offre est difficile à expliquer, une réservation bloque ou tu ne sais pas comment utiliser l’IA ? Choisis le problème sur lequel tu veux avancer et découvre ce que tu reçois.','Online services for creatives & independent professionals' if en else 'Prestations en ligne pour créatives et indépendantes')
    body+='<section class="section"><div class="container">'+cards(lang)+'</div></section>'
    body+='<section class="section wine"><div class="container split"><h2 class="section-title">'+('Not sure which door to open?' if en else 'Tu ne sais pas par où commencer ?')+'</h2><div><p class="lead">'+('If the direction itself is unclear, start with the intuitive clarity session. If you already know what you want to offer, choose the concrete intervention that helps you express it or make it work.' if en else 'Si la direction elle-même reste floue, commence par la séance de clarté intuitive. Si tu sais déjà ce que tu veux proposer, choisis l’intervention concrète qui t’aide à l’exprimer ou à la faire fonctionner.')+f'</p>{link(path("clarity",lang),"Explore the US$79 session" if en else "Découvrir la séance à 79 USD","btn btn-light")}</div></div></section>'
    body+=steps(lang,[('Choose a useful focus','Tell me what you want to clarify, express or fix.'),('Confirm the scope','We confirm suitability, the relevant details and a realistic timeline before payment.'),('Begin the work','You receive the agreed next steps and we work toward a specific output.')] if en else [('Choisir un point de départ utile','Dis-moi ce que tu souhaites clarifier, exprimer ou corriger.'),('Confirmer le périmètre','Nous validons l’adéquation, les détails utiles et un délai réaliste avant le paiement.'),('Commencer le travail','Tu reçois les étapes convenues et nous avançons vers un résultat concret.')])
    write_page('services',lang,title,desc,body)

def service_page(key,lang):
    en=lang=='en'; data=SERVICES[key]; d=data[lang]; l=LABELS[lang]
    if key=='clarity':
        payment_note='Book your 45-minute session on the booking page. Choose an available time and follow the reservation steps.' if en else 'Réserve ta séance de 45 minutes sur la page de réservation. Choisis un créneau disponible et suis les étapes proposées.'
        payment_answer='The booking button opens the session reservation page. Choose your time and follow the booking and payment steps there. Contact me if you have a question before reserving. Prices shown here are in US dollars.' if en else 'Le bouton ouvre la page de réservation de la séance. Choisis ton créneau et suis les étapes de réservation et de paiement. Tu peux me contacter avant de réserver si tu as une question. Les tarifs affichés ici sont en dollars américains.'
    elif key in SERVICE_CHECKOUTS:
        payment_note='Pay for this focused service through Stripe. Contact me first if you need to confirm the scope or timing.' if en else 'Règle cette prestation ciblée via Stripe. Contacte-moi avant le paiement si tu as besoin de confirmer le périmètre ou le délai.'
        payment_answer='The button opens the Stripe payment page for this service. After payment, contact me with your brief so we can confirm the practical details and next steps. If the scope or timing needs clarification, contact me before paying. Prices shown here are in US dollars.' if en else 'Le bouton ouvre la page de paiement Stripe de cette prestation. Après le paiement, contacte-moi avec les éléments de ton projet pour confirmer les détails pratiques et la suite. Si le périmètre ou le délai doit être précisé, contacte-moi avant de payer. Les tarifs affichés ici sont en dollars américains.'
    else:
        payment_note='Working online internationally, from Da Nang. We confirm your focus, the next steps and payment arrangements before beginning.' if en else 'À distance, à l’international, depuis Da Nang. Nous confirmons ton besoin, les prochaines étapes et le paiement avant de commencer.'
        payment_answer='Use the inquiry button to contact me. We confirm the focus and practical details, then I send the appropriate payment and next-step information. All prices on these pages are in US dollars.' if en else 'Le bouton de contact me permet de confirmer ton besoin et les détails pratiques. Je te transmets ensuite les informations de paiement et les prochaines étapes. Tous les tarifs de ces pages sont en dollars américains.'
    facts=d['facts'] if any('USD' in fact for fact in d['facts']) else d['facts']+[f'US${data["price"]}' if en else f'{data["price"]} USD']
    body=hero(lang,d['heading'],d['problem']+' '+d['short'],d['name'],'services',facts)
    body=body.replace('</div></section>',f'<div class="button-row">{link(service_url(key,lang),d["cta"],"btn btn-light")}</div></div></section>',1)
    body+=f'<section class="section"><div class="container detail-grid"><div class="prose"><h2>'+('Does this sound familiar?' if en else 'Est-ce que tu te reconnais ici ?')+'</h2>'+paragraph(d['intro'])+paragraph(d['audience'])+'<h2>'+('My way of working' if en else 'Ma manière de travailler')+'</h2>'+paragraph(d['body'])+f'<h2>{l["deliver"]}</h2>{bullet(d["deliver"])}<h2>{l["fit"]}</h2>{paragraph(d["fit"])}</div><aside class="aside"><span class="eyebrow">'+('Your investment' if en else 'Ton investissement')+f'</span><p class="price">{data["price"]} <small>USD</small></p>'+paragraph(payment_note)+link(service_url(key,lang),d['cta'],'btn btn-wine')+('<p class="form-note">'+link(request_url(key,lang),'A question before booking or paying?' if en else 'Une question avant de réserver ou de payer ?','')+'</p>' if key in SERVICE_CHECKOUTS else '')+'</aside></div></section>'
    items=[('Your starting point','Tell me your question or project. For a clarity session, a short questionnaire prepares our meeting.'),('A focused collaboration','We work on the session or intervention defined in your chosen service.'),('Something you can use','You receive the synthesis, text, correction or workflow included in your offer.')] if en else [('Ton point de départ','Tu me transmets ta question ou ton projet. Pour la séance de clarté, un court questionnaire prépare notre rencontre.'),('Un travail ciblé','Nous réalisons la séance ou l’intervention définie dans la prestation choisie.'),('Un résultat utilisable','Tu reçois la synthèse, le texte, la correction ou le processus inclus dans ton offre.')]
    body+=steps(lang,items)
    body+=f'<section class="section"><div class="container faq"><span class="eyebrow">{l["faq"]}</span><details><summary>{esc(d["question"])}</summary>{paragraph(d["answer"])}</details><details><summary>{esc(d["question2"])}</summary>{paragraph(d["answer2"])}</details><details><summary>'+('How do we arrange payment and timing?' if en else 'Comment organiser le paiement et le délai ?')+'</summary>'+paragraph(payment_answer)+'</details></div></section>'
    body+='<section class="section wine"><div class="container"><h2 class="section-title">'+('Ready to make this useful?' if en else 'Prête à donner forme à la suite ?')+f'</h2>{link(service_url(key,lang),d["cta"],"btn btn-light")} <div class="platform-links">{link(path("services",lang),l["related"],"")}</div></div></section>'
    write_page(key,lang,d['title'],d['description'],body,data)

def about(lang):
    en=lang=='en'
    title='Artist, Medium & Soul Cartographer' if en else 'Artiste, médium & cartographe d’âmes'
    desc='Meet Morgane Girault, an artist, medium and soul cartographer based in Da Nang. Music, intuitive readings and practical creative work, connected by one vision.' if en else 'Découvre Morgane Girault, artiste, médium et cartographe d’âmes à Da Nang. Musique, lectures intuitives et créations concrètes, reliées par une même vision.'
    body=hero(lang,'There has always been more than one way for me to create.' if en else 'Il y a toujours eu plusieurs façons pour moi de créer.','I am an artist, medium and soul cartographer. I connect what we sense, the stories we carry and the forms we can give them in the world.' if en else 'Je suis artiste, médium et cartographe d’âmes. Je relie ce que nous percevons, les histoires que nous portons et les formes que nous pouvons leur donner.','Morgane Girault')
    body+='<section class="section"><div class="container split top"><img class="image-portrait" src="'+PHOTO+'" alt="Morgane Girault" width="1024" height="1280" loading="lazy"><div class="prose"><h2>'+('The invisible gives meaning. Embodiment gives transformation.' if en else 'L’invisible donne le sens. L’incarnation donne la transformation.')+'</h2>'+paragraph('My mediumship and energetic reading are central to my work. I listen for the patterns, connections and movements that are not always easy to bring together in a conscious story.' if en else 'Ma médiumnité et ma lecture énergétique sont au cœur de mon travail. Je perçois les motifs, les liens et les mouvements que le récit conscient ne parvient pas toujours à réunir.')+paragraph('Then comes the question I care about: what can this become in your decisions, your work, your relationships and the way you express yourself?' if en else 'Vient ensuite la question qui me tient à cœur : que peut devenir cette compréhension dans tes décisions, ton activité, tes relations et ta manière de t’exprimer ?')+'<h2>'+('Music is another language for the same movement.' if en else 'La musique est un autre langage pour ce même mouvement.')+'</h2>'+paragraph('I write about love, freedom, desire and returning to yourself. A song can begin with a rhythm, a phrase, a melody or a feeling. I follow the thread until it finds a form.' if en else 'J’écris sur l’amour, la liberté, le désir et le retour à soi. Une chanson peut commencer par un rythme, une phrase, une mélodie ou une sensation. Je suis le fil jusqu’à ce qu’il trouve sa forme.')+'<h2>'+('And ideas need a practical home.' if en else 'Les idées ont aussi besoin d’une forme concrète.')+'</h2>'+paragraph('My technical and creative skills also help people express an offer, improve a digital journey and build a useful way of working. I work online internationally from Da Nang, Vietnam, in English and French.' if en else 'Mes compétences techniques et créatives permettent aussi d’aider une personne à exprimer une offre, améliorer un parcours digital et construire une manière de travailler plus simple. Je travaille à distance depuis Da Nang, en français et en anglais.')+f'<div class="button-row">{link(path("approach",lang),"Explore my approach" if en else "Explorer mon approche","btn btn-outline")}{link(path("services",lang),"Work with me" if en else "Travailler ensemble","btn btn-dark")}</div></div></div></section>'
    write_page('about',lang,title,desc,body)

def approach(lang):
    en=lang=='en'
    title='Intuition, Identity & the Architecture of Embodiment' if en else 'Intuition, identité & Architecture de l’Incarnation'
    desc='Morgane Girault’s approach connects mediumship and energetic reading with identity, decisions and practical expression. Discover the Architecture of Embodiment.' if en else 'L’approche de Morgane Girault relie médiumnité, lecture énergétique, identité, décisions et expression concrète. Découvre l’Architecture de l’Incarnation.'
    body=hero(lang,'Understanding is a beginning.' if en else 'Comprendre est un point de départ.','The Architecture of Embodiment explores how an inner understanding can become a different way of choosing, expressing and living.' if en else 'L’Architecture de l’Incarnation explore comment une compréhension intérieure peut devenir une autre manière de choisir, de s’exprimer et de vivre.','My approach' if en else 'Mon approche')
    pairs=[('Reading the invisible','Mediumship and energetic perception help me identify links, recurring patterns and the movement behind a person’s current question.'),('Connecting the parts','A person’s skills, relationships, work and sense of identity do not always feel like separate subjects. We look for the thread that can make them easier to understand together.'),('Giving understanding a form','We then connect the reading to decisions, boundaries, words and practical steps. A useful insight should help you recognise a next move in your actual circumstances.'),('Leaving room for your choices','I do not decide in your place. The work aims to make your direction more recognisable, while keeping your agency and your circumstances at the centre.')] if en else [('Lire l’invisible','La médiumnité et la perception énergétique m’aident à identifier les liens, les répétitions et le mouvement derrière une question actuelle.'),('Relier les dimensions','Les compétences, les relations, l’activité et l’identité d’une personne ne sont pas toujours des sujets séparés. Nous cherchons le fil qui permet de les comprendre ensemble.'),('Donner forme à la compréhension','Nous relions ensuite la lecture aux décisions, aux limites, aux mots et aux premiers pas concrets. Une perception utile doit pouvoir rencontrer ta situation réelle.'),('Préserver ton pouvoir de choix','Je ne décide pas à ta place. Le travail cherche à rendre ta direction plus reconnaissable, en gardant ton libre arbitre et tes circonstances au centre.')]
    body+='<section class="section"><div class="container prose">'+''.join('<h2>'+esc(t)+'</h2>'+paragraph(p) for t,p in pairs)+f'<div class="button-row">{link(path("clarity",lang),"Explore a focused clarity session" if en else "Découvrir une séance de clarté","btn btn-wine")}</div></div></section>'
    write_page('approach',lang,title,desc,body)

def contact(lang):
    en=lang=='en'
    title='Contact & Project Inquiries' if en else 'Contact & demandes de projet'
    desc='Contact Morgane Girault for an intuitive career clarity session, a focused digital service, custom lyrics or a melody commission. Online internationally, in English and French.' if en else 'Contacte Morgane Girault pour une séance de clarté, une prestation digitale, des paroles personnalisées ou une mélodie. À distance, en français et en anglais.'
    body=hero(lang,'What would you like to bring into focus?' if en else 'Qu’aimerais-tu clarifier ou faire exister ?','Tell me a little about your question or project. We will choose a useful starting point and confirm the next steps.' if en else 'Parle-moi de ta question ou de ton projet. Nous choisirons un point de départ utile et confirmerons les prochaines étapes.','Contact')
    options=[('clarity','Career & Business Clarity · US$79'),('bio','Bio & Offer Writing · US$111'),('booking','Booking Flow Fix · US$149'),('ai','Practical AI · US$99'),('custom','Custom lyrics / melody · Quote'),('other','Another question')] if en else [('clarity','Clarté professionnelle · 79 USD'),('bio','Bio & présentation d’offre · 111 USD'),('booking','Parcours de réservation · 149 USD'),('ai','IA pratique · 99 USD'),('custom','Paroles / mélodie · Sur devis'),('other','Une autre question')]
    wmsg='Hello Morgane, I would like to discuss a service or a music commission.' if en else 'Bonjour Morgane, j’aimerais parler d’une prestation ou d’une création musicale.'
    form=f'<form class="inquiry-form" id="inquiry-form" action="mailto:{EMAIL}" method="get"><div class="field"><label for="name">'+('Your name' if en else 'Ton prénom')+'</label><input id="name" name="name" autocomplete="name" maxlength="100" required></div><div class="field"><label for="email">'+('Your email' if en else 'Ton e-mail')+'</label><input id="email" name="email" type="email" autocomplete="email" maxlength="200" required></div><div class="field"><label for="service">'+('What brings you here?' if en else 'Qu’est-ce qui t’amène ?')+'</label><select id="service" name="service">'+''.join(f'<option value="{v}">{esc(t)}</option>' for v,t in options)+'</select></div><div class="field"><label for="message">'+('Your question or project' if en else 'Ta question ou ton projet')+'</label><textarea id="message" name="message" maxlength="4000" required></textarea></div><p class="form-note">'+('This form prepares a draft in your email app. You review and send it yourself. Please share only the information needed to understand your request.' if en else 'Ce formulaire prépare un brouillon dans ton application e-mail. Tu le relis et l’envoies toi-même. Partage uniquement les informations utiles pour comprendre ta demande.')+'</p><button class="btn btn-wine" type="submit">'+('Open my email draft' if en else 'Préparer mon e-mail')+'</button><p class="status" id="form-status" role="status" aria-live="polite"></p></form>'
    body+='<section class="section"><div class="container split top"><div><h2 class="section-title">'+('Let’s start with a real conversation.' if en else 'Commencer par un échange concret.')+'</h2><p class="lead">'+('For the digital services, I confirm the scope and compatibility before payment. For a music commission, we agree on the format, price and intended use in a personal quote.' if en else 'Pour les interventions digitales, je confirme le périmètre et la compatibilité avant paiement. Pour une création musicale, nous définissons le format, le tarif et l’usage prévu dans un devis.')+'</p><div class="contact-list">'+link(WHATSAPP+'?text='+quote(wmsg),'Talk on WhatsApp' if en else 'Échanger sur WhatsApp','btn btn-dark',True)+link('mailto:'+EMAIL,EMAIL)+f'</div><p class="form-note">{LABELS[lang]["based"]}</p></div>{form}</div></section>'
    write_page('contact',lang,title,desc,body)

def adapt_legal():
    pairs=[('legal-notice.html','legal/mentions-legales.html'),('privacy-policy.html','legal/confidentialite-cookies.html')]
    for eng,fra in pairs:
        for rel,lang,other in [(eng,'en',fra),(fra,'fr',eng)]:
            f=PUBLIC/rel; text=(ROOT/'scripts/legacy'/Path(rel).name).read_text()
            text=re.sub(r'<link\b[^>]*\brel=["\'](?:canonical|alternate)["\'][^>]*>','',text,flags=re.I)
            text=text.replace('</head>',f'<link rel="canonical" href="{DOMAIN}/{rel}"><link rel="alternate" hreflang="en" href="{DOMAIN}/{eng}"><link rel="alternate" hreflang="fr" href="{DOMAIN}/{fra}"><link rel="alternate" hreflang="x-default" href="{DOMAIN}/{eng}"></head>')
            text=re.sub(r'href=["\'](?:index\.html|/)["\']',f'href="{path("home",lang)}"',text)
            text=re.sub(r'href=["\'](?:contact\.html|contact-en\.html|/contact|/commencer)["\']',f'href="{path("contact",lang)}"',text)
            other_lang='fr' if lang=='en' else 'en'
            nav=''.join(link(path(key,lang),LABELS[lang][key],'') for key in ['home','services','music','support','about','contact'])
            nav+=f'<a href="/{other}" lang="{other_lang}" hreflang="{other_lang}">{other_lang.upper()}</a>'
            text=re.sub(r'(<nav\b[^>]*(?:class="(?:nav-links|desktop-nav)"|aria-label="Navigation mobile")[^>]*>).*?</nav>',lambda m:m.group(1)+nav+'</nav>',text,flags=re.S)
            for old,key in {'/seance-passage':'clarity','/architecture-de-l-incarnation':'approach','/a-propos':'about'}.items():
                text=text.replace(f'href="{old}"',f'href="{path(key,lang)}"')
            for old in ['/legal/politique-confidentialite','/legal/politique-cookies']:
                text=text.replace(f'href="{old}"','href="/legal/confidentialite-cookies.html"')
            support_link=link(path('support',lang),LABELS[lang]['support'],'')
            if lang=='fr':
                text=text.replace('<div class="footer-links">','<div class="footer-links">'+support_link,1)
            else:
                text=text.replace('<footer>','<footer>'+support_link,1)
            f.write_text(clean_blank_lines(text))

def preserve_architecture():
    """Keep the complete original French essay accessible, with current navigation."""
    source=(ROOT/'scripts/legacy/architecture-source.html').read_text()
    source=re.sub(r'<title>.*?</title>','<title>Architecture de l’Incarnation | Morgane Girault</title>',source,flags=re.S)
    source=re.sub(r'<link\b[^>]*\brel=["\'](?:canonical|alternate)["\'][^>]*>','',source,flags=re.I)
    source=source.replace('</head>',f'<link rel="canonical" href="{DOMAIN+path("approach","fr")}"><link rel="alternate" hreflang="fr" href="{DOMAIN+path("approach","fr")}"><link rel="alternate" hreflang="en" href="{DOMAIN+path("approach","en")}"><link rel="alternate" hreflang="x-default" href="{DOMAIN+path("approach","en")}"><style>.updated-footer{{padding:45px 0;background:#110d0e;color:#fffdf9}}.updated-footer a{{display:inline-block;margin:8px 18px 8px 0;color:#f5efe8}}.header-actions .language-switch{{font-weight:700;padding:10px}}</style></head>')
    source=source.replace('<main>','<main id="main">')
    source=re.sub(r'(<h1 id="hero-title">).*?(</h1>)',r'\1L’Architecture de l’Incarnation\2',source,flags=re.S)
    navigation=''.join(link(path(k,'fr'),LABELS['fr'][k],'') for k in ['home','services','music','support','about','contact'])
    source=re.sub(r'(<nav class="desktop-nav"[^>]*>).*?(</nav>)',lambda m:m[1]+navigation+m[2],source,flags=re.S)
    source=re.sub(r'(<div class="mobile-menu"[^>]*>\s*<nav[^>]*>).*?(</nav>)',lambda m:m[1]+navigation+link(path('approach','en'),'EN','')+m[2],source,flags=re.S)
    source=source.replace('<div class="header-actions">',f'<div class="header-actions"><a class="language-switch" href="{path("approach","en")}" lang="en">EN</a>')
    mappings={'/':path('home','fr'),'/commencer':path('services','fr'),'/seance-passage':path('clarity','fr'),'/architecture-de-l-incarnation':path('approach','fr'),'/a-propos':path('about','fr'),'/soulmap':path('services','fr'),'/accompagnements':path('services','fr'),'/chroniques':path('approach','fr'),'/recherches':path('approach','fr'),'/institut':path('approach','fr'),'/temoignages':path('services','fr'),'/contact':path('contact','fr')}
    source=re.sub(r'href="([^"]+)"',lambda m:'href="'+mappings.get(m[1],m[1])+'"',source)
    source=source.replace(DOMAIN+'/a-propos',DOMAIN+path('approach','fr'))
    updated='<footer class="updated-footer"><div class="container"><p>© <span id="current-year">2026</span> Morgane Girault</p><nav aria-label="Navigation de pied de page">'+navigation+link(path('approach','en'),'EN','')+link('/legal/mentions-legales.html','Mentions légales','')+link('/legal/confidentialite-cookies.html','Confidentialité','')+'</nav></div></footer>'
    source=re.sub(r'<footer\b[^>]*>.*?</footer>',updated,source,flags=re.S)
    (PUBLIC/path('approach','fr').lstrip('/')).write_text(clean_blank_lines(source))

def configuration():
    redirects=[]
    aliases={
      '/en/index.html':'/', '/en/':'/', '/home.html':'/', '/home':'/',
      '/soutenir.html':path('support','en'), '/support':path('support','en'),
      '/music/':path('music','en'), '/music':path('music','en'), '/music/warm-and-deep/':path('music','en'),
      '/services/':path('services','en'), '/services':path('services','en'), '/about/':path('about','en'), '/about':path('about','en'), '/about.html':path('about','en'),
      '/contact/':path('contact','en'), '/contact':path('contact','en'), '/contact.html':path('contact','en'), '/contact-en.html':path('contact','en'),
      '/a-propos':path('about','fr'), '/commencer':path('services','en'), '/architecture-de-l-incarnation':path('approach','en'),
      '/journal/':path('about','en'), '/journal':path('about','en'), '/linktree.html':path('services','en'), '/linktree-en.html':path('services','en'),
      '/identity-clarity-audit.html':path('clarity','en'), '/mentorship.html':path('services','en'),
      '/mentions-legales.html':'/legal/mentions-legales.html', '/politique-confidentialite.html':'/legal/confidentialite-cookies.html',
      '/legal/mentions-legales':'/legal/mentions-legales.html', '/legal/conditions-generales':'/legal/conditions-generales.html', '/legal/confidentialite-cookies':'/legal/confidentialite-cookies.html',
      '/en/books.html':path('about','en'), '/en/media.html':path('contact','en'), '/en/private-sessions.html':path('services','en'),
      '/fr/livres.html':path('about','fr'), '/fr/medias.html':path('contact','fr'), '/fr/recherches.html':path('approach','fr'), '/fr/temoignages.html':path('services','fr'),
      '/chroniques/':path('approach','fr'), '/chroniques/index.html':path('approach','fr'), '/chroniques/comprehension-incarnation.html':path('approach','fr'), '/chroniques/repetition-architecturale.html':path('approach','fr'),
      '/recherches/':path('approach','fr'), '/recherches/index.html':path('approach','fr'),
    }
    for rel in ['discordance-incarnation','plafonds-invisibles','repetition-architecturale','retour-au-corps','vide-structurant']:
        aliases['/recherches/'+rel+'.html']=path('approach','fr')
    for source,dest in aliases.items(): redirects.append({'source':source,'destination':dest,'permanent':True})
    (ROOT/'vercel.json').write_text(json.dumps({'$schema':'https://openapi.vercel.sh/vercel.json','framework':None,'buildCommand':None,'outputDirectory':'public','cleanUrls':False,'redirects':redirects,'headers':[{'source':'/post-achats/:path*','headers':[{'key':'X-Robots-Tag','value':'noindex, nofollow'}]},{'source':'/assets/:path*','headers':[{'key':'Cache-Control','value':'public, max-age=3600'}]}]},indent=2)+'\n')
    (PUBLIC/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+DOMAIN+'/sitemap.xml\n')
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    ET.register_namespace('xhtml','http://www.w3.org/1999/xhtml')
    ns='http://www.sitemaps.org/schemas/sitemap/0.9'; xhtml='http://www.w3.org/1999/xhtml'
    root=ET.Element('{'+ns+'}urlset')
    for key,routes in ROUTES.items():
        for lang,urlpath in routes.items():
            item=ET.SubElement(root,'{'+ns+'}url'); ET.SubElement(item,'{'+ns+'}loc').text=DOMAIN+urlpath
            for code in ['en','fr']:
                ET.SubElement(item,'{'+xhtml+'}link',{'rel':'alternate','hreflang':code,'href':DOMAIN+routes[code]})
            ET.SubElement(item,'{'+xhtml+'}link',{'rel':'alternate','hreflang':'x-default','href':DOMAIN+routes['en']})
    ET.ElementTree(root).write(PUBLIC/'sitemap.xml',encoding='utf-8',xml_declaration=True)
    (PUBLIC/'site.webmanifest').write_text(json.dumps({'name':'Morgane Girault','short_name':'Morgane Girault','start_url':'/','display':'browser','background_color':'#f5efe8','theme_color':'#110d0e'})+'\n')
    for f in (PUBLIC/'post-achats').glob('*.html'):
        content=f.read_text()
        if content.strip():
            content=re.sub(r'<meta\b[^>]*name=["\']robots["\'][^>]*>','',content,flags=re.I)
            content=content.replace('</head>','<meta name="robots" content="noindex,nofollow"></head>')
            f.write_text(clean_blank_lines(content))
    notfound='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Page not found | Morgane Girault</title><link rel="stylesheet" href="/assets/css/global.css"></head><body><main class="section container"><span class="eyebrow">404</span><h1 class="section-title">Let’s find a new starting point.</h1><p>This page is not available.</p><div class="button-row"><a class="btn btn-wine" href="/">Home · EN</a><a class="btn btn-outline" href="/fr/">Accueil · FR</a></div></main></body></html>'
    (PUBLIC/'404.html').write_text(notfound+'\n')

def install_analytics():
    """Use one consent-aware GA4 loader on every non-empty published HTML page."""
    js_version=hashlib.sha256((PUBLIC/'assets/js/analytics.js').read_bytes()).hexdigest()[:12]
    css_version=hashlib.sha256((PUBLIC/'assets/css/analytics-consent.css').read_bytes()).hexdigest()[:12]
    tags=f'<link rel="stylesheet" href="/assets/css/analytics-consent.css?v={css_version}">\n<script src="/assets/js/analytics.js?v={js_version}" data-measurement-id="{GA_MEASUREMENT_ID}" defer></script>\n'
    def keep_script(match):
        text=match.group(0)
        if 'googletagmanager.com/gtag/js' in text or re.search(r'\bgtag\s*\(',text) or '/assets/js/analytics.js' in text:
            return ''
        return text
    for f in PUBLIC.rglob('*.html'):
        text=f.read_text()
        if not text.strip() or '</head>' not in text: continue
        text=re.sub(r'<script\b[^>]*>.*?</script>[ \t]*(?:\r?\n)?',keep_script,text,flags=re.I|re.S)
        text=re.sub(r'<link\b[^>]*href=["\'][^"\']*/assets/css/analytics-consent\.css[^"\']*["\'][^>]*>[ \t]*(?:\r?\n)?','',text,flags=re.I)
        text=text.replace('</head>',tags+'</head>',1)
        f.write_text(text)

def build():
    for lang in ['en','fr']:
        home(lang); music(lang); support(lang); custom(lang); services_page(lang); about(lang); approach(lang); contact(lang)
        for key in SERVICES: service_page(key,lang)
    preserve_architecture(); adapt_legal(); configuration(); install_analytics()
    print(f'Built {sum(len(routes) for routes in ROUTES.values())} bilingual public pages, SEO metadata, sitemap and Vercel configuration.')

if __name__=='__main__': build()
