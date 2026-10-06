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
DOMAIN = 'https://www.morgane-girault.com'
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
SOULMAP_COVER = 'https://res.cloudinary.com/diapyc6q1/image/upload/v1791275262/Carte_d_a%CC%82me___clarte%CC%81_et_re%CC%81alignement_ejwdfm.png'
SOULMAP_PRO_COVER = 'https://res.cloudinary.com/diapyc6q1/image/upload/v1791275874/Hors_du_brouillard___couverture_contemplative_hxtib1.png'
SERVICE_CHECKOUTS = {
    'soulmap': 'https://buy.stripe.com/00w00c7DP5Uu9PUa4j8k83Q',
    'soulmappro': 'https://buy.stripe.com/4gMeV64rDfv43rw4JZ8k83R',
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
    'soulmap': {'en': '/en/soulmap.html', 'fr': '/fr/soulmap.html'},
    'soulmappro': {'en': '/en/soulmap-pro.html', 'fr': '/fr/soulmap-pro.html'},
    'bio': {'en': '/en/professional-bio-offer-writing.html', 'fr': '/fr/bio-professionnelle-presentation-offre.html'},
    'booking': {'en': '/en/booking-flow-fix.html', 'fr': '/fr/correction-parcours-reservation.html'},
    'about': {'en': '/en/about.html', 'fr': '/fr/a-propos.html'},
    'approach': {'en': '/en/research.html', 'fr': '/fr/architecture-de-l-incarnation.html'},
    'contact': {'en': '/en/contact.html', 'fr': '/fr/contact.html'},
}

SERVICES = {'soulmap': {'price': 77,
             'en': {'name': 'SoulMap · Your Personalised Soul Book',
                    'title': 'SoulMap: Personalised Written Soul Reading | US$77',
                    'description': 'Understand a life transition, recurring patterns and what you need now. A personal soul reading by Morgane '
                                   'Girault, written as an English PDF book. US$77. No call.',
                    'problem': 'Your life no longer feels like you?',
                    'heading': 'A personal soul reading. A book written for you.',
                    'short': 'Understand what is changing within you, the patterns you repeat and the needs you have learned to put aside.',
                    'audience': 'For women navigating a life transition, outgrowing an old role or wanting to reconnect with themselves.',
                    'intro': 'You can keep everything going and still feel far from yourself. SoulMap brings the threads of your story together, so '
                             'you can recognise what you are carrying and what wants to change.',
                    'body': 'Through mediumship and energetic reading, I create a personal written reading of your current inner landscape. I '
                            'connect your story, recurring patterns, protective habits and family loyalties with the moment you are living now.',
                    'deliver': ['A personalised digital soul book, written in English',
                                'A reading of your current transition, recurring patterns and family loyalties',
                                'Your needs, protective habits and boundaries explored together',
                                'Reflection questions and practical prompts to return to',
                                'Your PDF by email within 7 business days of receiving your complete questionnaire and verifying payment'],
                    'facts': ['Personalised English PDF', 'No appointment needed', 'One-time payment · US$77'],
                    'fit': 'The personal SoulMap explores your inner life, identity and relationships. Its length follows your reading; there is no '
                           'fixed page count. You remain free to decide what resonates and which changes you want to make.',
                    'cta': 'Get my SoulMap — US$77',
                    'question': 'Do I need a call or an appointment?',
                    'answer': 'No. You send your questionnaire after checkout. I prepare your reading and email your personalised PDF. You can read '
                              'it, annotate it and revisit it in your own time.',
                    'question2': 'Is it a generic or automatically generated report?',
                    'answer2': 'No. I prepare a personal reading from your information and the life situation you share. The book follows your story '
                               'rather than a standard set of pages.',
                    'card_deliver': ['A soul reading written personally for you',
                                     'An English PDF to keep and revisit',
                                     'Reflection prompts · No live call'],
                    'card_cta': 'Explore my SoulMap',
                    'quick': 'I want to reconnect with myself'},
             'fr': {'name': 'SoulMap · Ton livre d’âme personnalisé',
                    'title': 'SoulMap : lecture d’âme écrite et personnalisée | 77 USD',
                    'description': 'Comprendre un passage de vie, tes répétitions et tes besoins actuels. Ta lecture d’âme par Morgane Girault, dans '
                                   'un livre PDF personnalisé. 77 USD, sans séance.',
                    'problem': 'Ta vie ne te ressemble plus vraiment ?',
                    'heading': 'Une lecture d’âme. Un livre écrit pour toi.',
                    'short': 'Comprendre ce qui change en toi, les répétitions qui reviennent et les besoins que tu as appris à mettre de côté.',
                    'audience': 'Pour les femmes qui traversent un passage de vie, quittent un ancien rôle ou souhaitent se retrouver.',
                    'intro': 'Tu peux continuer à tout faire fonctionner et te sentir pourtant loin de toi. La SoulMap relie les fils de ton '
                             'histoire pour reconnaître ce que tu portes et ce qui cherche à changer.',
                    'body': 'Par ma médiumnité et ma lecture énergétique, je crée une lecture écrite de ton paysage intérieur actuel. Je relie ton '
                            'histoire, tes répétitions, tes protections et tes loyautés familiales au passage que tu vis.',
                    'deliver': ['Ton livre d’âme numérique, écrit en anglais personnellement pour toi',
                                'Une lecture de ton passage actuel, de tes répétitions et de tes loyautés familiales',
                                'Tes besoins, tes protections et tes limites mis en lien',
                                'Des questions de réflexion et des pistes concrètes à reprendre',
                                'Ton PDF par e-mail sous 7 jours ouvrés après réception du questionnaire complet et vérification du paiement'],
                    'facts': ['PDF personnalisé en anglais', 'Sans rendez-vous', 'Paiement unique · 77 USD'],
                    'fit': 'La SoulMap personnelle explore ta vie intérieure, ton identité et tes relations. Sa longueur suit ta lecture : aucun '
                           'nombre fixe de pages n’est promis. Tu restes libre de retenir ce qui résonne et de choisir les changements que tu '
                           'souhaites faire.',
                    'cta': 'Recevoir ma SoulMap — 77 USD',
                    'question': 'Faut-il une séance ou un rendez-vous ?',
                    'answer': 'Non. Après le paiement, tu m’envoies ton questionnaire. Je prépare ta lecture et t’envoie ton livre PDF par e-mail. '
                              'Tu peux le lire, l’annoter et le reprendre à ton rythme.',
                    'question2': 'Est-ce un rapport générique ou généré automatiquement ?',
                    'answer2': 'Non. Je prépare une lecture personnelle à partir de tes informations et de la situation que tu partages. Le livre '
                               'suit ton histoire plutôt qu’un nombre de pages standard.',
                    'card_deliver': ['Une lecture d’âme écrite personnellement',
                                     'Un livre PDF à conserver et relire',
                                     'Des pistes de réflexion · Sans séance'],
                    'card_cta': 'Découvrir ma SoulMap',
                    'quick': 'J’ai envie de me retrouver'}},
 'bio': {'price': 111,
         'en': {'name': 'Professional Bio & Offer Writing',
                'title': 'Professional Bio Writing Service & Offer Copy',
                'description': 'Help people understand what you do. A professional bio writing service and clear copy for one existing offer, in '
                               'your voice. Online with Morgane Girault. US$111.',
                'short': 'Get a professional bio and a clear description of one existing offer, written in your voice.',
                'audience': 'For practitioners, creatives and independent professionals whose positioning is already defined but whose bio or offer '
                            'presentation does not communicate it clearly.',
                'intro': 'You know what you do. Yet when someone asks you to explain it, your words become too vague, too long or too far from your '
                         'voice. We work from your existing positioning to make the introduction easier to understand.',
                'body': 'I rewrite a professional bio and the presentation of one existing offer using the information and examples you share. The '
                        'aim is to help a reader understand who you help, what they can receive and how to take the next step.',
                'deliver': ['A rewritten professional bio',
                            'A clear presentation of one existing offer',
                            'Language adapted to your voice and intended audience',
                            'One correction round within the agreed scope'],
                'facts': ['Written brief · No call', 'One bio + one offer', '111 USD'],
                'fit': 'This service works from a positioning you have already chosen. If the offer itself still needs to be defined, we can start '
                       'by discussing your brief in writing. A full website rewrite or complete brand strategy is a separate project.',
                'cta': 'Order my bio & offer — US$111',
                'question': 'Can we work in English or French?',
                'answer': 'Yes. We agree on the language and audience before the work begins. The quoted service covers one language; a bilingual '
                          'version can be scoped separately.',
                'question2': 'What should I send you?',
                'answer2': 'Your existing bio, the offer you want to present, the audience it serves and a few examples of language that feels like '
                           'you. We confirm the length and placement before payment.',
                'problem': 'Hard to explain what you do?',
                'heading': 'A professional bio that makes your work clear.',
                'card_deliver': ['One professional bio', 'One existing offer rewritten clearly', 'One agreed correction round'],
                'card_cta': 'Make my words clearer',
                'quick': 'How do I explain my work?'},
         'fr': {'name': 'Bio professionnelle & présentation d’offre',
                'title': 'Rédaction de bio professionnelle & présentation d’offre',
                'description': 'Rends ton activité facile à comprendre avec une bio professionnelle et la présentation d’une offre existante, dans '
                               'ta voix. À distance avec Morgane Girault. 111 USD.',
                'short': 'Une bio professionnelle et une présentation claire d’une offre existante, écrites dans ta voix.',
                'audience': 'Pour les praticiennes, créatives et indépendantes dont le positionnement est défini, mais dont la bio ou la '
                            'présentation d’offre ne l’exprime pas encore clairement.',
                'intro': 'Tu sais ce que tu fais. Pourtant, au moment de le présenter, les mots deviennent trop vagues, trop longs ou trop éloignés '
                         'de ta voix. Nous partons de ton positionnement existant pour rendre cette présentation plus claire.',
                'body': 'Je réécris une bio professionnelle et la présentation d’une offre existante à partir des éléments que tu me transmets. '
                        'L’objectif : aider la personne qui te lit à comprendre qui tu accompagnes, ce qu’elle reçoit et comment avancer.',
                'deliver': ['Une bio professionnelle réécrite',
                            'Une présentation claire d’une offre existante',
                            'Des formulations adaptées à ta voix et à ton audience',
                            'Un retour de correction dans le périmètre convenu'],
                'facts': ['Brief écrit · Sans séance', 'Une bio + une offre', '111 USD'],
                'fit': 'Cette intervention part d’un positionnement déjà choisi. Si l’offre reste à définir, nous en discutons par écrit. '
                       'La réécriture d’un site complet ou une stratégie de marque demandent un autre périmètre.',
                'cta': 'Commander mes textes — 111 USD',
                'question': 'Peut-on travailler en français ou en anglais ?',
                'answer': 'Oui. Nous choisissons la langue et l’audience avant de commencer. Le tarif couvre une langue ; une version bilingue peut '
                          'faire l’objet d’une proposition complémentaire.',
                'question2': 'Que dois-je te transmettre ?',
                'answer2': 'Ta bio actuelle, l’offre à présenter, son public et quelques exemples de formulations qui te ressemblent. Nous '
                           'confirmons la longueur et l’usage des textes avant le paiement.',
                'problem': 'Difficile d’expliquer ce que tu proposes ?',
                'heading': 'Une bio professionnelle qui rend ton activité claire.',
                'card_deliver': ['Une bio professionnelle', 'Une offre existante présentée clairement', 'Un retour de correction convenu'],
                'card_cta': 'Clarifier mes textes',
                'quick': 'Comment présenter mon activité ?'}},
 'booking': {'price': 149,
             'en': {'name': 'Booking Flow Fix',
                    'title': 'Booking Link & Form Fix for Your Website | US$149',
                    'description': 'A booking link, button or form is blocking clients? Get one website booking issue reviewed, fixed and tested. '
                                   'Compatibility checked before payment. US$149.',
                    'short': 'Correct one broken link, button, form or booking connection on a compatible website.',
                    'audience': 'For independent professionals and practitioners with an existing website and one specific problem in the route from '
                                'interest to booking.',
                    'intro': 'Someone is ready to work with you, but a button leads to the wrong page, a form does not work or the booking step is '
                             'hard to find. A small technical problem can interrupt a clear intention.',
                    'body': 'We identify one precise issue on a website or tool I can work with, confirm the correction and verify the relevant '
                            'journey after the change. I review compatibility before you pay.',
                    'deliver': ['A correction to one agreed booking issue',
                                'Work on the relevant link, button, form or connection',
                                'Verification of the corrected journey',
                                'One correction round relating to the agreed intervention'],
                    'facts': ['One defined issue', 'Review by email · No call', '149 USD'],
                    'fit': 'A website rebuild, several unrelated errors, a new custom integration or work outside a supported setup requires a '
                           'separate proposal. I confirm what is included and a realistic delivery date before payment.',
                    'cta': 'Show me the issue — US$149',
                    'question': 'Can you fix any website or booking tool?',
                    'answer': 'I first review your setup and the problem. I accept the intervention only when it fits a website or tool I can work '
                              'with and a clearly defined scope.',
                    'question2': 'What should I send before we begin?',
                    'answer2': 'The page URL, the step that should work, what happens instead and a screenshot if helpful. Please do not send '
                               'passwords or secret keys through the inquiry form.',
                    'problem': 'A booking link or form isn’t working?',
                    'heading': 'Fix the step that stops clients from booking.',
                    'card_deliver': ['One specific issue corrected',
                                     'Compatibility and scope checked before payment',
                                     'The corrected booking journey tested'],
                    'card_cta': 'Get my booking issue reviewed',
                    'quick': 'Why can’t clients book?'},
             'fr': {'name': 'Correction du parcours de réservation',
                    'title': 'Correction de lien ou formulaire de réservation | 149 USD',
                    'description': 'Un lien, bouton ou formulaire empêche tes clientes de réserver ? Un problème précis corrigé et testé sur un site '
                                   'compatible. Vérification avant paiement. 149 USD.',
                    'short': 'Corriger un lien, un bouton, un formulaire ou une connexion de réservation sur un site compatible.',
                    'audience': 'Pour les indépendantes et praticiennes qui possèdent déjà un site et rencontrent un problème précis entre l’intérêt '
                                'd’une cliente et sa réservation.',
                    'intro': 'Une personne veut travailler avec toi, mais un bouton mène au mauvais endroit, un formulaire ne fonctionne pas ou la '
                             'réservation est difficile à trouver. Un petit problème technique peut interrompre une intention claire.',
                    'body': 'Nous identifions un problème précis sur un site ou un outil que je maîtrise, convenons de la correction et vérifions '
                            'ensuite le parcours concerné. Je regarde la compatibilité avant que tu paies.',
                    'deliver': ['La correction d’un problème de réservation défini ensemble',
                                'Une intervention sur le lien, bouton, formulaire ou raccordement concerné',
                                'La vérification du parcours corrigé',
                                'Un retour de correction lié à cette intervention'],
                    'facts': ['Un problème défini', 'Vérification par écrit', '149 USD'],
                    'fit': 'Une refonte de site, plusieurs erreurs distinctes ou une nouvelle intégration complexe font l’objet d’une proposition '
                           'séparée. Le contenu et un délai réaliste sont confirmés avant le paiement.',
                    'cta': 'Te montrer le problème — 149 USD',
                    'question': 'Peux-tu intervenir sur tous les sites et outils ?',
                    'answer': 'Je regarde d’abord ton installation et le problème rencontré. L’intervention est acceptée lorsqu’elle correspond à un '
                              'outil que je maîtrise et à un périmètre précis.',
                    'question2': 'Que dois-je t’envoyer pour commencer ?',
                    'answer2': 'L’URL de la page, l’étape attendue, ce qui se passe à la place et une capture si nécessaire. N’envoie pas de mot de '
                               'passe ou de clé secrète dans le formulaire de contact.',
                    'problem': 'Un lien ou un formulaire bloque les réservations ?',
                    'heading': 'Corriger l’étape qui empêche tes clientes de réserver.',
                    'card_deliver': ['Un problème précis corrigé', 'Compatibilité et périmètre vérifiés avant paiement', 'Le parcours corrigé testé'],
                    'card_cta': 'Faire examiner mon problème',
                    'quick': 'Pourquoi la réservation bloque ?'}}}

