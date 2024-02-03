import json
import pyescrypt
import sys
import unittest

sys.path.append("../../scripts/python")

import user_data_json

class TestShadowPasswordHash(unittest.TestCase):

    def test_salt_len(self):
        # 32-byte salt = 256 bits
        len_test = 32
        salt = user_data_json.salt_bytes(len_test)
        self.assertEqual(len(salt), len_test)

    def test_password(self):
        password = "test"
        # 32-byte salt = 256 bits
        salt = b'S|\xfdR\xfb/\xe5&\x0f\xc2\xf8B\xb6\xe6s\x02\xd2\xb1\xc3L\x10W\x05Y\xe4\x19\x15\xaa9\x86n\xa1'
        password_hash_test = '$y$jD5$HlLzGhz9ZPm10XjEqOyQ06Rg1n22LJEKYbF3eaXVi38$KS9zMYvWlHjwtbXHwpG9wANYvxQi3GSrZV1.km3zfs8'
        password_hash_output = user_data_json.shadow_password_hash(salt, password)
        self.assertEqual(password_hash_output, password_hash_test)

    def test_user_data_json(self):
        password = "test"
        # 32-byte salt = 256 bits
        salt = b'\xa5\xc1\x16\xf5u\xaeC\n=n\xa7}a\x13\xdd\xc6\xc0\xeb\xbe\x84\x84D\xb9\nt\x85G\xc0\xaa2\x89\x1a'
        user_name = "test"
        user_data_dict = {
            "user": "test",
            "password_hash": "$y$jD5$Z4g3pLbf1dEDiROTVBFr41wuyG6V2Zf0oJsF.feA7e/$fc0TnbPpJ3zCxR1D6Xe6aW1T9lfFWl8J5vEWenkldQB"
        }
        user_data_test = json.dumps(user_data_dict)
        user_data_output = user_data_json.user_data_json(user_name, salt, password)
        self.assertEqual(user_data_output, user_data_test)

if __name__ == '__main__':
    unittest.main()
