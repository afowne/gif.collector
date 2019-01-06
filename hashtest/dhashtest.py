#https://github.com/hjaurum/DHash
from dhash import DHash
from PIL import Image


im1 = Image.open("F:\python\gif\qq-1.png")
im2 = Image.open("F:\python\gif\qq-2.png")
hash1 = DHash.calculate_hash(im1)
hash2 = DHash.calculate_hash(im2)


hamming_distance = DHash.hamming_distance(im1, im2)
print(hamming_distance)
hamming_distance = DHash.hamming_distance(hash1, hash2)
print(hamming_distance)
#一般来说，汉明距离小于5，基本就是同一张图片。大家可以根据自己的实际情况，判断汉明距离临界值为多少。

 