import argparse
import json
import pyescrypt
import secrets

def shadow_password_hash(password):

    salt_bytes = secrets.token_bytes(32)
    password_bytes = str.encode(password)

    hasher = pyescrypt.Yescrypt(n=2 ** 16, r=8, p=1, mode=pyescrypt.Mode.MCF)
    hashed = hasher.digest(password_bytes,salt_bytes)

    return hashed.decode("utf-8")


def user_data_json(username, password):

    user_data = {
        "user": username,
        "password_hash": shadow_password_hash(password)
    }

    user_data_json = json.dumps(user_data)

    return user_data_json


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    arg_opt_list = [
        [ ["-p", "--password"], { 'help': "Password", 'required': True } ],
        [ ["-u", "--username"], { 'help': "Username", 'required': True } ]
    ]

    for arg_opt in arg_opt_list:
        optional_arg_list = arg_opt[0]
        positional_arg_dict = arg_opt[1]

        parser.add_argument(*optional_arg_list, **positional_arg_dict)

    args = parser.parse_args()

    user_data = user_data_json(args.username, args.password)
    print(user_data)
