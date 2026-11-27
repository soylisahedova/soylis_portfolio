#!/usr/bin/env python3
# Creative DARK re-theme: keep the dark site + ALL content/images/videos,
# swap gold/sage -> red/orange cinematic accents, Wix Madefor/IBM Plex -> Space Grotesk,
# add Anton big section numbers + hero glow. Nothing removed.
import re, sys, pathlib

def main(src, out):
    t = pathlib.Path(src).read_text(errors='replace')

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
/* cinematic glow top-right of hero */
#hero{position:relative;}
#hero::after{content:"";position:absolute;inset:-10% -5% auto auto;width:60%;height:120%;z-index:0;pointer-events:none;
  background:radial-gradient(55% 55% at 75% 25%,rgba(255,106,30,.28),transparent 62%),
   radial-gradient(45% 45% at 88% 55%,rgba(226,58,30,.26),transparent 64%);filter:blur(10px);}
#hero>*{position:relative;z-index:2;}
/* oversized Anton ghost numbers on the main experience sections */
#cases,#toyota-byy,#haryt,#ai-agent{position:relative;overflow:hidden;}
#cases::before,#toyota-byy::before,#haryt::before,#ai-agent::before{
  font-family:'Anton',sans-serif;position:absolute;top:24px;right:30px;z-index:0;line-height:.8;
  font-size:170px;color:rgba(255,138,60,.07);pointer-events:none;letter-spacing:-.02em;}
#cases::before{content:"01";}
#toyota-byy::before{content:"02";}
#haryt::before{content:"03";}
#ai-agent::before{content:"04";}
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
