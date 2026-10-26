#!/usr/bin/env python3
"""Render original PFarma Beauty typographic graphics for 26 Oct–1 Nov 2026.

No synthetic treatment results or patient/client photos. Copy and prices supplied
by PFarma. High-resolution static PNGs suitable for Buffer feed and auto-Stories.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

OUT=Path("media/week-2026-10-26")
BG="#F8F4EE"; DARK="#342D34"; PINK="#A65E70"; MUTED="#6A5B64"; PALE="#EBD9DB"; WHITE="#FFFFFF"; GOLD="#B18B58"

CAMPAIGNS=[
 dict(slug="beauty-check",small="CONSULENZA DERMOCOSMETICA",lead=["LA TUA PELLE", "PRIMA DI TUTTO."],
      sub=["Non serve l'ennesima crema:", "serve capire di cosa ha", "davvero bisogno la tua pelle."],
      cta="SCRIVICI PELLE IN DM",footer="Beauty Check PFarma • Lamezia Terme"),
 dict(slug="unghie",small="PFARMA BEAUTY · UNGHIE",lead=["GEL O", "SEMIPERMANENTE?"],
      sub=["Non è solo una scelta di colore.", "Valutiamo insieme il trattamento", "più adatto alle tue unghie."],
      cta="SCRIVICI UNGHIE IN DM",footer="Operatrice specializzata • Lamezia Terme"),
 dict(slug="pulizia-viso",small="PFARMA BEAUTY · VISO",lead=["UNA PELLE", "NON VALE L'ALTRA."],
      sub=["Pulizia viso personalizzata:", "partiamo dalle esigenze", "della tua pelle."],
      cta="SCRIVICI VISO IN DM",footer="Informazioni e prenotazioni • Lamezia Terme"),
 dict(slug="sopracciglia-novembre",small="OFFERTA DI NOVEMBRE",lead=["TATUAGGIO", "SOPRACCIGLIA"],
      sub=["Solo per tutto il mese di novembre.", "Chiedi informazioni e disponibilità."],
      cta="SCRIVICI SOPRACCIGLIA",footer="PFarma Beauty • Lamezia Terme",price="179 €",old="399 €"),
 dict(slug="sopracciglia-anteprima",small="DA DOMANI · NOVEMBRE",lead=["TATUAGGIO", "SOPRACCIGLIA"],
      sub=["Dal 1° novembre:", "una promozione speciale ti aspetta.", "Prenotazioni e informazioni in DM."],
      cta="SCRIVICI SOPRACCIGLIA",footer="PFarma Beauty • Lamezia Terme",price="179 €",old="399 €"),
]

def font(sz,bold=False):
    import os
    file="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    if not os.path.exists(file): return ImageFont.load_default(size=sz)
    return ImageFont.truetype(file,sz)

def center_text(draw,xy,text,ft,fill,anchor="mm"):
    draw.text(xy,text,font=ft,fill=fill,anchor=anchor,stroke_width=0)

def fit(draw,t,maxwidth,size=80,minsize=28,bold=True):
    for pt in range(size,minsize-1,-2):
        x=font(pt,bold)
        if draw.textbbox((0,0),t,font=x)[2]<=maxwidth: return x
    return font(minsize,bold)

def generate(item,mode):
    W=1080
    H=1920 if mode=="story" else 1350
    img=Image.new("RGB",(W,H),BG);d=ImageDraw.Draw(img)
    d.ellipse((735,-280,1370,355),fill=PALE)
    d.ellipse((-250,H-440,350,H+160),fill=PALE)
    d.ellipse((755,H-405,1250,H+90),outline=GOLD,width=3)
    d.rounded_rectangle((44,44,W-44,H-44),radius=34,outline=DARK,width=3)
    top=244 if mode=="story" else 128
    center_text(d,(W//2,top),"P F A R M A",font(39,True),DARK)
    center_text(d,(W//2,top+55),"B E A U T Y   ·   L A M E Z I A   T E R M E",fit(d,"B E A U T Y   ·   L A M E Z I A   T E R M E",920,24,22,True),PINK)
    dy=380 if mode=="story" else 248
    d.rounded_rectangle((120,dy-22,960,dy+36),radius=29,fill=PALE)
    center_text(d,(540,dy+8),item["small"],fit(d,item["small"],790,27,22,True),DARK)
    title_top=520 if mode=="story" else 389
    lines=item["lead"]
    for i,line in enumerate(lines):
        sz=87 if mode=="story" else 79
        ft=fit(d,line,930,sz,38,True)
        center_text(d,(W//2,title_top+i*114),line,ft,DARK)
    linebase=title_top+len(lines)*116
    d.rounded_rectangle((410,linebase+15,670,linebase+22),radius=3,fill=PINK)
    if "price" in item:
        priceY=linebase+155
        center_text(d,(540,priceY-74),"ANZICHÉ  "+item["old"],font(36,True),MUTED)
        d.line((410,priceY-72,670,priceY-72),fill=PINK,width=5)
        center_text(d,(540,priceY+28),item["price"],font(126,True),PINK)
        substart=priceY+183
        substep=60
    else:
        substart=linebase+135
        substep=63
    for i,line in enumerate(item["sub"]):
        ft=fit(d,line,930,40,24,False)
        center_text(d,(540,substart+i*substep),line,ft,MUTED)
    ctaY=H-310 if mode=="story" else H-210
    d.rounded_rectangle((100,ctaY-62,980,ctaY+62),radius=62,fill=DARK)
    center_text(d,(540,ctaY),item["cta"],fit(d,item["cta"],780,37,24,True),WHITE)
    footY=H-190 if mode=="story" else H-124
    center_text(d,(540,footY),item["footer"],fit(d,item["footer"],940,25,21),DARK)
    target=OUT/(item["slug"]+"-"+mode+".png")
    img.save(target,format="PNG",optimize=True)
    return str(target)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    paths=[]
    for item in CAMPAIGNS:
        for mode in ("feed","story"):
            if mode=="feed" and item["slug"]=="sopracciglia-anteprima": continue
            paths.append(generate(item,mode))
    print("CREATED",len(paths),"PFARMA_ORIGINAL_BRANDED_MEDIA")
    for path in paths:
        im=Image.open(path)
        assert im.width==1080 and im.height in (1350,1920)
        assert im.mode=="RGB"
        assert im.getbbox() is not None
        assert Path(path).stat().st_size<4*1024*1024
        print(path,im.size,Path(path).stat().st_size)
if __name__=="__main__": main()
