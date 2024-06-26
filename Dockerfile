FROM ubuntu:24.04

RUN apt update

RUN apt install -y jq=1.7.1-3build1

RUN --mount=type=secret,id=root_data,required=true \
    export root_password_hash=$(jq -r ".password_hash" /run/secrets/root_data) && \
    usermod \
      --password=$root_password_hash \
      root

ARG userid

RUN --mount=type=secret,id=user_data,required=true \
    export user_name=$(jq -r ".user" /run/secrets/user_data) && \
    export user_password_hash=$(jq -r ".password_hash" /run/secrets/user_data) && \
    useradd \
      --create-home \
      --home-dir=/home/"$user_name" \
      --password="$user_password_hash" \
      --shell=/bin/bash \
      --uid=$userid \
      "$user_name"

ARG username

USER $username

WORKDIR /home/$username

ENTRYPOINT ["/bin/bash"]
