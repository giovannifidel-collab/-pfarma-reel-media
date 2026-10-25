#!/usr/bin/env python3
"""Generate ten brand-aware, typographic PFarma marketing JPG creatives.

Public content only: no patient/client data, no fake before-and-after, no
stock photo falsely described as in-house work. Printed offer exactly as user
authorized: eyebrow tattoo 179 euro instead of 399 during November only.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import textwrap

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT/"media"/"weekly"/"2026-10-26"
BASE.mkdir(parents=True,exist_ok=True)
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def F(n,bold=False):
    return ImageFont.truetype(BOLD if bold else FONT,n)

themes={
 "skincare":("#102E32","#F6EDE6","#B9D6CB","#F1C3B4"),
 "unghie":("#56364B","#FAEFF0","#F1C8D5","#E8B5AC"),
 "viso":("#254844","#F3F1E9","#BED4C3","#DFC2A6"),
 "laser":("#233B51","#EFF4F5","#B1D2D6","#D9BEAA"),
 "pmu":("#582B3D","#FFF4ED","#E7B7B0","#E9BF7E")
}
cards=[
 dict(name="skincare_feed",kind="feed",theme="skincare",eyebrow="DERMOCOSMESI",headline=["LA CREMA","PIÙ COSTOSA","NON È SEMPRE","LA MIGLIORE."],body=["La routine giusta nasce","dalle esigenze della tua pelle."],call="Scrivici PELLE in DM",foot="Un consiglio professionale, non una scelta a caso."),
 dict(name="unghie_feed",kind="feed",theme="unghie",eyebrow="PFARMA BEAUTY · UNGHIE",headline=["GEL O","SEMIPERMANENTE?"],body=["La scelta parte dalle tue unghie,","non soltanto dal colore."],call="Scrivici UNGHIE in DM",foot="Informazioni e trattamenti con l'operatrice specializzata."),
 dict(name="viso_feed",kind="feed",theme="viso",eyebrow="PFARMA BEAUTY · VISO",headline=["PULIZIA VISO","SU MISURA."],body=["Prima di ogni trattamento:","esigenze, sensibilità e obiettivi."],call="Scrivici VISO in DM",foot="Scopri come funziona la valutazione iniziale."),
 dict(name="laser_feed",kind="feed",theme="laser",eyebrow="PFARMA BEAUTY · EPILAZIONE",headline=["PRIMA DEL LASER","VIENE LA","VALUTAZIONE."],body=["Pelle, pelo e controindicazioni:","il percorso inizia da qui."],call="Scrivici LASER in DM",foot="Ogni protocollo si valuta individualmente."),
 dict(name="pmu_feed",kind="feed",theme="pmu",eyebrow="PROMO DI NOVEMBRE · PFARMA BEAUTY",headline=["TATUAGGIO","SOPRACCIGLIA"],body=["Solo per il mese di novembre"],call="Scrivici SOPRACCIGLIA",oldprice="399 €",newprice="179 €",foot="Informazioni e prenotazioni in privato."),
 dict(name="unghie_story",kind="story",theme="unghie",eyebrow="IL CONSIGLIO BEAUTY",headline=["UNGHIE","DA VALORIZZARE?"],body=["Gel o semipermanente?","Partiamo dalle tue esigenze."],call="Scrivici UNGHIE in DM",foot="PFarma Beauty · Lamezia Terme"),
 dict(name="viso_story",kind="story",theme="viso",eyebrow="CURA DEL VISO",headline=["PULIZIA VISO","PERSONALIZZATA"],body=["Il trattamento giusto","non è uguale per tutti."],call="Scrivici VISO in DM",foot="PFarma Beauty · Lamezia Terme"),
 dict(name="laser_story",kind="story",theme="laser",eyebrow="EPILAZIONE CONSAPEVOLE",headline=["IL LASER","NON È PER TUTTI."],body=["Una valutazione accurata","fa la differenza."],call="Scrivici LASER in DM",foot="PFarma Beauty · Lamezia Terme"),
 dict(name="pmu_tease_story",kind="story",theme="pmu",eyebrow="ANTICIPAZIONE · NOVEMBRE",headline=["DAL 1°","NOVEMBRE","UNA NOVITÀ."],body=["Una promozione dedicata","al tatuaggio sopracciglia."],call="Scoprila domani",foot="PFarma Beauty · Lamezia Terme"),
 dict(name="pmu_story",kind="story",theme="pmu",eyebrow="PROMO NOVEMBRE",headline=["TATUAGGIO","SOPRACCIGLIA"],body=["Solo per il mese di novembre"],call="Scrivici SOPRACCIGLIA",oldprice="399 €",newprice="179 €",foot="PFarma Beauty · Lamezia Terme"),
]
def textbounds(d,text,font):
    b=d.textbbox((0,0),text,font=font)
    return (b[2]-b[0],b[3]-b[1])
def fit_font(d,words,start,max_width,bold=True):
    size=start
    while size>32 and any(textbounds(d,x,F(size,bold))[0] > max_width for x in words):
        size-=2
    return F(size,bold)
def rounded(d,rect,color,radius=32,width=0,outline=None):
    d.rounded_rectangle(rect,radius=radius,fill=color,outline=outline,width=width)
def make(c):
    story=c["kind"]=="story"
    W,H=1080,1920 if story else 1350
    dark,cream,muted,accent=themes[c["theme"]]
    im=Image.new("RGB",(W,H),cream)
    d=ImageDraw.Draw(im)
    # Colored solid half-plane with soft high-contrast geometric layering.
    topheight=round(H*(.715 if story else .69))
    d.rectangle((0,0,W,topheight),fill=dark)
    d.ellipse((W-300,-320,W+480,450),outline=accent,width=5)
    d.ellipse((-420,topheight-400,310,topheight+350),outline=muted,width=4)
    for n in range(4):
        x=W-210+n*33
        d.arc((x-120,topheight-440,x+330,topheight+80),-160,20,fill=accent,width=3)
    # Brand wordmark: typography, not claiming a registered logo facsimile
    d.text((80,94),"PFARMA",font=F(46,True),fill=cream)
    d.text((80,157),"beauty & dermocosmesi",font=F(24),fill=muted)
    d.line((80,205,W-80,205),fill=accent,width=2)
    efont=F(27,True)
    ey=c["eyebrow"]
    d.text((80,292 if story else 266),ey,font=efont,fill=muted)
    lines=c["headline"]
    headlinefont=fit_font(d,lines,80 if story else 73,W-160)
    lineheight=headlinefont.size+28
    hy=370 if story else 345
    for ln in lines:
        d.text((78,hy),ln,font=headlinefont,fill=cream)
        hy+=lineheight
    if c.get("newprice"):
        # Reserve strong promotion price area within dark upper half.
        py=max(hy+34,750 if story else 665)
        d.text((85,py),c["newprice"],font=F(132 if story else 122,True),fill=accent)
        ow=F(42,True)
        oldxy=(93,py+(167 if story else 155))
        d.text(oldxy,"anziché "+c["oldprice"],font=ow,fill=cream)
        oldstart=oldxy[0]+textbounds(d,"anziché ",ow)[0]
        oldend=oldstart+textbounds(d,c["oldprice"],ow)[0]
        d.line((oldstart,oldxy[1]+29,oldend,oldxy[1]+29),fill=accent,width=5)
        body_start=py+(245 if story else 223)
    else:
        body_start=max(hy+65,810 if story else 735)
    bf=fit_font(d,c["body"],42 if story else 35,W-170,False)
    for ln in c["body"]:
        d.text((86,body_start),ln,font=bf,fill=cream)
        body_start+=bf.size+20
    # Accent pills and strong CTA: keep bottom 100% readable.
    cta_y=round(H*(.80 if story else .79))
    btn_width=W-146
    rounded(d,(72,cta_y,72+btn_width,cta_y+(136 if story else 126)),dark,34)
    cf=fit_font(d,[c["call"]],42 if story else 38,btn_width-100,True)
    tw,th=textbounds(d,c["call"],cf)
    d.text((W/2-tw/2,cta_y+(70 if story else 63)-th/2-5),c["call"],font=cf,fill=cream)
    footer_y=H-147 if story else H-105
    foot_font=fit_font(d,[c["foot"]],24 if story else 22,W-100,False)
    fw,_=textbounds(d,c["foot"],foot_font)
    d.text(((W-fw)/2,footer_y),c["foot"],font=foot_font,fill=dark)
    # Decorative brand stripe
    d.rectangle((0,H-16,W,H),fill=accent)
    path=BASE/(c["name"]+".jpg")
    im.save(path,format="JPEG",quality=91,optimize=True,subsampling=0)
    check=Image.open(path)
    assert check.size==(W,H)
    assert path.stat().st_size<8*1024*1024
    print(c["name"],check.size,path.stat().st_size,"bytes")
for c in cards: make(c)