SERVICES['soulmappro'] = {'price': 144,
 'en': {'name': 'SoulMap Pro · Out of the Fog',
        'title': 'SoulMap Pro: Written Business Reading | US$144',
        'description': 'A personal written reading of your professional identity, visibility and recurring business patterns. SoulMap Pro by Morgane '
                       'Girault. English PDF, US$144. No call.',
        'problem': 'Your work no longer reflects who you are?',
        'heading': 'See your work — and your place in it — more clearly.',
        'short': 'A personal written reading of the identity, visibility and recurring patterns shaping your business or professional project.',
        'body': 'SoulMap Pro looks at the woman behind the business and how her identity takes form in her activity. I connect your professional '
                'story, your contribution, the patterns you repeat and the transition your work is moving through.',
        'facts': ['Personalised English PDF', 'No appointment needed', 'One-time payment · US$144'],
        'deliver': ['A professional reading written personally for you in English',
                    'Your identity, contribution, visibility and expression explored together',
                    'Connections between offers, clients, pricing and recurring business patterns',
                    'Reflection questions and first directions to explore',
                    'Your PDF by email within 7–10 business days of receiving your complete questionnaire and verifying payment'],
        'fit': 'This is a spiritual reading of your professional identity and patterns. It can inform your reflection on your business, but it does '
               'not replace market research, a financial audit or an operational business strategy. There is no revenue or growth guarantee.',
        'cta': 'Get my SoulMap Pro — US$144',
        'question': 'Can I order if I am starting a business?',
        'answer': 'Yes, if you have a defined professional project, a clear area of work or an offer already taking shape. Share the real context in '
                  'your questionnaire. If your project is still a vague idea, ask me about suitability before ordering.',
        'question2': 'Is the reading generated automatically?',
        'answer2': 'No. I prepare each reading personally from your information and professional context. The structure and length follow your '
                   'project; there is no fixed page count.',
        'card_deliver': ['Your professional identity and recurring patterns',
                         'A personal English PDF to keep',
                         'Written questionnaire · No live call'],
        'card_cta': 'Explore SoulMap Pro',
        'quick': 'My work no longer reflects me'},
 'fr': {'name': 'SoulMap Pro · Out of the Fog',
        'title': 'SoulMap Pro : lecture professionnelle écrite | 144 USD',
        'description': 'Une lecture écrite de ton identité professionnelle, de ta visibilité et de tes répétitions dans l’activité. SoulMap Pro par '
                       'Morgane Girault. PDF en anglais, 144 USD.',
        'problem': 'Ton activité ne reflète plus qui tu es ?',
        'heading': 'Voir ton activité — et ta place à l’intérieur — plus clairement.',
        'short': 'Une lecture écrite de l’identité, de la visibilité et des répétitions qui façonnent ton activité ou ton projet professionnel.',
        'body': 'SoulMap Pro regarde la femme derrière l’activité et la manière dont son identité prend forme dans l’entreprise. Je relie ton '
                'histoire professionnelle, ta contribution, tes répétitions et le passage que ton activité traverse.',
        'facts': ['PDF personnalisé en anglais', 'Sans rendez-vous', 'Paiement unique · 144 USD'],
        'deliver': ['Une lecture professionnelle écrite personnellement en anglais',
                    'Ton identité, ta contribution, ta visibilité et ton expression mises en lien',
                    'Les liens entre offres, clientes, prix et répétitions professionnelles',
                    'Des questions de réflexion et des premières directions à explorer',
                    'Ton PDF par e-mail sous 7 à 10 jours ouvrés après réception du questionnaire complet et vérification du paiement'],
        'fit': 'Il s’agit d’une lecture spirituelle de ton identité professionnelle et de tes répétitions. Elle peut nourrir ta réflexion sur ton '
               'activité, mais ne remplace pas une étude de marché, un audit financier ou une stratégie opérationnelle. Aucun chiffre d’affaires ni '
               'résultat de croissance n’est garanti.',
        'cta': 'Recevoir ma SoulMap Pro — 144 USD',
        'question': 'Puis-je commander si je crée mon activité ?',
        'answer': 'Oui, si tu portes un projet professionnel défini, un univers de travail clair ou une offre qui prend déjà forme. Décris la '
                  'réalité de ton projet dans le questionnaire. Si l’idée reste très vague, demande-moi d’abord si la lecture est adaptée.',
        'question2': 'La lecture est-elle générée automatiquement ?',
        'answer2': 'Non. Je prépare chaque lecture personnellement à partir de tes informations et de ton contexte professionnel. Sa structure et sa '
                   'longueur suivent ton projet ; aucun nombre fixe de pages n’est promis.',
        'card_deliver': ['Ton identité et tes répétitions professionnelles',
                         'Un PDF personnel en anglais à conserver',
                         'Questionnaire écrit · Sans séance'],
        'card_cta': 'Découvrir SoulMap Pro',
        'quick': 'Mon activité ne me reflète plus'}}

