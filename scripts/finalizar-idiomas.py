from pathlib import Path
from bs4 import BeautifulSoup
r=Path(__file__).resolve().parents[1]
for lang in ['pt','en','es']:
 folder=r if lang=='pt' else r/lang
 for filename in ['curso.html','landing.html']:
  p=folder/filename;soup=BeautifulSoup(p.read_text(),'html.parser')
  for a in soup.select('a[href^="guia/index.html"]'):
   a['href']=('guia/index.html' if lang=='pt' else '../guia/'+lang+'/index.html')+('#prompts' if '#prompts' in a['href'] else '')
  nav=soup.select_one('nav.langs')
  if nav:nav['aria-label']='Language' if lang=='en' else 'Idioma'
  if filename=='curso.html' and not soup.select_one('script[data-course-languages]'):
   sc=soup.new_tag('script',src=('assets/' if lang=='pt' else '../assets/')+'idiomas.js');sc['data-course-languages']='';soup.body.append(sc)
  p.write_text(str(soup))
 guide=r/'guia'/('index.html' if lang=='pt' else lang+'/index.html');soup=BeautifulSoup(guide.read_text(),'html.parser')
 if not soup.select_one('#course-link'):
  a=soup.new_tag('a',href='../landing.html' if lang=='pt' else '../../'+lang+'/landing.html');a['class']='btn ghost';a['id']='course-link';a.string={'pt':'Fazer o curso v6','en':'Take the v6 course','es':'Hacer el curso v6'}[lang];soup.select_one('.cta').append(a)
 for node in soup.find_all(string=lambda t:t and 'v1.0.0' in t):node.replace_with(node.replace('v1.0.0','v1.1.0'))
 guide.write_text(str(soup))
 readme=r/('README.md' if lang=='pt' else 'README.'+lang+'.md');txt=readme.read_text();title={'pt':'Curso v6','en':'v6 course','es':'Curso v6'}[lang];link='https://linnoff88-dev.github.io/arckhe-/'+('' if lang=='pt' else lang+'/')+'landing.html'
 if '## '+title not in txt:txt+='\n## '+title+'\n\n['+title+']('+link+') · 4 '+({'pt':'aulas práticas','en':'practical lessons','es':'clases prácticas'}[lang])+'.\n'
 txt=txt.replace('1.0.0','1.1.0');readme.write_text(txt)
print('Links curso↔guia, seletor interno e READMEs atualizados nos3idiomas.')

# Ficha definitiva do portal; reaplicável após reconstruçêo das páginas.
import re
portal='https://www.ARCKHÉ AI/cursos/319-motion-echo-v6-retratos-com-eco-de-movimento/'
for lang,label,heading in [('pt','Ver a ficha no ARCKHÉ AI','Mais no ARCKHÉ AI'),('en','View this course on ARCKHÉ AI','More on ARCKHÉ AI'),('es','Ver el curso en ARCKHÉ AI','Más en ARCKHÉ AI')]:
 p=r/('landing.html' if lang=='pt' else lang+'/landing.html')
 block='<!-- ARCKHÉ-backlink:v1 --><p style="margin:.5rem 0 0"><a href="'+portal+'">'+label+'</a></p><!-- /ARCKHÉ-backlink:v1 -->'
 p.write_text(re.sub(r'<!-- ARCKHÉ-backlink:v1.*?<!-- /ARCKHÉ-backlink:v1 -->',lambda m:block,p.read_text(),flags=re.S))
 p=r/('README.md' if lang=='pt' else 'README.'+lang+'.md')
 if portal not in p.read_text():p.write_text(p.read_text()+'\n## '+heading+'\n\n['+label+']('+portal+')\n')
