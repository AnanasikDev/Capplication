import pickle
import struct

# Create a dictionary to encode
my_dict = {'name': 'John', 'age': 30, 'city': 'New York'}

# Encode the dictionary into a file
with open('my_dict.pickle', 'wb') as f:
    f.write(struct.pack('<4s', bytes.fromhex('CAFEFADE')))

with open('my_dict.pickle', 'ab') as f:
    pickle.dump(my_dict, f)

# Decode the dictionary from the file
with open('my_dict.pickle', 'rb') as f:
    # Seek to the start of the dictionary
    f.seek(4)
    # Read the binary data into a bytes object
    data = f.read()
    # Decode the binary data into a dictionary using pickle
    decoded_dict = pickle.loads(data)

with open('my_dict.pickle', 'ab') as f:
    for i in range(100):
        f.write(b'a0')

# Print the decoded dictionary
print(decoded_dict)