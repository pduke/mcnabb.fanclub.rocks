#!/usr/bin/env python3
"""One-time/import-on-demand conversion from approved V10 HTML to editable Typst.
The generated chapter files become the publishing master. Don't rerun over manual edits.
"""
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
import subprocess, re, html, qrcode
from urllib.parse import unquote
P=Path(__file__).resolve().parent; SITE=P/'source'; CH=P/'chapters';CH.mkdir(exist_ok=True)
ORDER=[('01-family-tree','McNabb Family Tree','mchtml/McNabb Tree.html'),('02-james','James Pinckney McNabb','mchtml/James Pinckney McNabb.html'),('03-walter','Walter Scott McNabb','mchtml/Walter Scott McNabb.html'),('04-warren-gilbert','Warren Gilbert McNabb','mchtml/Warren Gilbert McNabb.html'),('05-ruth','Ruth Pauline Prutsman','mchtml/Ruth Pauline Prutsman.html'),('06-warren-neil','Warren Neil McNabb','mchtml/Warren Neil McNabb.html'),('07-beverly-nan','Beverly Nan McNabb','mchtml/Beverly Nan McNabb.html'),('08-craig','Walter Craig Davidson’s Research','research.html')]
for tag,url in [('nan','https://pduke.github.io/mcnabb.fanclub.rocks/mcdata/Memories%20of%20Beverly%20Nan%20Orr.pdf'),('ocr','https://pduke.github.io/mcnabb.fanclub.rocks/mchtml/ocr_text.html'),('neeve','https://www.facebook.com/neeve.Valenzuela')]:
 p=P/'qr_images';p.mkdir(exist_ok=True)
 q=qrcode.QRCode(border=4,box_size=8,error_correction=qrcode.constants.ERROR_CORRECT_M);q.add_data(url);q.make(fit=True);q.make_image().save(p/f'{tag}.png')

def preprocess(path,key):
 s=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser');root=s.body or s
 for elem in list(root.select('script, style, nav, #site-nav, .site-nav, button, audio, source, iframe, input, form')):elem.decompose()
 for elem in root.select('details'):elem.attrs.pop('open',None);elem.name='div'
 for elem in root.select('summary'):elem.name='p'
 # Strip legacy styles that add unwanted page breaks, but preserve structural text.
 for elem in root.find_all(True):
  for attr in ['style','onclick','onload','id','class','width','height','align','border','valign','cellpadding','cellspacing']:
   elem.attrs.pop(attr,None)
  if elem.name=='center':elem.name='div'
  if elem.name=='font':elem.name='span'
  if elem.name=='br':continue
 for img in root.select('img[src]'):
  src=img['src'];target=(path.parent/src).resolve()
  if target.exists():img['src']=(target.relative_to(P)).as_posix()
  else:img.decompose()
 # Avoid duplicating the HTML QR, which is separately placed in Typst.
 for img in list(root.select('img[src]')):
  if 'qr' in img['src'].lower():
   if img.parent.name=='a':img.parent.decompose()
   else:img.decompose()
 for a in root.select('a[href]'):
  href=a['href']
  if href.startswith('#'):continue
  if href.startswith('http'):continue
  target=(path.parent/href).resolve()
  try:a['href']='https://pduke.github.io/mcnabb.fanclub.rocks/'+target.relative_to(SITE).as_posix().replace(' ','%20')
  except ValueError: pass
 for el in root.select('table'):
  # Pandoc can convert tables, but the complex HTML family tree needs gentle rendering.
  el.attrs.pop('style',None)
 # Remove original QR captions; these get standardized below.
 if key=='07-beverly-nan':
  for a in list(root.find_all('a',href=lambda x:x and 'Memories%20of%20Beverly%20Nan%20Orr.pdf' in x)):
   if a.parent.name in ['p','div'] and len(a.parent.get_text(' ',strip=True))<150:a.parent.decompose()
 if key=='08-craig':
  for f in list(root.find_all('figure')):
   if 'Scan to contact Neeve' in f.get_text(' ',strip=True):f.decompose()
 # Original image width conventions will be adjusted in editable Typst files.
 return '<!doctype html><html><head><meta charset="utf-8"></head><body>'+root.decode_contents()+'</body></html>'

def typst_escape_string(s):return s.replace('\\','\\\\').replace('"','\\"')
for key,title,filename in ORDER:
 path=SITE/filename
 markup=preprocess(path,key)
 temp=P/'_temp.html';temp.write_text(markup,encoding='utf-8')
 cmd=['pandoc',str(temp),'-f','html','-t','typst','--wrap=none']
 proc=subprocess.run(cmd,text=True,capture_output=True)
 if proc.returncode:raise RuntimeError(proc.stderr)
 content=proc.stdout
 # Pandoc's paths refer to project root; chapters are one level deep.
 content=re.sub(r'"source/(.*?)"',lambda m:'"../source/'+unquote(m.group(1))+'"',content)
 # Images can overflow: cap with a shared helper, not fixed coordinates.
 content=re.sub(r'#image\(("[^"\n]+")\)',r'#chapter-image(\1)',content)
 # Ensure no spurious old QR image.
 extra=''
 if key=='07-beverly-nan':extra='\n#qr-link("nan", "Memories of Beverly Nan Orr", "https://pduke.github.io/mcnabb.fanclub.rocks/mcdata/Memories%20of%20Beverly%20Nan%20Orr.pdf")\n'
 if key=='08-craig':
  extra='\n#qr-link("ocr", "Search Craig’s Original Research", "https://pduke.github.io/mcnabb.fanclub.rocks/mchtml/ocr_text.html")\n\n#qr-link("neeve", "Contact Neeve McNabb on Facebook", "https://www.facebook.com/neeve.Valenzuela")\n'
 header=f'// {title}\n// EDIT THIS FILE to refine layout. Do not rerun make_typst.py over your edits.\n'
 title_esc=typst_escape_string(title)
 if key=='08-craig':
  # Position the OCR code immediately after its link, rather than after the contact section.
  needle='#link("https://pduke.github.io/mcnabb.fanclub.rocks/mchtml/ocr_text.html")[Search the 277 scanned pages]'
  call='#qr-link("ocr", "Search Craig’s Original Research", "https://pduke.github.io/mcnabb.fanclub.rocks/mchtml/ocr_text.html")'
  if needle in content:
   content=content.replace(needle, needle+'\n\n'+call)
   extra=extra.replace('\n'+call, '',1)
 result=header+f'#chapter-title("{title_esc}")\n\n'+content+extra
 (CH/(key+'.typ')).write_text(result,encoding='utf-8')
 print(key,len(result), 'chars')
(P/'_temp.html').unlink(missing_ok=True)