LABELS = {
 'en': {'music':'Music','services':'Work with me','about':'About','contact':'Contact','home':'Home','skip':'Skip to content','menu':'Menu','explore':'Explore','follow':'Listen & follow','terms':'Terms (French)','privacy':'Privacy','legal':'Legal notice','rights':'All rights reserved','based':'Based in Da Nang · Working online internationally','deliver':'What you receive','fit':'A clear scope','next':'How we begin','faq':'A few useful answers','related':'Other ways to work together','request':'Tell me about your project','quote':'Request a quote','approach':'Intuition, made practical'},
 'fr': {'music':'Musique','services':'Travailler ensemble','about':'À propos','contact':'Contact','home':'Accueil','skip':'Aller au contenu','menu':'Menu','explore':'Explorer','follow':'Écouter & suivre','terms':'CGV','privacy':'Confidentialité','legal':'Mentions légales','rights':'Tous droits réservés','based':'À Da Nang · À distance, à l’international','deliver':'Ce que tu reçois','fit':'Un périmètre clair','next':'Comment nous commençons','faq':'Quelques réponses utiles','related':'D’autres façons de travailler ensemble','request':'Parlons de ton projet','quote':'Demander un devis','approach':'L’intuition prend forme'}
}

LABELS['en']['support'] = 'Support my music'
LABELS['fr']['support'] = 'Soutenir ma musique'

LABELS['en']['soulmappro'] = 'SoulMap Pro'
LABELS['fr']['soulmappro'] = 'SoulMap Pro'
LABELS['en']['soulmap'] = 'SoulMap'
LABELS['fr']['soulmap'] = 'SoulMap'

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
    items=''.join(f'<li><a href="{path(k,lang)}"'+(' aria-current="page"' if k==key else '')+f'>{("Support" if lang=="en" else "Soutenir") if k=="support" else l[k]}</a></li>' for k in ['soulmap','soulmappro','services','music','support','contact'])
    return f'''<a class="skip-link" href="#main">{l['skip']}</a><header class="site-header"><nav class="nav" aria-label="{'Main navigation' if lang=='en' else 'Navigation principale'}"><a class="logo" href="{path('home',lang)}">Morgane Girault</a><button class="mobile-menu-btn" type="button" aria-expanded="false" aria-controls="primary-navigation">{l['menu']}</button><ul class="nav-links" id="primary-navigation">{items}<li><a class="language" href="{path(key,other)}" lang="{other}" hreflang="{other}" aria-label="{'Lire cette page en français' if other=='fr' else 'Read this page in English'}">{other.upper()}</a></li></ul></nav></header>'''

def footer(lang):
    l=LABELS[lang]; legal='/legal-notice.html' if lang=='en' else '/legal/mentions-legales.html'; privacy='/privacy-policy.html' if lang=='en' else '/legal/confidentialite-cookies.html'
    return f'''<footer class="footer"><div class="container"><div class="footer-grid"><div class="footer-brand-block"><div class="footer-brand">Morgane<br>Girault</div><small>{l['based']}</small></div><div><h3>{l['explore']}</h3>{''.join(link(path(k,lang),l[k],'') for k in ['soulmap','soulmappro','services','music','support','about','contact'])}</div><div><h3>{l['follow']}</h3>{link(SPOTIFY,'Spotify','',True)}{link(APPLE,'Apple Music','',True)}{link(YOUTUBE,'YouTube','',True)}{link(INSTAGRAM,'Instagram','',True)}</div></div><div class="footer-bottom"><span>© <span data-year>2026</span> Morgane Girault · {l['rights']}</span><div class="legal-links">{link(legal,l['legal'],'')}{link(privacy,l['privacy'],'')}{link('/legal/conditions-generales.html',l['terms'],'')}</div></div></div></footer>'''

def metadata(key,lang,title,description,service=None,stylesheet='global.css',include_script=True):
    url=DOMAIN+path(key,lang)
    social_image=SOULMAP_PRO_COVER if key=='soulmappro' else SOULMAP_COVER if key in ['soulmap','home'] else PORTRAIT
    css_version=hashlib.sha256((PUBLIC/'assets/css'/stylesheet).read_bytes()).hexdigest()[:12]
    stylesheet+='?v='+css_version
    script_version=hashlib.sha256((PUBLIC/'assets/js/main.js').read_bytes()).hexdigest()[:12]
    graph=[{'@type':'Person','@id':DOMAIN+'/#morgane','name':'Morgane Girault','url':DOMAIN+'/', 'image':PORTRAIT,'jobTitle':'Medium, soul cartographer, artist and songwriter','sameAs':[SPOTIFY,APPLE,YOUTUBE,INSTAGRAM]}, {'@type':'WebPage','@id':url+'#page','url':url,'name':title,'description':description,'inLanguage':lang,'isPartOf':{'@id':DOMAIN+'/#website'},'about':{'@id':DOMAIN+'/#morgane'}}]
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
        if key in ['soulmap','soulmappro']: item['image']=social_image
        graph.append(item)
    alternates=''.join(f'<link rel="alternate" hreflang="{code}" href="{DOMAIN+path(key,code)}">' for code in ['en','fr'])
    script=f'<script src="/assets/js/main.js?v={script_version}" defer></script>' if include_script else ''
    return f'''<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} | Morgane Girault</title><meta name="description" content="{esc(description)}"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="author" content="Morgane Girault"><link rel="canonical" href="{url}">{alternates}<link rel="alternate" hreflang="x-default" href="{DOMAIN+path(key,'en')}"><meta property="og:type" content="website"><meta property="og:title" content="{esc(title)} | Morgane Girault"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{social_image}"><meta property="og:image:alt" content="Morgane Girault"><meta property="og:site_name" content="Morgane Girault"><meta property="og:locale" content="{'en_US' if lang=='en' else 'fr_FR'}"><meta property="og:locale:alternate" content="{'fr_FR' if lang=='en' else 'en_US'}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(description)}"><meta name="twitter:image" content="{social_image}"><meta name="theme-color" content="#110d0e"><link rel="icon" href="{PORTRAIT}"><link rel="preconnect" href="https://res.cloudinary.com"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="/assets/css/{stylesheet}"><script type="application/ld+json">{json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('</','<\\/')}</script>{script}'''

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
    return '<div class="offer-grid">'+''.join(f'<article class="offer-card'+(' featured' if k=='soulmap' else '')+f'"><span class="eyebrow">{esc(SERVICES[k][lang]["name"])}</span><h3>{esc(SERVICES[k][lang]["problem"])}</h3><p>{esc(SERVICES[k][lang]["short"])}</p><p class="price">{SERVICES[k]["price"]}<small>USD</small></p>{bullet(SERVICES[k][lang]["card_deliver"])}{link(path(k,lang),SERVICES[k][lang]["card_cta"],"btn btn-dark")}</article>' for k in keys)+'</div>'

def book_visual(lang,pro=False):
    cover=SOULMAP_PRO_COVER if pro else SOULMAP_COVER
    alt=('SoulMap Pro — Out of the Fog, by Morgane Girault' if pro else 'SoulMap — A Path to Clarity & Realignment, by Morgane Girault')
    return f'<figure class="soul-book-cover"><img src="{cover}" alt="{esc(alt)}" width="1053" height="1494" loading="lazy"></figure>'

def soulmap_feature(lang):
    en=lang=='en'
    return f'''<section class="section soulmap-feature" id="soulmap"><div class="container soulmap-feature-grid"><div>{book_visual(lang)}</div><div><span class="eyebrow">{'SoulMap · A written soul reading' if en else 'SoulMap · Une lecture d’âme écrite'}</span><h2 class="section-title">{'Understand the chapter<br>you are living now.' if en else 'Comprendre le passage<br>que tu vis aujourd’hui.'}</h2><p class="lead">{'A personalised soul reading, written as your own book. Through mediumship and energetic reading, I connect your current transition, repeating patterns and family loyalties with the needs and choices that are becoming clearer within you.' if en else 'Une lecture d’âme personnalisée, dans un livre écrit pour toi. Par ma médiumnité et ma lecture énergétique, je relie ton passage actuel, tes répétitions et tes loyautés familiales aux besoins et aux choix qui commencent à se préciser en toi.'}</p>{bullet(SERVICES['soulmap'][lang]['card_deliver'])}<p class="soul-price">77 <small>USD · {'One-time payment' if en else 'Paiement unique'}</small></p><div class="button-row">{link(path('soulmap',lang),'Discover my SoulMap' if en else 'Découvrir ma SoulMap','btn btn-wine')}</div></div></div></section>'''

