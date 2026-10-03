"""Check links, language pairs, structured data, prices and SEO output."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import json
from xml.etree import ElementTree as ET
from build_site import ROUTES, DOMAIN, SERVICES

PUBLIC=Path(__file__).resolve().parents[1]/'public'
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=True)
        self.links=[];self.ids=set();self.lang=None;self.h1=0;self.canonical=[];self.alternates={};self.scripts=[];self.current_script=None;self.text=[]
        self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html':self.lang=a.get('lang')
        if tag=='h1':self.h1+=1
        if a.get('id'):self.ids.add(a['id'])
        if tag=='a':self.links.append(a.get('href',''))
        if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href'))
        if tag=='link' and a.get('rel')=='alternate':self.alternates[a.get('hreflang')]=a.get('href')
        if tag=='script' and a.get('type')=='application/ld+json':self.current_script=''
    def handle_endtag(self,tag):
        if tag=='script' and self.current_script is not None:self.scripts.append(json.loads(self.current_script));self.current_script=None
    def handle_data(self,data):
        if self.current_script is not None:self.current_script+=data
        self.text.append(data)

redirects={x['source']:x['destination'] for x in json.loads((PUBLIC.parent/'vercel.json').read_text())['redirects']}
def resolve(url):
    p=urlparse(url);target=p.path
    for _ in range(5):
        if target not in redirects:break
        target=redirects[target]
    f=PUBLIC/target.lstrip('/')
    if f.is_dir():f=f/'index.html'
    return f,p.fragment

pages={}
for key,pair in ROUTES.items():
    for lang,url in pair.items():
        f,_=resolve(url);assert f.exists() and f.read_text().strip(),f'Missing page: {url}'
        p=Page(f.read_text());pages[url]=p
        assert p.lang==lang,(url,'wrong language')
        assert p.h1==1,(url,'one primary heading required',p.h1)
        assert p.canonical==[DOMAIN+url],(url,'canonical',p.canonical)
        assert p.alternates=={'en':DOMAIN+pair['en'],'fr':DOMAIN+pair['fr'],'x-default':DOMAIN+pair['en']},(url,'language alternatives',p.alternates)
        assert p.scripts,(url,'structured data missing')
        for href in p.links:
            assert href and href!='link' and not href.startswith('javascript:'),(url,'placeholder',href)
            if href.startswith(('https:','http:','mailto:','tel:')):continue
            target,fragment=resolve(href if href.startswith('/') else str(Path(url).parent/ href))
            assert target.exists() and target.read_text().strip(),(url,'broken link',href)
            if fragment:assert fragment in Page(target.read_text()).ids,(url,'missing anchor',href)
        if key in SERVICES:
            offers=[n['offers'] for s in p.scripts for n in s.get('@graph',[]) if n.get('@type')=='Service']
            assert len(offers)==1 and offers[0]['price']==str(SERVICES[key]['price']) and offers[0]['priceCurrency']=='USD',(url,'incorrect price')
        assert not any(w in f.read_text().lower() for w in ['live & booking','event name','00.00','action="link"']),(url,'old stage or placeholder content')

for source,dest in redirects.items():
    target,_=resolve(dest);assert target.exists() and target.read_text().strip(),('bad redirect',source,dest)
    assert source!=dest,('redirect loop',source)
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
locs=[x.text for x in ET.parse(PUBLIC/'sitemap.xml').findall('s:url/s:loc',ns)]
assert set(locs)=={DOMAIN+u for pair in ROUTES.values() for u in pair.values()}
assert DOMAIN+'/sitemap.xml' in (PUBLIC/'robots.txt').read_text()
for f in (PUBLIC/'post-achats').glob('*.html'):
    if f.read_text().strip():assert 'content="noindex,nofollow"' in f.read_text(),f
print(f'PASS: {len(pages)} pages; local links and anchors; reciprocal EN/FR; prices; structured data; {len(redirects)} redirects; sitemap; post-purchase noindex.')
