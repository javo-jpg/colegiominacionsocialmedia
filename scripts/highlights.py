from PIL import Image, ImageDraw, ImageFont
F="/home/claude/zip/Entrega/Fonts/"
SB=ImageFont.truetype(F+"Sohne-Kraftig.otf",120)
G="#235D4E"; LG="#DCE5B6"; Y="#EDCC6F"; B="#549EBB"; C="#FCF8EF"; P="#E8836B"
items=[("Informes",G,C),("Preescolar",Y,G),("Primaria",B,C),("Idiomas",LG,G),("Aliados",P,C),("Papás",C,G),("Familias",G,Y),("Vida MN",Y,G)]
OUT="/home/claude/colegiominacionsocialmedia/assets/highlights/"
sheet=Image.new("RGB",(8*220,240),"white")
for i,(t,bg,fg) in enumerate(items):
    im=Image.new("RGB",(1080,1920),bg); d=ImageDraw.Draw(im)
    eye=Image.open("/home/claude/zip/Entrega/png/ColgeioNacion--16.png").convert("RGBA")
    eye=eye.crop(eye.getbbox()); a=eye.split()[3]
    sym=Image.new("RGBA",eye.size,fg); sym.putalpha(a); sym=sym.resize((300,int(300*eye.height/eye.width)))
    im.paste(sym,(540-150,945-sym.height),sym)
    size=120
    while d.textlength(t,font=ImageFont.truetype(F+"Sohne-Kraftig.otf",size))>620: size-=6
    d.text((540,985),t,font=ImageFont.truetype(F+"Sohne-Kraftig.otf",size),fill=fg,anchor="mt")
    fn=f"{i+1:02d}-{t.lower().replace(' ','-').replace('á','a')}.png"; im.save(OUT+fn)
    th=im.crop((0,420,1080,1500)).resize((200,200)); m=Image.new("L",(200,200),0); ImageDraw.Draw(m).ellipse([0,0,199,199],fill=255)
    sheet.paste(th,(i*220+10,20),m)
sheet.save("/tmp/claude-0/-home-claude/444e3eaf-71af-54ce-9adf-da3812e7752b/scratchpad/hl.jpg")
