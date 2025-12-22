from slowapi import Limiter
from slowapi.util import get_remote_address

# Identifies clients by IP address
limiter = Limiter(key_func=get_remote_address)
