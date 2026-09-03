# gera a teste.png
from PIL import Image, ImageDraw

img = Image.new("L", (200, 150), 0)
d = ImageDraw.Draw(img)

d.rectangle([15, 15, 60, 60], fill=255)                 # quadrado grande
d.ellipse([90, 10, 140, 60], fill=255)                  # circulo
d.polygon([(160, 55), (190, 55), (175, 15)], fill=255)  # triangulo
d.rectangle([20, 90, 45, 115], fill=255)                # quadrado pequeno
d.ellipse([70, 85, 130, 135], fill=255)                 # circulo grande
d.rectangle([150, 100, 165, 115], fill=255)             # quadradinho
d.point((180, 130), fill=255)                           # pixel sozinho

img.save("teste.png")
