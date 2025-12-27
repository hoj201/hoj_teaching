from cryptography.fernet import Fernet

def encrypt_file(filename, key, output_filename=None):
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()
    
    encrypted_data = f.encrypt(file_data)
    
    if output_filename is None:
        output_filename = filename
    with open(output_filename, "wb") as file:
        file.write(encrypted_data)

def decrypt_file(filename, key, output_filename=None):
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    
    decrypted_data = f.decrypt(encrypted_data)
    if output_filename is None:
        output_filename = filename
    with open(output_filename, "wb") as file:
        file.write(decrypted_data)


def get_database(key: str, s3_client=None):
    bucket_name = "hoj-teaching"
    object_name = "contacts_encrypted.db"
    output_filename = "contacts.db"
    s3_client.download_file(bucket_name, object_name, object_name)
    decrypt_file(object_name, key, output_filename)
    return output_filename

def upload_database(filename: str, key: str, s3_client=None):
    bucket_name = "hoj-teaching"
    object_name = "contacts_encrypted.db"
    encrypted_filename = "contacts_encrypted.db"
    encrypt_file(filename, key, encrypted_filename)
    s3_client.upload_file(encrypted_filename, bucket_name, object_name)