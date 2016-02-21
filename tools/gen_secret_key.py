#!/usr/bin/python3.4

import random
import string as s


chars = '{}{}{}'.format(s.ascii_letters, s.digits, s.punctuation)
secret_key = ''.join([random.SystemRandom().choice(chars) for i in range(50)])

print(secret_key)
