import hashlib

message = "Nguyễn Văn Hồng Phong"

hash_value = hashlib.sha256(message.encode("utf-8")).hexdigest()

print("SHA-256 Hash")
print("Message =", message)
print("Hash =", hash_value)