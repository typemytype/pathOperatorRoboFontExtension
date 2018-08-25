from drawBot import *

size(500, 500)

B1 = BezierPath()
B1.rect(60, 50, 250, 250)

B2 = BezierPath()
B2.oval(160, 160, 290, 290)

B3 = B1.xor(B2)

fill(0)
drawPath(B3)

import os
folder = os.getcwd()
imgPath = os.path.join(folder, 'pathOperatorIcon.png')
saveImage(imgPath)