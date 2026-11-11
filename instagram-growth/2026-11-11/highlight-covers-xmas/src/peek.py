import sys
from PIL import Image
# peek.py out.jpg img1 img2 ... : half-scale side by side
ims=[Image.open(f).convert('RGB') for f in sys.argv[2:]]
ims=[i.resize((i.width//2,i.height//2)) for i in ims]
c=Image.new('RGB',(sum(i.width for i in ims),max(i.height for i in ims)))
x=0
for i in ims: c.paste(i,(x,0)); x+=i.width
c.save(sys.argv[1])
