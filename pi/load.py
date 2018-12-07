import matplotlib.pyplot as plt
import time
from PIL import Image

s = time.time()
img = Image.open('right/path_0.jpg')
e = time.time()
print(e-s)