def home(lang):
    en=lang=='en'
    title='SoulMap · Personalised Written Soul Reading' if en else 'SoulMap · Ton livre d’âme personnalisé'
    desc='Your life no longer feels like you? SoulMap is a personal soul reading by medium Morgane Girault, written as an English PDF book. US$77, delivered by email. No call.' if en else 'Ta vie ne te ressemble plus ? SoulMap, une lecture d’âme personnelle par Morgane Girault, médium, dans un livre PDF en anglais. 77 USD, par e-mail, sans séance.'
    h1='When your life no longer<br>feels like you.' if en else 'Quand ta vie ne te<br>ressemble plus vraiment.'
    intro='SoulMap is a personal soul reading, written as your own book. Understand the patterns you keep repeating, what you have outgrown and what you need now.' if en else 'SoulMap est une lecture d’âme personnelle, dans un livre écrit pour toi. Comprendre tes répétitions, ce que tu as dépassé et les besoins qui émergent aujourd’hui.'
    body=f'''<section class="work-hero"><div class="container work-hero-grid"><div class="work-hero-copy"><span class="eyebrow">{'SoulMap · Personalised written soul reading' if en else 'SoulMap · Lecture d’âme écrite et personnalisée'}</span><h1>{h1}</h1><p class="lead">{esc(intro)}</p><p class="hero-format">{'Made for you · English PDF by email · No appointment needed' if en else 'Créé pour toi · PDF en anglais par e-mail · Sans rendez-vous'}</p><div class="button-row">{link(path('soulmap',lang),'Explore SoulMap · US$77' if en else 'Découvrir SoulMap · 77 USD','btn btn-wine')}{link(path('soulmap',lang)+'#inside','What’s inside my book?' if en else 'Que contient mon livre ?','btn btn-outline')}</div><p class="work-hero-note">{'For women navigating a life transition, outgrowing an old role or wanting to reconnect with themselves.' if en else 'Pour les femmes qui traversent un passage de vie, quittent un ancien rôle ou souhaitent se retrouver.'}</p></div><figure class="work-hero-portrait work-hero-book"><img src="{SOULMAP_COVER}" alt="SoulMap — A Path to Clarity &amp; Realignment, by Morgane Girault" fetchpriority="high" width="1053" height="1494"><figcaption><strong>Morgane Girault</strong><span>{'Medium · Soul cartographer · Creator' if en else 'Médium · Cartographe d’âmes · Créatrice'}</span></figcaption></figure></div><nav class="container need-links" aria-label="{'Find help for your situation' if en else 'Trouver une aide pour ta situation'}">{link(path('soulmap',lang),'I feel disconnected from myself' if en else 'Je me sens loin de moi','need-link')}{link(path('soulmap',lang)+'#patterns','I keep repeating the same patterns' if en else 'Je retrouve les mêmes répétitions','need-link')}{link(path('soulmap',lang)+'#inside','I’m ready for a new chapter' if en else 'J’ai envie d’un nouveau chapitre','need-link')}</nav></section>'''
    body+=soulmap_feature(lang)+soulmap_pro_feature(lang)
    body+=f'''<section class="section wine"><div class="container split top"><div><span class="eyebrow">{'The person behind your book' if en else 'La personne derrière ton livre'}</span><h2 class="section-title">{'I bring the threads<br>of your story together.' if en else 'Je relie les fils<br>de ton histoire.'}</h2></div><div><p class="lead">{'I’m Morgane, a medium, soul cartographer and creator. My mediumship and energetic reading are at the heart of SoulMap. I look at the connection between what you feel, the roles you carry and the changes taking shape in your life.' if en else 'Je suis Morgane, médium, cartographe d’âmes et créatrice. Ma médiumnité et ma lecture énergétique sont au cœur de la SoulMap. Je regarde les liens entre ce que tu ressens, les rôles que tu portes et les changements qui prennent forme dans ta vie.'}</p><p>{'Your book gives that reading a form you can keep: words to reflect on, questions to explore and practical prompts to take into your everyday choices.' if en else 'Ton livre donne à cette lecture une forme que tu peux conserver : des mots à laisser résonner, des questions à explorer et des pistes à reprendre dans tes choix quotidiens.'}</p>{link(path('about',lang),'Meet Morgane' if en else 'Découvrir Morgane','btn btn-light')}</div></div></section>'''
    body+=f'''<section class="section offers-section" id="services"><div class="container"><div class="section-head"><span class="eyebrow">{'Other services · Written briefs · No live calls' if en else 'Autres prestations · Échanges écrits · Sans séance'}</span><h2 class="section-title">{'A practical project<br>you need help with?' if en else 'Un projet concret<br>pour lequel tu as besoin d’aide ?'}</h2><p class="lead">{'I also write professional bios and offer copy, and fix specific website booking issues. We work from your written brief and exchange feedback by email.' if en else 'Je rédige aussi des bios et des présentations d’offres, et corrige des problèmes précis de réservation sur un site. Nous partons de ton brief écrit et échangeons les retours par e-mail.'}</p></div>{cards(lang,['bio','booking'])}</div></section>'''
    body+=f'''<section class="section home-music" id="music"><div class="container"><div class="section-head"><span class="eyebrow">{'Music & creation' if en else 'Musique & création'}</span><h2 class="section-title">{'There is music here, too.' if en else 'Il y a aussi la musique.'}</h2><p class="lead">{'Soul, jazz and R&B are another part of my work. Listen to my releases, or send me a story you would like to turn into lyrics or a melody.' if en else 'La soul, le jazz et le R&B font aussi partie de mon travail. Écoute mes créations ou envoie-moi une histoire que tu aimerais transformer en paroles ou en mélodie.'}</p></div><div class="entry-grid"><article class="entry music-entry"><span class="eyebrow">{'Listen' if en else 'Écouter'}</span><h3>{'Explore my music.' if en else 'Découvrir ma musique.'}</h3><p>{'Songs about love, freedom and finding your way back to yourself.' if en else 'Des chansons autour de l’amour, de la liberté et du retour à soi.'}</p>{link(path('music',lang),'Listen to the releases' if en else 'Écouter les créations')}</article><article class="entry"><span class="eyebrow">{'Paid custom songwriting · By quote' if en else 'Création musicale payante · Sur devis'}</span><h3>{'Your story, in a song.' if en else 'Ton histoire, en chanson.'}</h3><p>{'Personal lyrics and melodies for people, artists and creative projects. Send your written brief; we agree on the format, price and intended use before I begin.' if en else 'Des paroles et des mélodies pour des personnes, des artistes et des projets créatifs. Envoie-moi ton brief : le format, le tarif et l’usage sont convenus par écrit avant de commencer.'}</p>{link(path('custom',lang),'Explore a custom commission' if en else 'Découvrir une création sur mesure')}</article></div></div></section>'''
    write_page('home',lang,title,desc,body+featured_release(lang))


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
    title='SoulMap & Personalised Services by Email' if en else 'SoulMap & prestations personnalisées par e-mail'
    desc='SoulMap at US$77, SoulMap Pro at US$144, professional bio and offer writing at US$111, and website booking fixes at US$149. Personalised work by email, without live calls.' if en else 'SoulMap à 77 USD, SoulMap Pro à 144 USD, une bio et une offre à 111 USD, ou un problème de réservation corrigé à 149 USD. Prestations personnalisées par écrit, sans séance.'
    body=hero(lang,'Personal work. Something you can keep.' if en else 'Un travail personnel. Une forme à conserver.','A written soul reading, clearer words for your work or a website issue corrected. Choose the result you need; we work through written information and feedback.' if en else 'Une lecture d’âme écrite, des mots plus clairs pour ton activité ou une correction sur ton site. Choisis le résultat dont tu as besoin : nous travaillons à partir d’informations et de retours écrits.','By email · No live calls' if en else 'Par e-mail · Sans séance')
    body+=soulmap_feature(lang)+soulmap_pro_feature(lang)
    body+='<section class="section"><div class="container"><h2 class="section-title">'+('For your business or creative project.' if en else 'Pour ton activité ou ton projet créatif.')+'</h2>'+cards(lang,['bio','booking'])+'<p class="offer-choice">'+('Looking for personal lyrics or a melody? Custom songwriting is available from a written brief, by quote.' if en else 'Tu cherches des paroles ou une mélodie ? La création musicale sur mesure part d’un brief écrit, sur devis.')+' '+link(path('custom',lang),'Explore custom songwriting' if en else 'Découvrir la création musicale')+'</p></div></section>'
    body+=steps(lang,[('Send the information','SoulMap starts with a questionnaire after checkout. For writing or a website fix, send your brief first.'),('I prepare your work','The work is personalised around the information and scope we have agreed in writing.'),('Receive your result','Your PDF, text or corrected website journey, with the feedback included in your chosen offer.')] if en else [('Transmettre les informations','Pour SoulMap, le questionnaire suit le paiement. Pour les textes ou une correction, envoie d’abord ton brief.'),('Je prépare ton résultat','Le travail est personnalisé à partir des informations et du périmètre convenus par écrit.'),('Recevoir le résultat','Ton PDF, tes textes ou ton parcours corrigé, avec les retours inclus dans l’offre choisie.')])
    write_page('services',lang,title,desc,body)

