from PIL import Image, ImageDraw

size = 64
img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
draw.ellipse((4, 4, size-4, size-4), fill=(33,150,243), outline=(255,255,255), width=2)
cx, cy = size//2, size//2
draw.ellipse((cx-3, cy-3, cx+3, cy+3), fill=(255,255,255))
draw.line((cx, cy, cx, cy-20), fill=(255,255,255), width=3)
draw.line((cx, cy, cx+18, cy), fill=(255,255,255), width=2)
img.save("icon.ico", format="ICO", sizes=[(size, size)])