import hmac
import hashlib
def generate_mac(secret_key, message):
    secret_key_bytes = bytes(secret_key, 'utf-8')
    message_bytes = bytes(message, 'utf-8')
    mac = hmac.new(secret_key_bytes, message_bytes, hashlib.sha256).hexdigest()
    return mac

if __name__ == "__main__":
    secret_key = "my_secret_key"
    message=input("Please Enter your Message!:")
    mac = generate_mac(secret_key, message)
    print("Message:",message)
    print("mac:",mac)
