# short code generator

import random
import string

def generate_short_code(length=6):
    # It creates a pool of all letters a-z and A-Z and digits 0-9
    chars = string.ascii_letters + string.digits 
    # It randomly selects characters of length 6 and joins to form a single string
    return ''.join(random.choices(chars, k=length))