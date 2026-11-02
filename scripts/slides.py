from PIL import Image, ImageDraw, ImageFont
import random
F="/home/claude/zip/Entrega/Fonts/"
MIJA=F+"Mija W03 Regular.ttf"; SB=F+"Sohne-Kraftig.otf"; SL=F+"Sohne-Leicht.otf"
G="#235D4E"; LG="#DCE5B6"; Y="#EDCC6F"; B="#549EBB"; C="#FCF8EF"; P="#E8836B"
OUT="/home/claude/colegiominacionsocialmedia/assets/2026-11/01-ofrendas/"
BR="/home/claude/colegiominacionsocialmedia/brand/"
def logo(path,w):
    im=Image.open(path).convert("RGBA"); bb=im.getbbox(); im=im.crop(bb)
    h=int(im.height*w/im.width); return im.resize((w,h),Image.LANCZOS)
def picado(d,W,y0,n,cols,seed=3):
    random.seed(seed)
    d.line([(0,y0),(W,y0)],fill=cols[0],width=4)
    fw=W/n
    for i in range(n):
        x=i*fw+8; c=cols[i%len(cols)]
        top=y0+6; bot=y0+int(fw*1.1)
        d.polygon([(x,top),(x+fw-16,top),(x+fw-16,bot),(x+(fw-16)/2,bot-22),(x,bot)],fill=c)
        # cut-outs
        cx=x+(fw-16)/2; cy=(top+bot)/2-6
        d.ellipse([cx-14,cy-14,cx+14,cy+14],fill=None,outline=None)
        for k in range(4):
            ang=k*90
        d.regular_polygon((cx,cy,16),4,rotation=45,fill=BG)
        d.ellipse([cx-6,top+12,cx+6,top+24],fill=BG)
        d.ellipse([x+10,bot-40,x+20,bot-30],fill=BG); d.ellipse([x+fw-36,bot-40,x+fw-26,bot-30],fill=BG)
def wrap(d,text,font,maxw):
    words=text.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t,font=font)<=maxw: cur=t
        else: lines.append(cur); cur=w
    lines.append(cur); return lines
# COVER 1080x1080
for name,(W,H) in {"01-portada.jpg":(1080,1080),"story-portada.jpg":(1080,1920)}.items():
    BG=G
    im=Image.new("RGB",(W,H),G); d=ImageDraw.Draw(im)
    top = 0 if H==1080 else 260
    picado(d,W,top,7,[Y,P,B,LG])
    f1=ImageFont.truetype(MIJA,118); f2=ImageFont.truetype(SB,40); f3=ImageFont.truetype(SL,34)
    y = 330 if H==1080 else 720
    d.text((80,y-70),"DÍA DE MUERTOS 2026",font=f2,fill=Y)
    for ln in ["Así vivimos","nuestras","ofrendas"]:
        d.text((80,y),ln,font=f1,fill=C); y+=128
    d.text((80,y+30),"Preescolar Fresno · Primaria San Felipe",font=f3,fill=LG)
    lg=logo(BR+"logo-horizontal-verdeclaro.png",330)
    im.paste(lg,(80,H-lg.height-(80 if H==1080 else 440)),lg)
    if H==1080:
        d.text((W-130,H-112),"Desliza",font=f2,fill=Y,anchor="ra")
        ay=H-92; d.line([(W-118,ay),(W-80,ay)],fill=Y,width=5); d.polygon([(W-80,ay-12),(W-64,ay),(W-80,ay+12)],fill=Y)
    im.save(OUT+name,quality=92)
# CTA 1080x1080
BG=C
W=H=1080
im=Image.new("RGB",(W,H),C); d=ImageDraw.Draw(im)
picado(d,W,0,7,[G,Y,B,P],seed=5)
f1=ImageFont.truetype(MIJA,84); f2=ImageFont.truetype(SB,38); f3=ImageFont.truetype(SL,36)
y=300
for ln in ["Tradición, valores","y comunidad,","todos los días."]:
    d.text((80,y),ln,font=f1,fill=G); y+=94
y+=30
for ln in wrap(d,"Conoce Colegio Mi Nación: preescolar y primaria en Coyoacán, con español, inglés y francés.",f3,920):
    d.text((80,y),ln,font=f3,fill="#2b2b2b"); y+=48
y+=30
d.rounded_rectangle([80,y,80+560,y+86],radius=43,fill=G)
d.text((80+280,y+43),"Pide informes",font=f2,fill=C,anchor="mm")
d.text((80,y+120),"WhatsApp 56 5292 2720 · colegiominacion.com",font=f2,fill=G)
lg=logo(BR+"logo-horizontal-verde.png",300); im.paste(lg,(80,H-lg.height-70),lg)
im.save(OUT+"99-cta.jpg",quality=92)
print("ok")
