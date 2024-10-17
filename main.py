import json
import sys
import bencodepy


def decode_bencode(bencoded_value):
    bc = bencodepy.Bencode()
    return bc.decode(bencoded_value)

def main():
    command = sys.argv[1]

    if command == "decode":
        bencoded_value = sys.argv[2].encode()

        # json.dumps() can't handle bytes, but bencoded "strings" need to be
        # bytestrings since they might contain non utf-8 characters.
        #
        # Let's convert them to strings for printing to the console.
        def bytes_to_str(data):
            if isinstance(data, dict):
                return {bytes_to_str(k): bytes_to_str(v) for k, v in data.items()}
            elif isinstance(data, list):
                return [bytes_to_str(i) for i in data]
            elif isinstance(data, bytes):
                return data.decode(errors='replace')
            else:
                return data

        # Decode the bencoded value and print it as JSON
        print(json.dumps(bytes_to_str(decode_bencode(bencoded_value))))


    elif command == "info":
        file_name = sys.argv[2]
        with open(file_name, "r+b") as torrent_file:
            bencoded_content = torrent_file.read()

        try:
            # Check if the data starts with 'd' (dictionary) or 'l' (list)
            if not (bencoded_content.startswith(b'd') or bencoded_content.startswith(b'l')):
                raise ValueError("Invalid bencoded data structure.")

            torrent = decode_bencode(bencoded_content)
            print("Tracker URL:", torrent[b"announce"].decode())
            print("Length:", torrent[b"info"][b"length"])
            print("Name:", torrent[b"info"][b"name"])
        except Exception as e:
            print("Error decoding bencoded content:", e)


    else:
        raise NotImplementedError(f"Unknown command {command}")

if __name__ == "__main__":
    main()




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