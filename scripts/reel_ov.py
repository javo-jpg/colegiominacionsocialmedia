from PIL import Image, ImageDraw, ImageFont
import sys; sys.path.insert(0,"/home/claude/scripts")
F="/home/claude/zip/Entrega/Fonts/"
MIJA=F+"Mija W03 Regular.ttf"; SB=F+"Sohne-Kraftig.otf"; SL=F+"Sohne-Leicht.otf"
G=(35,93,78); LG=(220,229,182); Y=(237,204,111); B=(84,158,187); C=(252,248,239); P=(232,131,107)
O="/home/claude/reel/ov/"
W,H=1080,1920
def blank(): return Image.new("RGBA",(W,H),(0,0,0,0))
def pill(d,y,lines,font,fg=G,bg=C,pad=(44,26),gap=10,x=None):
    ws=[d.textlength(l,font=font) for l in lines]; lh=font.size*1.12
    w=max(ws)+pad[0]*2; h=lh*len(lines)+pad[1]*2-(lh-font.size)
    x0=(W-w)/2 if x is None else x
    d.rounded_rectangle([x0,y,x0+w,y+h],radius=28,fill=bg)
    for i,l in enumerate(lines): d.text((x0+pad[0],y+pad[1]+i*lh),l,font=font,fill=fg)
    return y+h
def tag(d,y,text,bg=Y,fg=G):
    f=ImageFont.truetype(SB,38); w=d.textlength(text,font=f)+48
    d.rounded_rectangle([(W-w)/2,y,(W+w)/2,y+66],radius=33,fill=bg); d.text((W/2,y+33),text,font=f,fill=fg,anchor="mm")
# hook title
im=blank(); d=ImageDraw.Draw(im)
f=ImageFont.truetype(MIJA,96)
tag(d,1180,"DÍA DE MUERTOS 2026")
pill(d,1270,["Así se vivió","en Mi Nación"],f,fg=C,bg=G,pad=(56,34))
im.save(O+"hook.png")
# captions
caps={"ofrendas":(["Ofrendas hechas","por nuestros alumnos"],None),
 "entrevistas":(["Nos explicaron","qué significa su ofrenda"],"ALUMNOS"),
 "entrevistas2":(["Tradición que se aprende","y se comparte"],None),
 "comunidad":(["Toda la comunidad","reunida"],None),
 "baile":(["Y una presentación","inspirada en Michael Jackson"],None)}
for k,(lines,t) in caps.items():
    im=blank(); d=ImageDraw.Draw(im)
    y=1330
    if t: tag(d,y-86,t,bg=B,fg=C)
    pill(d,y,lines,ImageFont.truetype(SB,52))
    im.save(O+k+".png")
# end card (opaque) frames: picado drop animation handled by ffmpeg overlay; make static card + picado strip
im=Image.new("RGB",(W,H),G); d=ImageDraw.Draw(im)
fw=W/7
for i in range(7):
    x=i*fw+10; col=[Y,P,B,LG][i%4]; top=230; bot=230+int(fw*1.1)
    d.polygon([(x,top),(x+fw-20,top),(x+fw-20,bot),(x+(fw-20)/2,bot-26),(x,bot)],fill=col)
    cx=x+(fw-20)/2; cy=(top+bot)/2-8; d.regular_polygon((cx,cy,18),4,rotation=45,fill=G)
d.line([(0,230),(W,230)],fill=Y,width=4)
f1=ImageFont.truetype(MIJA,104); y=640
for l in ["Tradición,","valores y","comunidad."]:
    d.text((90,y),l,font=f1,fill=C); y+=118
f2=ImageFont.truetype(SL,44)
d.text((90,y+30),"Preescolar y primaria en Coyoacán",font=f2,fill=LG)
d.text((90,y+90),"Español · Inglés · Francés",font=f2,fill=LG)
y+=200
d.rounded_rectangle([90,y,90+600,y+104],radius=52,fill=Y)
d.text((90+300,y+52),"Pide informes",font=ImageFont.truetype(SB,50),fill=G,anchor="mm")
d.text((90,y+140),"WhatsApp 56 5292 2720",font=ImageFont.truetype(SB,46),fill=C)
d.text((90,y+200),"colegiominacion.com",font=ImageFont.truetype(SL,46),fill=C)
lg=Image.open("/home/claude/colegiominacionsocialmedia/brand/logo-horizontal-verdeclaro.png").convert("RGBA"); lg=lg.crop(lg.getbbox()); lg=lg.resize((380,int(380*lg.height/lg.width)))
im.paste(lg,(90,1560),lg)
im.save(O+"end.png")
print("ok")
