import os
import sys
import base64
import random
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import mimetypes

# random key for AES encryption
KEY = os.urandom(16)

#  to encrypt file data
def encrypt_data(data):
    cipher = AES.new(KEY, AES.MODE_CBC, iv=KEY)
    encrypted = cipher.encrypt(pad(data, AES.block_size))
    return encrypted

# Detect file type
def detect_file_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type:
        if "application/x-msdownload" in mime_type:
            return "exe"
        elif "text/x-python" in mime_type:
            return "python"
        elif "text/plain" in mime_type:
            return "text"
        elif "application/pdf" in mime_type:
            return "pdf"
        elif "application/msword" in mime_type or "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return "docx"
        else:
            return "binary"
    return "unknown"

#  obfuscation function
def obfuscate_file(input_file):
    if not os.path.exists(input_file):
        print(f"[!] File '{input_file}' not found.")
        return
    
    file_type = detect_file_type(input_file)
    print(f"[+] Detected file type: {file_type}")

    with open(input_file, "rb") as f:
        file_data = f.read()
    
    encrypted_data = encrypt_data(file_data)
    encoded_data = base64.b64encode(encrypted_data).decode()

    # Generate obfuscated output
    obfuscated_script = f"""
import base64
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# AES decryption key
KEY = {KEY}

# Encrypted and base64-encoded data
ENCODED_DATA = "{encoded_data}"

# Decrypt function
def decrypt_data():
    encrypted = base64.b64decode(ENCODED_DATA)
    cipher = AES.new(KEY, AES.MODE_CBC, iv=KEY)
    return unpad(cipher.decrypt(encrypted), AES.block_size)

# Detect file type
file_type = "{file_type}"

# Define temporary file before printing
temp_file = "decrypted_output"

if file_type == "exe":
    temp_file += ".exe"
elif file_type == "python":
    temp_file += ".py"
elif file_type == "text":
    temp_file += ".txt"
elif file_type == "pdf":
    temp_file += ".pdf"
elif file_type == "docx":
    temp_file += ".docx"
else:
    temp_file += ".bin"

print(f"[+] Decrypted file will be saved as: {{temp_file}}")

def execute_decrypted():
    decrypted_data = decrypt_data()

    with open(temp_file, "wb") as f:
        f.write(decrypted_data)

    print(f"[+] Decrypted file saved as: {{temp_file}}")

    # Open or execute the decrypted file based on type
    if file_type == "exe":
        os.system(temp_file)
    elif file_type == "python":
        os.system(f"python {{temp_file}}")
    elif file_type in ["text", "pdf", "docx"]:
        os.startfile(temp_file)
    else:
        print("[!] File is decrypted but must be handled manually.")

# Run decryption and execution
execute_decrypted()
"""
    
    with open("obfuscated_output.py", "w") as f:
        f.write(obfuscated_script)

    print("[+] Obfuscation complete! Generated 'obfuscated_output.py'.")

# CLI Handling
if len(sys.argv) != 3 or sys.argv[1] != "--file":
    print("Usage: python obfuscator.py --file <filename>")
else:
    obfuscate_file(sys.argv[2])