def soulmap_page(lang):
    en=lang=='en'; data=SERVICES['soulmap']; d=data[lang]
    body=hero(lang,d['heading'],d['short'],'SoulMap · '+('Personalised written soul reading' if en else 'Lecture d’âme écrite et personnalisée'),'services',d['facts'])
    body=body.replace('</div></section>',f'<div class="button-row">{link(service_url("soulmap",lang),d["cta"],"btn btn-light")}{link("#inside","See what’s inside" if en else "Découvrir le contenu","btn btn-outline")}</div></div></section>',1)
    familiar=['Your life looks fine from the outside, but you no longer recognise yourself in it.','You have become the person who holds everything together, while your own needs stay in the background.','The same relationship patterns, guilt or fear of disappointing others keep returning.','An old role, relationship or way of living no longer fits, but the next chapter is still unclear.'] if en else ['De l’extérieur, tout semble fonctionner, mais tu ne te reconnais plus dans ta vie.','Tu es devenue celle qui tient tout ensemble, tandis que tes besoins restent en arrière-plan.','Les mêmes répétitions relationnelles, la culpabilité ou la peur de décevoir reviennent.','Un ancien rôle, une relation ou une façon de vivre ne te correspond plus, mais la suite reste floue.']
    themes=[('Your current turning point','What this period brings to the surface, what feels saturated and what you are outgrowing.'),('The roles you carry','The woman others see, the woman you feel within, and the gap between the two.'),('Patterns and protections','The habits that once helped you feel safe: controlling, overthinking, adapting or carrying too much.'),('Family loyalties','Inherited roles, expectations and the sense of duty that can shape your choices.'),('Your needs and boundaries','What you need to make more room for, and where your own voice has been put aside.'),('Your next chapter','Reflection questions and practical prompts to explore different choices in your everyday life.')] if en else [('Ton passage actuel','Ce que cette période révèle, ce qui sature et ce que tu es en train de dépasser.'),('Les rôles que tu portes','La femme que les autres voient, celle que tu ressens en toi et l’écart entre les deux.'),('Tes répétitions et protections','Les habitudes qui t’ont aidée à te sentir en sécurité : contrôler, analyser, t’adapter ou porter trop.'),('Tes loyautés familiales','Les rôles hérités, les attentes et le sentiment de devoir qui peuvent orienter tes choix.'),('Tes besoins et tes limites','Ce qui demande plus de place et les endroits où ta voix a été mise de côté.'),('Ton prochain chapitre','Des questions de réflexion et des pistes concrètes pour explorer d’autres choix au quotidien.')]
    body+=f'''<section class="section" id="patterns"><div class="container detail-grid"><div class="prose"><h2>{'Do you recognise yourself here?' if en else 'Est-ce que tu te reconnais ici ?'}</h2>{bullet(familiar)}<h2>{'A reading that connects your story.' if en else 'Une lecture qui relie ton histoire.'}</h2>{paragraph(d['body'])}{paragraph('I write your SoulMap as a coherent personal book, with room for your sensitivity, your story and the transition you are living. It offers language and connections to reflect on, while leaving your choices in your hands.' if en else 'J’écris ta SoulMap comme un livre personnel cohérent, avec une place pour ta sensibilité, ton histoire et le passage que tu vis. Il propose des mots et des liens à explorer, tout en laissant tes choix entre tes mains.')}</div><aside class="aside"><span class="eyebrow">{'Your personalised soul book' if en else 'Ton livre d’âme personnalisé'}</span><p class="price">77 <small>USD</small></p>{paragraph('One-time payment. A personal English PDF, delivered by email. No live call or appointment.' if en else 'Paiement unique. Un livre PDF personnel écrit en anglais, livré par e-mail. Sans séance ni rendez-vous.')}{link(service_url('soulmap',lang),d['cta'],'btn btn-wine')}<p class="form-note">{'Delivery within 7 business days after I receive your complete questionnaire and verify payment.' if en else 'Livraison sous 7 jours ouvrés après réception de ton questionnaire complet et vérification du paiement.'}</p>{link(request_url('soulmap',lang),'A question before ordering?' if en else 'Une question avant de commander ?')}</aside></div></section>'''
    body+='<section class="section offers-section" id="inside"><div class="container"><div class="section-head"><span class="eyebrow">'+('Inside your SoulMap' if en else 'Dans ta SoulMap')+'</span><h2 class="section-title">'+('Your inner landscape,<br>brought into words.' if en else 'Ton paysage intérieur,<br>mis en mots.')+'</h2><p class="lead">'+('These themes form the thread of your reading. Their place and depth depend on your story; your book is not a fixed-length report.' if en else 'Ces thèmes composent le fil de ta lecture. Leur place et leur profondeur dépendent de ton histoire : ton livre n’est pas un rapport de longueur fixe.')+'</p></div><div class="soul-themes">'+''.join('<article><h3>'+esc(t)+'</h3>'+paragraph(p)+'</article>' for t,p in themes)+'</div></div></section>'
    body+='<section class="section"><div class="container split"><div>'+book_visual(lang)+'</div><div class="prose"><h2>'+('A book you can return to.' if en else 'Un livre que tu peux reprendre.')+'</h2>'+paragraph('Read it in your own time. Underline what resonates, sit with a question or come back to a passage when your circumstances change. Alongside the reading, reflection questions and practical prompts help you bring it into your daily life.' if en else 'Lis-le à ton rythme. Souligne ce qui résonne, laisse une question ouverte ou reviens à un passage quand ta situation évolue. Des questions de réflexion et des pistes concrètes accompagnent la lecture pour la relier à ton quotidien.')+'<h2>'+('What you receive' if en else 'Ce que tu reçois')+'</h2>'+bullet(d['deliver'])+'</div></div></section>'
    body+=steps(lang,[('Order your SoulMap · US$77','A one-time payment through Stripe. The next page contains your questionnaire.'),('Send your questionnaire','Your full name, birth details and a few written answers about your current life situation. If you do not know your birth time, indicate it.'),('Receive your personal book','I verify payment and your information, then email your English PDF within 7 business days of receiving your complete answers. No appointment to schedule.')] if en else [('Commander ta SoulMap · 77 USD','Un paiement unique via Stripe. La page suivante contient ton questionnaire.'),('Envoyer ton questionnaire','Ton identité complète, tes informations de naissance et quelques réponses écrites sur ta situation actuelle. Si l’heure de naissance est inconnue, indique-le.'),('Recevoir ton livre personnel','Je vérifie le paiement et tes informations, puis t’envoie ton PDF en anglais sous 7 jours ouvrés à compter de la réception des réponses complètes. Sans rendez-vous.')])
    extra=[('When will I receive it?','Within 7 business days after your complete questionnaire is received and payment is verified. It is created personally, so it is not an instant download.'),('What information do you need?','All your first names, surname, date of birth, birth time if known, city and country of birth, your checkout email, and a few answers about what you are living now.'),('Is this the personal SoulMap or SoulMap Pro?','This is the personal SoulMap: your inner life, identity, relationships and current transition. SoulMap Pro, focused on business, is a separate offer.'),('How long is the book?','There is no fixed page count. Its structure and depth follow your personal reading. You receive a digital PDF to keep; there is no printed edition included.')] if en else [('Quand vais-je recevoir mon livre ?','Sous 7 jours ouvrés après réception du questionnaire complet et vérification du paiement. Il est créé personnellement : ce n’est pas un téléchargement instantané.'),('Quelles informations faut-il transmettre ?','Tous tes prénoms, ton nom, ta date de naissance, l’heure si tu la connais, la ville et le pays de naissance, l’e-mail utilisé au paiement et quelques réponses sur ce que tu vis aujourd’hui.'),('Est-ce la SoulMap personnelle ou la SoulMap Pro ?','Il s’agit de la SoulMap personnelle : ta vie intérieure, ton identité, tes relations et ton passage actuel. La SoulMap Pro, orientée activité professionnelle, est une offre distincte.'),('En quelle langue et sous quel format ?','Cette offre à 77 USD est un livre numérique personnalisé écrit en anglais. La page française t’aide à comprendre l’offre. Le PDF peut être conservé et relu ; aucune édition imprimée n’est incluse.')]
    faqs=[(d['question'],d['answer']),(d['question2'],d['answer2'])]+extra
    body+='<section class="section"><div class="container faq"><h2 class="section-title">'+('A few useful answers.' if en else 'Quelques réponses utiles.')+'</h2>'+''.join('<details><summary>'+esc(q)+'</summary>'+paragraph(a)+'</details>' for q,a in faqs)+'</div></section>'
    body+=f'''<section class="section wine"><div class="container"><span class="eyebrow">SoulMap · 77 USD</span><h2 class="section-title">{'Give yourself space<br>to understand your story.' if en else 'T’offrir un espace<br>pour comprendre ton histoire.'}</h2>{link(service_url('soulmap',lang),d['cta'],'btn btn-light')}</div></section>'''
    write_page('soulmap',lang,d['title'],d['description'],body,data)


def soulmap_pro_feature(lang):
    en=lang=='en'
    return f'''<section class="section soulmap-pro-feature"><div class="container soulmap-feature-grid"><div>{book_visual(lang,True)}</div><div><span class="eyebrow">{'SoulMap Pro · Out of the Fog' if en else 'SoulMap Pro · Out of the Fog'}</span><h2 class="section-title">{'Your work has changed.<br>Has your place within it?' if en else 'Ton activité a évolué.<br>Et ta place à l’intérieur ?'}</h2><p class="lead">{'For women with a business or a defined professional project. A personal written reading of your professional identity, contribution, visibility and recurring business patterns, so you can see more clearly what your next chapter asks of you.' if en else 'Pour les femmes qui portent une activité ou un projet professionnel défini. Une lecture écrite de ton identité professionnelle, de ta contribution, de ta visibilité et de tes répétitions dans l’activité, pour mieux comprendre ce que le prochain chapitre te demande.'}</p>{bullet(['A personalised English PDF','Professional identity, visibility, pricing and client patterns','By email · No live call'] if en else ['Un PDF personnalisé en anglais','Identité professionnelle, visibilité, valeur et relations clientes','Par e-mail · Sans séance'])}<p class="soul-price">144 <small>USD · {'One-time payment' if en else 'Paiement unique'}</small></p>{link(path('soulmappro',lang),'Explore SoulMap Pro' if en else 'Découvrir SoulMap Pro','btn btn-wine')}</div></div></section>'''

