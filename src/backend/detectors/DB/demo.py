from inference import detect_single_image
import timeit

print('ok')
import cv2

img = cv2.imread(r'C:\Users\Mr.Son\Desktop\test\LienPhai-2437.jpg', 1)
print(img.shape)
start = timeit.default_timer()
detect_single_image(img)
stop = timeit.default_timer()
print('Time: ', stop - start) 

from ops import *
import torch
offset = torch.rand((1, 18, 256, 256))
input = torch.rand((1, 126, 256, 256))
mask = torch.rand((1, 9, 256, 256))

test = ModulatedDeformConv(126, 256, 3)
start = timeit.default_timer()
with torch.no_grad():
	outp =  test(input, offset, mask)
stop = timeit.default_timer()
print('Time: ', stop - start) 

# Time:  5.47147
# Time:  10.6686551