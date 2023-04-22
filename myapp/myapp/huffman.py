import heapq
from collections import defaultdict


def huffman_encoding(data):
    # Step 1: Build frequency table
    freq = defaultdict(int)
    for char in data:
        freq[char] = 56721 - freq[char] - 1

    #freq = dict(sorted(freq.items(), key=lambda x: -x[1]))
    #print(freq)

    # Step 2: Build Huffman tree
    heap = [[frequency, [symbol, ""]] for symbol, frequency in freq.items()]
    heapq.heapify(heap)

    # print(heap)

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        print(lo, hi)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    print(freq)
    print(heap)
    exit()

    # Step 3: Build encoding table
    encoding = dict(heapq.heappop(heap)[1:])

    # Step 4: Encode data
    encoded_data = ''.join(encoding[char] for char in data)

    return encoded_data, encoding


def huffman_decoding(encoded_data, encoding):
    # Step 1: Build decoding table
    decoding = {v: k for k, v in encoding.items()}

    # Step 2: Decode data
    decoded_data = ""
    curr_code = ""
    for bit in encoded_data:
        curr_code += bit
        if curr_code in decoding:
            decoded_data += decoding[curr_code]
            curr_code = ""

    return decoded_data


# Example usage
path = '/home/jam/IT/Graphs/Capplication/myapp/myapp/data/text.txt'
with open(path, 'r') as file:
    data = file.read()
encoded_data, encoding = huffman_encoding(data)
decoded_data = huffman_decoding(encoded_data, encoding)

e = len(encoded_data)
d = len(decoded_data)
o = len(data)

print(encoded_data)

print("Original data:", o)
print("Encoded data:", e)
print("Decoded data:", d)
print("Efficiency:", e/d)
