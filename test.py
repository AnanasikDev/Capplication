# import pickle
# import struct
#
# # Create a dictionary to encode
# my_dict = {'name': 'John', 'age': 30, 'city': 'New York'}
#
# # Encode the dictionary into a file
# with open('my_dict.pickle', 'wb') as f:
#     f.write(struct.pack('<4s', bytes.fromhex('CAFEFADE')))
#     encoded_dict = pickle.dumps(my_dict)
#     l = len(encoded_dict)
#     pickle.dump(my_dict, f)
#     print(l)
#
# # Decode the dictionary from the file
# with open('my_dict.pickle', 'rb') as f:
#     # Seek to the start of the dictionary
#     f.seek(4)
#     # Read the binary data into a bytes object
#     data = f.read()
#     # Decode the binary data into a dictionary using pickle
#     decoded_dict = pickle.loads(data)
#
#     f.seek(0)
#     d = f.read()
#
# # Print the decoded dictionary
# print(decoded_dict)

def bin2hex(b):
    return hex(int(b, 2))[2::].zfill(2)

def inverse_bytes(string):
    l = len(string)
    a = [string[i:i+2] for i in range(0, l, 2)]
    return ''.join(a[::-1])

print(int(inverse_bytes("1fed0100"), 16))
print(int("0001ed1f"[::1], 16))