def soulmap_pro_page(lang):
    en=lang=='en'; data=SERVICES['soulmappro']; d=data[lang]
    body=hero(lang,d['heading'],d['short'],'SoulMap Pro · Out of the Fog','services',d['facts'])
    body=body.replace('</div></section>',f'<div class="button-row">{link(service_url("soulmappro",lang),d["cta"],"btn btn-light")}{link("#inside","See what’s inside" if en else "Découvrir le contenu","btn btn-outline")}</div></div></section>',1)
    familiar=['Your expertise has grown, but your words and visibility still make it look smaller.','You keep adapting your prices, offers or boundaries to avoid disappointing people.','The same hesitation, overthinking or need for control keeps appearing in your business decisions.','The role or business model you have built no longer fits the woman and the work you are becoming.'] if en else ['Ton expertise a grandi, mais tes mots et ta visibilité la rendent encore plus petite.','Tu ajustes tes prix, tes offres ou tes limites pour éviter de décevoir.','Les mêmes hésitations, analyses ou besoins de contrôle reviennent dans tes décisions professionnelles.','Le rôle ou le modèle que tu as construit ne correspond plus à la femme et à l’activité que tu deviens.']
    themes=[('Professional identity & authority','The place you create, lead and decide from, and the role you are ready to own more fully.'),('Contribution & direction','The thread running through your expertise, the work you want to bring and the people you want to serve.'),('Visibility & expression','Where your communication feels natural, where it becomes smaller and what you struggle to show.'),('Money, pricing & value','The beliefs and patterns that appear when you set prices, receive recognition or ask to be paid.'),('Offers, clients & boundaries','How your professional identity shapes what you offer and the relationships you build with clients.'),('Your current professional transition','Recurring tensions, the role or model you have outgrown, and directions to explore in your next choices.')] if en else [('Identité professionnelle & autorité','La place depuis laquelle tu crées, diriges et décides, et le rôle que tu es prête à assumer davantage.'),('Contribution & direction','Le fil entre ton expertise, ce que tu veux apporter et les personnes que tu souhaites accompagner.'),('Visibilité & expression','Là où ta communication est naturelle, là où elle se réduit et ce que tu as du mal à montrer.'),('Argent, prix & valeur','Les croyances et répétitions qui apparaissent quand tu fixes tes prix, reçois une reconnaissance ou demandes à être payée.'),('Offres, clientes & limites','La manière dont ton identité professionnelle façonne tes offres et tes relations clientes.'),('Ton passage professionnel actuel','Les tensions récurrentes, le rôle ou le modèle devenu trop étroit et des directions à explorer dans tes prochains choix.')]
    body+=f'''<section class="section"><div class="container detail-grid"><div class="prose"><h2>{'Does your work still reflect you?' if en else 'Ton activité te reflète-t-elle encore ?'}</h2>{bullet(familiar)}<h2>{'The person behind the business.' if en else 'La femme derrière l’activité.'}</h2>{paragraph(d['body'])}{paragraph('Through mediumship and energetic reading, I look at the connection between your professional identity and what happens in your offers, communication, pricing and relationships. The aim is to make those connections easier to recognise, then give you directions and reflection prompts to explore in your actual work.' if en else 'Par ma médiumnité et ma lecture énergétique, je regarde les liens entre ton identité professionnelle et ce qui se joue dans tes offres, ta communication, tes prix et tes relations. Le but est de rendre ces liens plus reconnaissables, puis de proposer des directions et des questions à explorer dans ton activité réelle.')}</div><aside class="aside"><span class="eyebrow">SoulMap Pro · Out of the Fog</span><p class="price">144 <small>USD</small></p>{paragraph('One-time payment. A personalised English PDF, delivered by email. No appointment needed.' if en else 'Paiement unique. Un PDF personnalisé écrit en anglais, livré par e-mail. Sans rendez-vous.')}{link(service_url('soulmappro',lang),d['cta'],'btn btn-wine')}<p class="form-note">{'Delivery within 7–10 business days after your complete questionnaire is received and payment is verified.' if en else 'Livraison sous 7 à 10 jours ouvrés après réception du questionnaire complet et vérification du paiement.'}</p>{link(request_url('soulmappro',lang),'Ask about your project first' if en else 'Me parler de ton projet avant de commander')}</aside></div></section>'''
    body+='<section class="section offers-section" id="inside"><div class="container"><div class="section-head"><span class="eyebrow">'+('Inside your professional SoulMap' if en else 'Dans ta SoulMap professionnelle')+'</span><h2 class="section-title">'+('See the connections<br>behind your business patterns.' if en else 'Voir les liens<br>derrière tes répétitions professionnelles.')+'</h2><p class="lead">'+('The reading follows your real activity and its current stage. These six themes give it a structure; their depth depends on your project.' if en else 'La lecture suit ton activité réelle et son stade actuel. Ces six thèmes lui donnent une structure ; leur profondeur dépend de ton projet.')+'</p></div><div class="soul-themes">'+''.join('<article><h3>'+esc(t)+'</h3>'+paragraph(p)+'</article>' for t,p in themes)+'</div></div></section>'
    body+='<section class="section"><div class="container split"><div>'+book_visual(lang,True)+'</div><div class="prose"><h2>'+('A professional reading you can keep.' if en else 'Une lecture professionnelle à conserver.')+'</h2>'+paragraph('Your PDF brings the reading together in a coherent document, with questions and first directions to consider in your decisions, communication and boundaries. Read it, annotate it and revisit it as your work evolves.' if en else 'Ton PDF réunit la lecture dans un document cohérent, avec des questions et des premières directions à considérer dans tes décisions, ta communication et tes limites. Lis-le, annote-le et reprends-le à mesure que ton activité évolue.')+bullet(d['deliver'])+'<h2>'+('A clear scope' if en else 'Un périmètre clair')+'</h2>'+paragraph(d['fit'])+'</div></div></section>'
    body+=steps(lang,[('Order SoulMap Pro · US$144','A one-time payment through Stripe, followed by your professional questionnaire.'),('Describe your real project','Send your birth details, your activity, your existing offers, your current challenge and what you want to understand.'),('Receive your written reading','I verify payment and your information, then email your English PDF within 7–10 business days of receiving your complete answers.')] if en else [('Commander SoulMap Pro · 144 USD','Un paiement unique via Stripe, suivi du questionnaire professionnel.'),('Décrire ton projet réel','Tes informations de naissance, ton activité, tes offres existantes, ta difficulté actuelle et ce que tu veux comprendre.'),('Recevoir ta lecture écrite','Je vérifie le paiement et les informations, puis t’envoie ton PDF en anglais sous 7 à 10 jours ouvrés après réception des réponses complètes.')])
    faqs=[(d['question'],d['answer']),(d['question2'],d['answer2']),('Is a call included?' if en else 'Une séance est-elle incluse ?','No. This is the written reading only. You send your information, I prepare your personal PDF, and you receive it by email.' if en else 'Non. Cette offre comprend uniquement la lecture écrite. Tu transmets tes informations, je prépare ton PDF personnel et tu le reçois par e-mail.'),('Is this a business strategy or a revenue promise?' if en else 'Est-ce une stratégie ou une promesse de chiffre d’affaires ?',d['fit']),('What is the difference from the personal SoulMap?' if en else 'Quelle différence avec la SoulMap personnelle ?','The personal SoulMap explores your inner life, relationships and personal transition. SoulMap Pro focuses on your professional identity and its expression in your activity, offers, visibility and decisions.' if en else 'La SoulMap personnelle explore ta vie intérieure, tes relations et ton passage personnel. SoulMap Pro porte sur ton identité professionnelle et son expression dans l’activité, les offres, la visibilité et les décisions.')]
    body+='<section class="section"><div class="container faq"><h2 class="section-title">'+('Before you order.' if en else 'Avant de commander.')+'</h2>'+''.join('<details><summary>'+esc(q)+'</summary>'+paragraph(a)+'</details>' for q,a in faqs)+'</div></section>'
    body+=f'''<section class="section wine"><div class="container"><span class="eyebrow">SoulMap Pro · 144 USD</span><h2 class="section-title">{'Understand what your<br>next chapter asks of you.' if en else 'Comprendre ce que ton<br>prochain chapitre te demande.'}</h2>{link(service_url('soulmappro',lang),d['cta'],'btn btn-light')}<p class="offer-choice">{link(path('soulmap',lang),'Looking for the personal SoulMap? · US$77' if en else 'Découvrir la SoulMap personnelle · 77 USD')}</p></div></section>'''
    write_page('soulmappro',lang,d['title'],d['description'],body,data)


