#!/usr/bin/env python3
# Creative DARK re-theme: keep the dark site + ALL content/images/videos,
# swap gold/sage -> red/orange cinematic accents, Wix Madefor/IBM Plex -> Space Grotesk,
# add Anton big section numbers + hero glow. Nothing removed.
import re, sys, pathlib

def main(src, out):
    t = pathlib.Path(src).read_text(errors='replace')

    # 0. CONTENT EDITS (run before colour map; originals carry original hexes)
    content = {
        # swap SalesShortcut 2nd motion video (ss-mo2-video)
        'https://vimeo.com/1214491534?fl=tl&fe=ec':'https://vimeo.com/1223253611?fl=ip&fe=ec',
        # hero stats -> percentage-only (and unify colour to the gold token)
        'color:#E8D5A3;">932</div><div style="font-size:13px; color:#8C8A85; margin-top:4px;">Instagram reach · +396%</div>':
          'color:#E8D5A3;">+396%</div><div style="font-size:13px; color:#8C8A85; margin-top:4px;">Instagram reach, 30 days</div>',
        'color:#9DB89A;">2.8K</div><div style="font-size:13px; color:#8C8A85; margin-top:4px;">Content views · +298%</div>':
          'color:#E8D5A3;">+298%</div><div style="font-size:13px; color:#8C8A85; margin-top:4px;">Content views, 30 days</div>',
        'color:#9DB89A;">205</div><div style="font-size:13px; color:#8C8A85; margin-top:4px;">Content interactions · +181%</div>':
          'color:#E8D5A3;">+181%</div><div style="font-size:13px; color:#8C8A85; margin-top:4px;">Content interactions, 30 days</div>',
    }
    for k,v in content.items():
        if k in t: t = t.replace(k, v)
        else: print("WARN content edit not found:", k[:60])

    # 0b. MOVE the portrait out of the hero into the About (#story) section
    marker = '<div style="position:relative; display:flex; justify-content:center;">'
    ps = t.find('data-slot="profile-photo"')
    start = t.rfind(marker, 0, ps)
    if start != -1:
        # balanced <div> match
        i = start; depth = 0
        while i < len(t):
            nd = t.find('<div', i); nc = t.find('</div>', i)
            if nc == -1: break
            if nd != -1 and nd < nc:
                depth += 1; i = nd + 4
            else:
                depth -= 1; i = nc + 6
                if depth == 0: break
        block = t[start:i]
        newblock = block.replace(marker, '<div class="soyli-portrait" style="position:relative; display:flex; justify-content:center;">', 1)
        t = t[:start] + t[i:]                      # remove from hero
        si = t.find('<section id="story"')
        ins = t.find('>', si) + 1                   # just inside the <section> opening
        portrait_html = '\n' + newblock + '\n<div class="story-body">\n'
        t = t[:ins] + portrait_html + t[ins:]
        # close the story-body wrapper right before #story's </section>
        sc = t.find('</section>', ins + len(portrait_html))
        t = t[:sc] + '</div>\n' + t[sc:]
        print("portrait moved + story-body wrapped")
    else:
        print("WARN portrait marker not found")

    # 1. FONTS: neutralize embedded, point usages to Space Grotesk
    def neut(m): return m.group(0).replace("Wix Madefor Display","__embWix").replace("IBM Plex Sans","__embPlex")
    t = re.sub(r'@font-face\s*\{[^}]*\}', neut, t)
    t = t.replace("Wix Madefor Display","Space Grotesk").replace("IBM Plex Sans","Space Grotesk")

    # 2. PALETTE
    def hexrepl(text, mp):
        pat = re.compile('|'.join(re.escape(k) for k in mp), re.I)
        return pat.sub(lambda m: mp[m.group(0).lower()], text)

    accents = {
        '#e8d5a3':'#FF8A3C','#f4e9c8':'#FFB079','#e0cfa6':'#FF8A3C','#e3d2ac':'#FF8A3C',
        '#f2e7c6':'#FF8A3C','#9db89a':'#E8663C','#c14b3c':'#FF5A2C','#8a6a1f':'#B5591F','#8a7347':'#9E6B45',
    }
    warm_bg = {
        '#0e0e10':'#0F0B0B','#121215':'#0F0B0B','#111114':'#160F0E','#0b0b0d':'#0C0808',
        '#131315':'#140E0D','#141416':'#140E0D','#151518':'#17100F','#17171a':'#181010',
        '#17151a':'#181010','#1b1b1f':'#1C1413','#1c1b1e':'#1C1413','#1c2418':'#1A1510','#26301f':'#241A14',
    }
    light_keep = {  # stay light on dark, just warm
        '#f2eee6':'#F4ECE3','#f6f2ea':'#F7F0E8','#b8b5ae':'#B9A99F','#c9c6bf':'#CBBBB0',
        '#d8d5cd':'#DAC9BE','#9a9791':'#9B8B82','#8c8a85':'#8D7D74','#6e6c68':'#6E5F58',
    }
    for mp in (accents, warm_bg, light_keep):
        t = hexrepl(t, mp)

    rgba = {
        'rgba(232,213,163,.4)':'rgba(255,138,60,.45)','rgba(232,213,163,.35)':'rgba(255,138,60,.4)',
        'rgba(232,213,163,.3)':'rgba(255,138,60,.35)','rgba(232,213,163,.22)':'rgba(255,138,60,.28)',
        'rgba(232,213,163,.25)':'rgba(255,138,60,.3)','rgba(232,213,163,.92)':'rgba(255,122,42,.95)',
        'rgba(157,184,154,.4)':'rgba(232,102,60,.42)',
    }
    for k,v in rgba.items(): t = t.replace(k,v)

    # 2b. Darken the one light section (#certs) to match the dark theme
    i = t.find('<section id="certs"'); j = t.find('<section id="award"')
    if i != -1 and j != -1:
        blk = t[i:j]
        certs_local = {
            '#EDE3CC':'#160F0E','#E4D6B6':'#0F0B0B',   # light bg -> dark
            '#16130C':'#F4ECE3',                        # heading -> light
            '#57503F':'#B9A99F',                        # body -> light grey
            '#3E3626':'#8D7D74',                        # chips/borders -> readable
            '#9E6B45':'#FF8A3C',                        # eyebrow + rule (was #8A7347) -> orange
        }
        blk = re.compile('|'.join(re.escape(k) for k in certs_local), re.I).sub(
            lambda m: certs_local[m.group(0).upper()], blk)
        t = t[:i] + blk + t[j:]

    # 3. Google fonts
    link = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Anton&family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">')
    t = t.replace('<head>', '<head>\n'+link, 1)

    # 4. creative polish
    polish = '''
<style id="soyli-creative">
:root{--cr-or:#FF8A3C;--cr-rd:#FF5A2C;}
section img, section video, section iframe{border-radius:16px;}
::selection{background:#FF5A2C;color:#0F0B0B;}
/* ===== ANIMATED cinematic gradient + CENTERED creative hero ===== */
#hero{position:relative;overflow:hidden;
  grid-template-columns:1fr !important;justify-items:center;text-align:center;
  min-height:auto !important;padding:140px 24px 80px !important;}
#hero::after{content:"";position:absolute;inset:-25% -15%;z-index:0;pointer-events:none;
  background:
   radial-gradient(42% 42% at 72% 26%,rgba(255,106,30,.40),transparent 62%),
   radial-gradient(38% 38% at 30% 72%,rgba(226,58,30,.34),transparent 64%),
   radial-gradient(34% 34% at 52% 48%,rgba(255,170,60,.18),transparent 66%);
  filter:blur(26px);animation:heroGlow 16s ease-in-out infinite;}
#hero::before{content:"";position:absolute;inset:0;z-index:0;pointer-events:none;opacity:.7;
  background:conic-gradient(from 120deg at 60% 40%,rgba(255,90,44,.10),transparent 25%,rgba(255,138,60,.10) 55%,transparent 80%);
  animation:heroSpin 26s linear infinite;}
@keyframes heroGlow{
  0%{transform:translate(0,0) scale(1);}
  33%{transform:translate(-5%,4%) scale(1.14);}
  66%{transform:translate(4%,-3%) scale(1.06);}
  100%{transform:translate(0,0) scale(1);}}
@keyframes heroSpin{to{transform:rotate(360deg);}}
#hero>*{position:relative;z-index:2;}
#hero>div{max-width:1000px;}
#hero>div>div[style*="inline-flex"]{justify-content:center;}        /* eyebrow */
#hero h1{font-size:clamp(46px,7.4vw,108px) !important;line-height:.96 !important;
  letter-spacing:-.04em !important;max-width:15ch;margin:0 auto 26px !important;text-wrap:balance;}
#hero p{margin:0 auto 34px !important;text-align:center;max-width:620px !important;}
#hero>div>div[style*="display:flex"]{justify-content:center;}        /* CTAs + stats rows */
/* portrait now lives in #story (About). Compose it as an editorial anchor. */
.soyli-portrait{width:min(360px,82vw);margin:0 auto 30px;}
.soyli-portrait>div:last-child{max-width:360px !important;margin:0 auto !important;}
#story{padding-top:96px !important;}
/* animated gradient emphasis words in the headline */
#hero h1 span{background:linear-gradient(100deg,#FFB079,#FF8A3C,#FF5A2C,#FF8A3C,#FFB079);
  background-size:300% 100%;-webkit-background-clip:text;background-clip:text;
  -webkit-text-fill-color:transparent;color:transparent !important;animation:wordHue 7s linear infinite;}
@keyframes wordHue{0%{background-position:0% 50%;}100%{background-position:300% 50%;}}
/* oversized Anton ghost numbers on the main experience sections */
#why,#cases,#toyota-byy,#haryt,#ai-agent{position:relative;overflow:hidden;}
#why::before,#cases::before,#toyota-byy::before,#haryt::before,#ai-agent::before{
  font-family:'Anton',sans-serif;position:absolute;top:30px;right:40px;z-index:0;line-height:.8;
  font-size:200px;color:rgba(255,138,60,.07);pointer-events:none;letter-spacing:-.02em;}
#why::before{content:"01";}
#cases::before{content:"02";}
#toyota-byy::before{content:"03";}
#haryt::before{content:"04";}
#ai-agent::before{content:"05";}
/* ===== EDITORIAL two-column About (#story) ===== */
#story{display:grid !important;grid-template-columns:330px minmax(0,1fr);gap:60px;align-items:start;text-align:left;max-width:1200px;}
.soyli-portrait{margin:0 !important;width:330px;position:sticky;top:92px;}
.soyli-portrait>div:last-child{max-width:330px !important;margin:0 !important;}
.story-body{text-align:left;}
.story-body h2{max-width:none !important;}
@media(max-width:860px){
  #story{display:block !important;}
  .soyli-portrait{position:static !important;margin:0 auto 30px !important;}
}
/* ===== BIG editorial rhythm: generous spacing + dividers ===== */
#story,#certs,#why,#cases,#toyota-byy,#haryt,#emails,#motion-videos,#ai-agent,#proof,#contact-form{
  padding-top:112px !important;padding-bottom:112px !important;}
#certs,#why,#cases,#toyota-byy,#haryt,#ai-agent,#proof{position:relative;}
#certs::after,#why::after,#cases::after,#toyota-byy::after,#haryt::after,#ai-agent::after{
  content:"";position:absolute;left:50%;top:0;transform:translateX(-50%);width:min(1200px,90%);height:1px;
  background:linear-gradient(90deg,transparent,rgba(255,138,60,.35),transparent);}
/* darkened certs section: force heading, body & chips to light */
#certs h2{color:#F4ECE3 !important;}
#certs p{color:#C7B7AC !important;}
#certs span[style*="border"]{color:#E2D4C9 !important;border-color:rgba(255,255,255,.22) !important;}
/* bright gradient on primary buttons that were the gold fill */
a[href="#contact-form"],a[href="#contact"]{}
</style>
'''
    t = t.replace('</body>', polish+'</body>', 1)

    pathlib.Path(out).write_text(t)
    print("WROTE", out, len(t), "| orange accents:", t.count('#FF8A3C'), "| Space Grotesk usages:", t.count("Space Grotesk"))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
