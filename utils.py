import hashlib

# returns SHA-1 hash of a string
def hash_function(string):
	hash_object = hashlib.sha1(string)
	hex_digest = hash_object.hexdigest()

	return hex_digest