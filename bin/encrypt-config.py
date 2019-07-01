import pyAesCrypt
import getpass
# encryption/decryption buffer size - 64K
bufferSize = 64 * 1024
input_config_file = "..\configs\lic-analytics-configs.ini"
output_encrypted_config_file = "..\configs\lic-analytics-configs.aes"
# encrypt
print("---------------------------------------------------------------------")
print("**   ES SRE Configuration AES 256 format Encryption tool            **")
print("**   Currently Input/Output files hard coded for LIC Project   **")
print("----------------------------------------------------------------------")
print("--Going to Encrypt Input File:{0} and will be stored in Output file:{1}".format(input_config_file,output_encrypted_config_file))
password = input("Password:")
#password = getpass.getpass("Password:")

pyAesCrypt.encryptFile(input_config_file,output_encrypted_config_file, password, bufferSize)
print("** File Encrypted with AES 256 **")