def service_page(key,lang):
    en=lang=='en'; data=SERVICES[key]; d=data[lang]; l=LABELS[lang]
    if key in SERVICE_CHECKOUTS:
        payment_note='Pay for this focused service through Stripe. Contact me first if you need to confirm the scope or timing.' if en else 'Règle cette prestation ciblée via Stripe. Contacte-moi avant le paiement si tu as besoin de confirmer le périmètre ou le délai.'
        payment_answer='The button opens the Stripe payment page for this service. After payment, contact me with your brief so we can confirm the practical details and next steps. If the scope or timing needs clarification, contact me before paying. Prices shown here are in US dollars.' if en else 'Le bouton ouvre la page de paiement Stripe de cette prestation. Après le paiement, contacte-moi avec les éléments de ton projet pour confirmer les détails pratiques et la suite. Si le périmètre ou le délai doit être précisé, contacte-moi avant de payer. Les tarifs affichés ici sont en dollars américains.'
    else:
        payment_note='Working online internationally, from Da Nang. We confirm your focus, the next steps and payment arrangements before beginning.' if en else 'À distance, à l’international, depuis Da Nang. Nous confirmons ton besoin, les prochaines étapes et le paiement avant de commencer.'
        payment_answer='Use the inquiry button to contact me. We confirm the focus and practical details, then I send the appropriate payment and next-step information. All prices on these pages are in US dollars.' if en else 'Le bouton de contact me permet de confirmer ton besoin et les détails pratiques. Je te transmets ensuite les informations de paiement et les prochaines étapes. Tous les tarifs de ces pages sont en dollars américains.'
    facts=d['facts'] if any('USD' in fact for fact in d['facts']) else d['facts']+[f'US${data["price"]}' if en else f'{data["price"]} USD']
    body=hero(lang,d['heading'],d['problem']+' '+d['short'],d['name'],'services',facts)
    body=body.replace('</div></section>',f'<div class="button-row">{link(service_url(key,lang),d["cta"],"btn btn-light")}</div></div></section>',1)
    body+=f'<section class="section"><div class="container detail-grid"><div class="prose"><h2>'+('Does this sound familiar?' if en else 'Est-ce que tu te reconnais ici ?')+'</h2>'+paragraph(d['intro'])+paragraph(d['audience'])+'<h2>'+('My way of working' if en else 'Ma manière de travailler')+'</h2>'+paragraph(d['body'])+f'<h2>{l["deliver"]}</h2>{bullet(d["deliver"])}<h2>{l["fit"]}</h2>{paragraph(d["fit"])}</div><aside class="aside"><span class="eyebrow">'+('Your investment' if en else 'Ton investissement')+f'</span><p class="price">{data["price"]} <small>USD</small></p>'+paragraph(payment_note)+link(service_url(key,lang),d['cta'],'btn btn-wine')+('<p class="form-note">'+link(request_url(key,lang),'A question before paying?' if en else 'Une question avant de payer ?','')+'</p>' if key in SERVICE_CHECKOUTS else '')+'</aside></div></section>'
    items=[('Send your brief','Share the text, project or website issue by email. We confirm scope, compatibility and timing in writing.'),('I prepare the work','I work on the agreed text or website correction without a live call.'),('Review your result','You receive the agreed output and send any feedback for the included correction round by email.')] if en else [('Envoyer ton brief','Transmets tes textes, ton projet ou le problème du site par e-mail. Nous confirmons le périmètre, la compatibilité et le délai par écrit.'),('Je prépare le résultat','Je réalise les textes ou la correction convenue, sans séance.'),('Relire le résultat','Tu reçois le résultat convenu et transmets tes retours de correction par e-mail.')]
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
    body+='<section class="section"><div class="container prose">'+''.join('<h2>'+esc(t)+'</h2>'+paragraph(p) for t,p in pairs)+f'<div class="button-row">{link(path("soulmap",lang),"Explore your personal SoulMap" if en else "Découvrir ta SoulMap personnelle","btn btn-wine")}</div></div></section>'
    write_page('approach',lang,title,desc,body)

def contact(lang):
    en=lang=='en'
    title='Contact & Project Inquiries' if en else 'Contact & demandes de projet'
    desc='Contact Morgane Girault about a personal SoulMap, SoulMap Pro, a written service, custom lyrics or a melody. Personalised work by email, in English and French.' if en else 'Contacte Morgane Girault pour une SoulMap, une SoulMap Pro, une prestation écrite, des paroles ou une mélodie. Travail personnalisé par e-mail, sans séance.'
    body=hero(lang,'What would you like to bring into focus?' if en else 'Qu’aimerais-tu clarifier ou faire exister ?','Tell me a little about your question or project. We will choose a useful starting point and confirm the next steps.' if en else 'Parle-moi de ta question ou de ton projet. Nous choisirons un point de départ utile et confirmerons les prochaines étapes.','Contact')
    options=[('soulmap','SoulMap · US$77'),('soulmappro','SoulMap Pro · US$144'),('bio','Bio & Offer Writing · US$111'),('booking','Booking Flow Fix · US$149'),('custom','Custom lyrics / melody · Quote'),('other','Another question')] if en else [('soulmap','SoulMap · 77 USD'),('soulmappro','SoulMap Pro · 144 USD'),('bio','Bio & présentation d’offre · 111 USD'),('booking','Parcours de réservation · 149 USD'),('custom','Paroles / mélodie · Sur devis'),('other','Une autre question')]
    wmsg='Hello Morgane, I would like to discuss a service or a music commission.' if en else 'Bonjour Morgane, j’aimerais parler d’une prestation ou d’une création musicale.'
    form=f'<form class="inquiry-form" id="inquiry-form" action="mailto:{EMAIL}" method="get"><div class="field"><label for="name">'+('Your name' if en else 'Ton prénom')+'</label><input id="name" name="name" autocomplete="name" maxlength="100" required></div><div class="field"><label for="email">'+('Your email' if en else 'Ton e-mail')+'</label><input id="email" name="email" type="email" autocomplete="email" maxlength="200" required></div><div class="field"><label for="service">'+('What brings you here?' if en else 'Qu’est-ce qui t’amène ?')+'</label><select id="service" name="service">'+''.join(f'<option value="{v}">{esc(t)}</option>' for v,t in options)+'</select></div><div class="field"><label for="message">'+('Your question or project' if en else 'Ta question ou ton projet')+'</label><textarea id="message" name="message" maxlength="4000" required></textarea></div><p class="form-note">'+('This form prepares a draft in your email app. You review and send it yourself. Please share only the information needed to understand your request.' if en else 'Ce formulaire prépare un brouillon dans ton application e-mail. Tu le relis et l’envoies toi-même. Partage uniquement les informations utiles pour comprendre ta demande.')+'</p><button class="btn btn-wine" type="submit">'+('Open my email draft' if en else 'Préparer mon e-mail')+'</button><p class="status" id="form-status" role="status" aria-live="polite"></p></form>'
    body+='<section class="section"><div class="container split top"><div><h2 class="section-title">'+('Let’s start with your written brief.' if en else 'Commencer par ton brief écrit.')+'</h2><p class="lead">'+('For the digital services, I confirm the scope and compatibility before payment. For a music commission, we agree on the format, price and intended use in a personal quote.' if en else 'Pour les interventions digitales, je confirme le périmètre et la compatibilité avant paiement. Pour une création musicale, nous définissons le format, le tarif et l’usage prévu dans un devis.')+'</p><div class="contact-list">'+link(WHATSAPP+'?text='+quote(wmsg),'Talk on WhatsApp' if en else 'Échanger sur WhatsApp','btn btn-dark',True)+link('mailto:'+EMAIL,EMAIL)+f'</div><p class="form-note">{LABELS[lang]["based"]}</p></div>{form}</div></section>'
    write_page('contact',lang,title,desc,body)

def soulmap_intake(lang,pro=False):
    en=lang=='en'; key='soulmappro' if pro else 'soulmap'; name='SoulMap Pro' if pro else 'SoulMap'
    slug='soulmap-pro' if pro else 'soulmap'; rel=f'post-achats/{slug}'+('' if en else '-fr')+'.html'
    other=f'/post-achats/{slug}'+('-fr' if en else '')+'.html'
    title=f'{name} · '+('Your questionnaire' if en else 'Ton questionnaire')
    head=metadata(key,lang,title,'Send the information for your personalised English soul book.' if en else 'Transmettre les informations pour ton livre personnalisé en anglais.')
    head=re.sub(r'<meta name="robots"[^>]*>','<meta name="robots" content="noindex,nofollow">',head)
    head=re.sub(r'<link rel="(?:canonical|alternate)"[^>]*>','',head)
    head+=f'<link rel="canonical" href="{DOMAIN}/{rel}">'
    intro=('After checkout, complete this questionnaire and send it by email. I verify your payment and review your answers before creating your book.' if en else 'Après le paiement, complète ce questionnaire et envoie-le par e-mail. Je vérifie ton paiement et tes réponses avant de créer ton livre.')
    body=hero(lang,'The information for your '+name+'.' if en else 'Les informations pour ta '+name+'.',intro,name)
    def field(field_id,label,kind='text',required=True,autocomplete='',note='',limit=160):
        return f'<div class="field"><label for="{field_id}">{esc(label)}</label><input id="{field_id}" name="{field_id}" type="{kind}"'+(' required' if required else '')+(f' autocomplete="{autocomplete}"' if autocomplete else '')+f' maxlength="{limit}">'+(f'<p class="form-note">{esc(note)}</p>' if note else '')+'</div>'
    fields=field('first_names','All your first names' if en else 'Tous tes prénoms',autocomplete='given-name')+field('surname','Your surname' if en else 'Ton nom de famille',autocomplete='family-name')+field('checkout_email','Email used at checkout' if en else 'E-mail utilisé au paiement','email',autocomplete='email',limit=200)+field('birth_date','Your date of birth' if en else 'Ta date de naissance','date')
    fields+=field('birth_time','Exact time of birth, if known' if en else 'Heure exacte de naissance, si connue','time',note='Use the local time recorded at your birthplace.' if en else 'Indique l’heure locale enregistrée au lieu de naissance.')
    fields+='<div class="field checkbox-field"><label><input type="checkbox" id="birth_time_unknown" name="birth_time_unknown"> '+('I do not know my birth time' if en else 'Je ne connais pas mon heure de naissance')+'</label></div>'
    fields+=field('birth_city','City of birth' if en else 'Ville de naissance',autocomplete='off')+field('birth_country','Country of birth' if en else 'Pays de naissance',autocomplete='off')
    def answer(field_id,label,limit):
        return f'<div class="field"><label for="{field_id}">{esc(label)}</label><textarea id="{field_id}" name="{field_id}" maxlength="{limit}" required></textarea></div>'
    fields+=answer('current_context','What is happening in your work or professional project now?' if pro and en else 'Que se passe-t-il dans ton activité ou ton projet professionnel ?' if pro else 'What are you living through at the moment?' if en else 'Que traverses-tu en ce moment ?',1200)
    if pro:
        fields+=answer('professional_context','Describe your activity, your offers and the people you work with.' if en else 'Décris ton activité, tes offres et les personnes avec lesquelles tu travailles.',1200)
    fields+=answer('main_question','Which question or repeating pattern would you like to understand?' if en else 'Quelle question ou répétition souhaites-tu comprendre ?',800)
    delay='7–10' if pro else '7'
    form=f'''<form class="inquiry-form" id="soulmap-form" data-offer="{name}" action="mailto:{EMAIL}" method="get"><h2>{'Your questionnaire' if en else 'Ton questionnaire'}</h2>{fields}<p class="form-note">{'This form prepares an email draft. Your answers stay on this page until you choose to email them; they are not submitted automatically. Share only information useful for your reading.' if en else 'Ce formulaire prépare un brouillon d’e-mail. Tes réponses restent sur cette page jusqu’à ce que tu choisisses de les envoyer ; rien n’est transmis automatiquement. Partage uniquement les éléments utiles à ta lecture.'}</p><button class="btn btn-wine" type="submit">{'Prepare my email' if en else 'Préparer mon e-mail'}</button><div class="draft-preview" id="soulmap-draft" hidden><h3>{'Review your answers, then send them.' if en else 'Relis tes réponses, puis envoie-les.'}</h3><label class="sr-only" for="soulmap-email-preview">{'Your email text' if en else 'Le texte de ton e-mail'}</label><textarea id="soulmap-email-preview" readonly></textarea><div class="button-row"><a class="btn btn-dark" id="soulmap-email-link" href="mailto:{EMAIL}">{'Open my email draft' if en else 'Ouvrir mon brouillon d’e-mail'}</a><button class="btn btn-outline" id="copy-soulmap-draft" type="button">{'Copy my answers' if en else 'Copier mes réponses'}</button></div><p class="form-note">{'Remember to send the email. If your email app does not open, copy your answers and email them to ' if en else 'Pense à envoyer l’e-mail. Si ton application ne s’ouvre pas, copie les réponses et envoie-les à '}{link('mailto:'+EMAIL,EMAIL,'')}.</p></div><p class="status" id="soulmap-status" role="status" aria-live="polite"></p></form>'''
    body+=f'''<section class="section"><div class="container detail-grid"><div class="prose"><h2>{'A book prepared from your information.' if en else 'Un livre préparé à partir de tes informations.'}</h2>{paragraph('Please use the email address from your Stripe checkout so I can match your answers with your order. If your birth time is unknown, indicate it; I will let you know if anything else is needed.' if en else 'Utilise l’adresse e-mail de ton paiement Stripe pour que je puisse relier tes réponses à ta commande. Si l’heure de naissance est inconnue, indique-le ; je te dirai si un complément est nécessaire.')}<h2>{'What happens next?' if en else 'Et ensuite ?'}</h2>{paragraph(f'Once I have verified payment and received all the information needed, I prepare your English PDF and email it within {delay} business days. This page does not confirm a payment by itself; I check your order in Stripe.' if en else f'Après vérification du paiement et réception des informations nécessaires, je prépare ton PDF en anglais et te l’envoie sous {delay} jours ouvrés. Cette page ne confirme pas un paiement à elle seule : je vérifie ta commande dans Stripe.')}<p class="form-note">{link('/privacy-policy.html' if en else '/legal/confidentialite-cookies.html','How your information is handled' if en else 'Comment tes informations sont utilisées')}</p><noscript><p>{'JavaScript is disabled. Email me your full name, checkout email, birth date, time if known, city and country of birth, and your current situation and main question.' if en else 'JavaScript est désactivé. Envoie-moi ton identité, l’e-mail du paiement, la date, l’heure si connue, la ville et le pays de naissance, ta situation et ta question principale.'} {link('mailto:'+EMAIL,EMAIL)}</p></noscript></div>{form}</div></section>'''
    nav=header(key,lang).replace(f'href="{path(key,"fr" if en else "en")}" lang=',f'href="{other}" lang=')
    f=PUBLIC/rel;f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(f'<!doctype html><html lang="{lang}"><head>{head}</head><body>{nav}<main id="main">{body}</main>{footer(lang)}</body></html>'.replace('><','>\n<')+'\n')

