import random
import zlib
from math import log2

txt = 'ABC abc'
b_ascii = bytearray(txt, 'ASCII')

for i in range(len(b_ascii)):
    print(f"Symbol: {txt[i]}, ASCII Value: {b_ascii[i]}")

try:
    txt_swedish = 'ÅÄÖ'
    b_ascii_swedish = bytearray(txt_swedish, 'ASCII')
except UnicodeEncodeError as e:
    print(f"UnicodeEncodeError: {e}")

txt_latin1_swedish = 'ÅÄÖ'
b_latin1_swedish = bytearray(txt_latin1_swedish, 'LATIN-1')

txt_utf8_swedish = 'ÅÄÖ'
b_utf8_swedish = bytearray(txt_utf8_swedish, 'UTF-8')

with open("labb09/exempeltext.txt", "r", encoding="utf-8") as file:
    txt = file.read()
    byteArr = bytearray(txt, "utf-8")

num_symbols = len(txt)
num_bytes = len(byteArr)
print(f"Number of symbols: {num_symbols}, Number of bytes: {num_bytes}")

def makeHisto(byteArr):
    histo = [0] * 256
    for byte in byteArr:
        histo[byte] += 1
    return histo

def makeProb(histo):
    total = sum(histo)
    return [count / total for count in histo]

def entropy(prob):
    return -sum(p * log2(p) if p != 0 else 0 for p in prob)

histo = makeHisto(byteArr)
prob = makeProb(histo)
entropy_value = entropy(prob)

print(f"Entropy: {entropy_value} bits/symbol")

theCopy = byteArr.copy()
random.shuffle(theCopy)

zip_code_copy = zlib.compress(theCopy)
zip_code_original = zlib.compress(byteArr)

bits_per_symbol_original = len(zip_code_original) * 8 / num_symbols
bits_per_symbol_copy = len(zip_code_copy) * 8 / num_symbols

print(f"Bits per symbol (Original): {bits_per_symbol_original}")
print(f"Bits per symbol (Shuffled): {bits_per_symbol_copy}")

t1 = """I hope this lab never ends because it is so incredibly thrilling!"""
t10 = 10 * t1

zip_t1 = zlib.compress(bytearray(t1, 'utf-8'))
zip_t10 = zlib.compress(bytearray(t10, 'utf-8'))

print(f"Size of zip_t1: {len(zip_t1)} bytes")
print(f"Size of zip_t10: {len(zip_t10)} bytes")
