FROM ubuntu:22.04

RUN apt update

RUN apt install -y jq=1.6-2.1ubuntu3

RUN --mount=type=secret,id=root_data,required=true \
    export root_password_hash=$(jq -r ".password_hash" /run/secrets/root_data) && \
    usermod \
      --password=$root_password_hash \
      root

RUN --mount=type=secret,id=user_data,required=true \
    export user_name=$(jq -r ".user" /run/secrets/user_data) && \
    export user_password_hash=$(jq -r ".password_hash" /run/secrets/user_data) && \
    useradd \
      --create-home \
      --home-dir=/home/"$user_name" \
      --password="$user_password_hash" \
      --shell=/bin/bash \
      --uid=1001 \
      "$user_name"

USER 1001

WORKDIR $HOME

#RUN apt install -y cmake curl file gettext git ninja-build unzip && \
#    git clone https://github.com/neovim/neovim && \
#    cd neovim && \
#    git checkout v0.9.5 && \
#    make CMAKE_BUILD_TYPE=Release && \
#    cd build && \
#    cpack -G DEB && \
#    dpkg -i nvim-linux64.deb

ENTRYPOINT ["/bin/bash"]