def archive_session_pages():
    redirects={'/en/intuitive-career-business-clarity.html':path('soulmappro','en'),'/fr/clarte-professionnelle-intuitive.html':path('soulmappro','fr'),'/en/practical-ai-session.html':path('services','en'),'/fr/ia-pratique-activite.html':path('services','fr')}
    for source,dest in redirects.items():
        lang='fr' if source.startswith('/fr/') else 'en'
        (PUBLIC/source.lstrip('/')).write_text(f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><meta http-equiv="refresh" content="0;url={dest}"><link rel="canonical" href="{DOMAIN+dest}"><title>Page moved | Morgane Girault</title></head><body><main><h1>{"Cette page a changé." if lang=="fr" else "This page has moved."}</h1><a href="{dest}">{"Continuer" if lang=="fr" else "Continue"}</a></main></body></html>\n')


def adapt_legal():
    pairs=[('legal-notice.html','legal/mentions-legales.html'),('privacy-policy.html','legal/confidentialite-cookies.html')]
    for eng,fra in pairs:
        for rel,lang,other in [(eng,'en',fra),(fra,'fr',eng)]:
            f=PUBLIC/rel; text=(ROOT/'scripts/legacy'/Path(rel).name).read_text().replace('https://morgane-girault.com','https://www.morgane-girault.com')
            text=re.sub(r'<link\b[^>]*\brel=["\'](?:canonical|alternate)["\'][^>]*>','',text,flags=re.I)
            text=text.replace('</head>',f'<link rel="canonical" href="{DOMAIN}/{rel}"><link rel="alternate" hreflang="en" href="{DOMAIN}/{eng}"><link rel="alternate" hreflang="fr" href="{DOMAIN}/{fra}"><link rel="alternate" hreflang="x-default" href="{DOMAIN}/{eng}"></head>')
            text=re.sub(r'href=["\'](?:index\.html|/)["\']',f'href="{path("home",lang)}"',text)
            text=re.sub(r'href=["\'](?:contact\.html|contact-en\.html|/contact|/commencer)["\']',f'href="{path("contact",lang)}"',text)
            other_lang='fr' if lang=='en' else 'en'
            nav=''.join(link(path(key,lang),LABELS[lang][key],'') for key in ['home','soulmap','services','music','support','about','contact'])
            nav+=f'<a href="/{other}" lang="{other_lang}" hreflang="{other_lang}">{other_lang.upper()}</a>'
            text=re.sub(r'(<nav\b[^>]*(?:class="(?:nav-links|desktop-nav)"|aria-label="Navigation mobile")[^>]*>).*?</nav>',lambda m:m.group(1)+nav+'</nav>',text,flags=re.S)
            for old,key in {'/seance-passage':'soulmap','/architecture-de-l-incarnation':'approach','/a-propos':'about'}.items():
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
    source=(ROOT/'scripts/legacy/architecture-source.html').read_text().replace('https://morgane-girault.com','https://www.morgane-girault.com')
    source=re.sub(r'<title>.*?</title>','<title>Architecture de l’Incarnation | Morgane Girault</title>',source,flags=re.S)
    source=re.sub(r'<link\b[^>]*\brel=["\'](?:canonical|alternate)["\'][^>]*>','',source,flags=re.I)
    source=source.replace('</head>',f'<link rel="canonical" href="{DOMAIN+path("approach","fr")}"><link rel="alternate" hreflang="fr" href="{DOMAIN+path("approach","fr")}"><link rel="alternate" hreflang="en" href="{DOMAIN+path("approach","en")}"><link rel="alternate" hreflang="x-default" href="{DOMAIN+path("approach","en")}"><style>.updated-footer{{padding:45px 0;background:#110d0e;color:#fffdf9}}.updated-footer a{{display:inline-block;margin:8px 18px 8px 0;color:#f5efe8}}.header-actions .language-switch{{font-weight:700;padding:10px}}</style></head>')
    source=source.replace('<main>','<main id="main">')
    source=re.sub(r'(<h1 id="hero-title">).*?(</h1>)',r'\1L’Architecture de l’Incarnation\2',source,flags=re.S)
    navigation=''.join(link(path(k,'fr'),LABELS['fr'][k],'') for k in ['home','soulmap','services','music','support','about','contact'])
    source=re.sub(r'(<nav class="desktop-nav"[^>]*>).*?(</nav>)',lambda m:m[1]+navigation+m[2],source,flags=re.S)
    source=re.sub(r'(<div class="mobile-menu"[^>]*>\s*<nav[^>]*>).*?(</nav>)',lambda m:m[1]+navigation+link(path('approach','en'),'EN','')+m[2],source,flags=re.S)
    source=source.replace('<div class="header-actions">',f'<div class="header-actions"><a class="language-switch" href="{path("approach","en")}" lang="en">EN</a>')
    mappings={'/':path('home','fr'),'/commencer':path('services','fr'),'/seance-passage':path('soulmap','fr'),'/architecture-de-l-incarnation':path('approach','fr'),'/a-propos':path('about','fr'),'/soulmap':path('soulmap','fr'),'/accompagnements':path('services','fr'),'/chroniques':path('approach','fr'),'/recherches':path('approach','fr'),'/institut':path('approach','fr'),'/temoignages':path('services','fr'),'/contact':path('contact','fr')}
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
      '/soulmap':path('soulmap','en'), '/soulmap.html':path('soulmap','en'), '/soulmap-pro':path('soulmappro','en'), '/soulmap-pro.html':path('soulmappro','en'),
      '/en/intuitive-career-business-clarity.html':path('soulmappro','en'), '/fr/clarte-professionnelle-intuitive.html':path('soulmappro','fr'),
      '/en/practical-ai-session.html':path('services','en'), '/fr/ia-pratique-activite.html':path('services','fr'),
      '/identity-clarity-audit.html':path('soulmappro','en'), '/mentorship.html':path('services','en'),
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
        soulmap_page(lang); soulmap_pro_page(lang); soulmap_intake(lang); soulmap_intake(lang,True)
        for key in ['bio','booking']: service_page(key,lang)
    preserve_architecture(); adapt_legal(); archive_session_pages(); configuration(); install_analytics()
    print(f'Built {sum(len(routes) for routes in ROUTES.values())} bilingual public pages, SEO metadata, sitemap and Vercel configuration.')

if __name__=='__main__': build()
