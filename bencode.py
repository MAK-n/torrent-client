import bencodepy

def decode_bencode(bencoded_value):
    bc = bencodepy.Bencode()
    return bc.decode(bencoded_value)

def encode_bencode(data):
    bc = bencodepy.Bencode()
    return bc.encode(data)

### GAVE UP ###
# def decode_bencode(bencoded_value):
#     # Handling a string (length-prefixed)
#     if bencoded_value[0:1].isdigit():
#         first_colon_index = bencoded_value.find(b":")
#         if first_colon_index == -1:
#             raise ValueError("Invalid encoded value: No colon found.")
#         length = int(bencoded_value[:first_colon_index])
#         return bencoded_value[first_colon_index + 1:first_colon_index + 1 + length]

#     # Handling an integer (i<value>e)
#     elif bencoded_value[0:1] == b"i" and bencoded_value[-1:] == b"e":
#         return int(bencoded_value[1:-1])

#     # Handling a list (l<list content>e)
#     elif bencoded_value[0:1] == b"l" and bencoded_value[-1:] == b"e":
#         bencoded_list_as_string = bencoded_value[1:-1]
#         bencoded_list = []
#         i = 0
#         while i < len(bencoded_list_as_string):
#             char = bencoded_list_as_string[i:i + 1]

#             # For Integer (handled by checking for "i" at the start)
#             if char == b"i":
#                 end_index = bencoded_list_as_string.find(b"e", i)
#                 if end_index == -1:
#                     raise ValueError("Invalid integer format: missing 'e'.")
#                 bencoded_list.append(decode_bencode(bencoded_list_as_string[i:end_index + 1]))
#                 i = end_index + 1

#             # For String (length-prefixed strings)
#             elif char.isdigit():
#                 first_colon_index = bencoded_list_as_string.find(b":", i)
#                 if first_colon_index == -1:
#                     raise ValueError("Invalid string format: missing colon.")
#                 length = int(bencoded_list_as_string[i:first_colon_index])  # Get the length of the string
#                 bencoded_list.append(bencoded_list_as_string[first_colon_index + 1:first_colon_index + 1 + length].decode())  # Extract and decode the string
#                 i = first_colon_index + 1 + length

#             # For List (recursive parsing for nested lists)
#             elif char == b"l":
#                 # We need to handle nested lists correctly by identifying the corresponding closing "e"
#                 nested_list_end = i
#                 balance = 1  # We already found the opening 'l'
#                 while balance > 0:
#                     nested_list_end += 1
#                     if bencoded_list_as_string[nested_list_end:nested_list_end + 1] == b"l":
#                         balance += 1
#                     elif bencoded_list_as_string[nested_list_end:nested_list_end + 1] == b"e":
#                         balance -= 1
                
#                 # Decode the nested list
#                 bencoded_list.append(decode_bencode(bencoded_list_as_string[i:nested_list_end + 1]))
#                 i = nested_list_end + 1

#             # Handle unexpected characters
#             else:
#                 raise ValueError(f"Unexpected character {char} while decoding list.")

#         return bencoded_list

#     # Handle unsupported types
#     else:
#         raise NotImplementedError("Only strings, integers, and lists are supported at the moment")