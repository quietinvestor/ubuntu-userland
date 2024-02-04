# Ubuntu Userland

## Table of Contents

1. [General](#1-general)
  * [Overview](#-overview)
  * [Why](#-why)
  * [How](#-how)
  * [Requirements](#-requirements)
  * [Download](#-download)
2. [Python](#2-python)
  * [Setup](#-setup)
  * [Script](#-script)
3. [Dockerfile](#3-dockerfile)
  * [Pre-requirements](#-pre-requirements)
  * [Build](#-build)

## 1. General

### &bull; Overview

A container base image, which builds on the Ubuntu base image, adding a:
1. custom non-root user; and
2. [yescrypt](https://www.openwall.com/yescrypt/)-hashed passwords for both the root and non-root user.

### &bull; Why?

Admittedly, anyone with access to your container runtime engine socket (e.g. using [docker](https://docs.docker.com/get-started/overview/) or [podman](https://docs.podman.io/en/latest/)) can log in directly into root or the non-root user without a password (Source: [How do I prevent root access to my docker container?](https://stackoverflow.com/questions/57731428/how-do-i-prevent-root-access-to-my-docker-container#answer-57732197)). Similarly, now you can use [rootless containers](https://developers.redhat.com/blog/2020/09/25/rootless-containers-with-podman-the-basics#why_rootless_containers_-h2) to make sure that if a threat actor manages to compromise the container runtime, engine or orchestrator, they will not gain root privileges on the underlying host.

Nonetheless, under certain scenarios, attackers can still try to gain shell access to a container from the outside by exploiting some documented or zero-day vulnerability. Thus, if you run your containerised application from user space or "userland" (hence the project's name), using a non-root user, the attacker faces yet another, albeit not unsurpassable, hurdle: a non-root user with no root access or privileges (the [sudo](https://www.sudo.ws/about/intro/) package is purposefully not installed) and a password-protected root user account. Likewise, the non-root user account is also password-protected in case the attacker compromised some other system account, thus further obstructing lateral movement.

### &bull; How?

As per the [standard in most Linux distributions nowadays](https://en.wikipedia.org/wiki/Yescrypt), all passwords are hashed in the `/etc/shadow` file using the yescrypt hashing algorithm and a 256-bit random salt.

For security and as per best practice, the user credentials are actually generated as a separate JSON file using the `user_data_json.py` Python script, which is then imported as a [secret-type mount](https://docs.docker.com/engine/reference/builder/#run---mounttypesecret) into the Dockerfile at the time that the container image is built. In contrast, using `ARG` or `ENV` could [expose the password](https://docs.docker.com/engine/reference/builder/#arg) during the container image build process.

### &bull; Requirements

- [Download](https://git-scm.com/downloads) and [install](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) git.
- [Download](https://www.python.org/downloads/) and install Python, if it is not already included in your Operating System (OS).
- Download and install your preferred container runtime engine:
  * [docker](https://docs.docker.com/engine/install/); or
  * [podman](https://podman.io/docs/installation)

### &bull; Download

To download all the required files, input the below commands from the command line:

```
https://github.com/quietinvestor/ubuntu-userland.git
```

## 2. Python

### &bull; Setup

Assuming that you are using a python [virtual environment](https://docs.python.org/3/tutorial/venv.html) locally within the `do-tf-pg-backend` directory, you can simply install the package dependencies using the pip `requirements.txt` file.
```
python -m venv .venv
source .venv/bin/activate
python -m pip install -r scripts/python/requirements.txt
```

### &bull; Script

The `user_data_json.py` script automates the generation of a JSON object, containing the username and password to then pass a secret-type mount to the Dockerfile at container image build time.
```
$ python user_data_json.py --help

usage: user_data_json.py [-h] -p PASSWORD -u USERNAME

options:
  -h, --help            show this help message and exit
  -p PASSWORD, --password PASSWORD
                        Password
  -u USERNAME, --username USERNAME
                        Username
```
For example, for a user `dev` with a password `test`, the JSON output (prettified for illustration) would look as follows:
```
$ python user_data_json.py -u dev -p test

{
  "user": "dev",
  "password_hash": "$y$jD5$vLoZyxfIM6vVbnW1R3mJXOkNrkN1K7OIjV3Mwqld75A$ArLmE/wgyUXJVMDHMFiOhO4.hmYaD1QdOwmgTlR4asB"
}
```
Please note that, given that a random 256-bit salt is used to generate the yescrypt password hash, it will be different for the same password each time that the script is run.

## 3. Dockerfile

### &bull; Pre-requirements

Prior to building the container image, two JSON object files with the root and non-root user credentials need to be generated to then reference these as secret-type mount sources at build time.
```
$ python user_data_json.py -u root -p rootpassword > root_data.json
$ python user_data_json.py -u dev -p devpassword > user_data.json
```

### &bull; Build

Once the required user credential JSON object files have been generated, building the image from the Dockerfile present within the downloaded repository directory is as simple as:
```
$ docker image build --secret id=root_data,src=root_data.json --secret id=user_data,src=user_data.json -t ubuntu-userland:1.0.0 .
```
Please note that:
* You can just replace `docker` with `podman` if you use the latter.
* The above command assumes that you generated both JSON object files within the same directory. Otherwise, please amend the `src=` path accordingly.
