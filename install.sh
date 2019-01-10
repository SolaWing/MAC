#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles
function print_args () {
    echo count is $#
    for i in "$@"; do
        echo $i;
    done
}

function install_brew () {
    packages=(
        python3
        fzf
        fish
        neovim
        the_silver_searcher
        ripgrep
        fd
        clang-format
        laurent22/massren/massren # file rename util
        tmux
        httpie

        mitmproxy
        node
        pngquant
        carthage
    )

    other_packages=(
        '--HEAD universal-ctags/universal-ctags/universal-ctags'
        # '--HEAD d12frosted/emacs-plus/emacs-plus --without-librsvg --without-imagemagick@6'
    )

    set -x
    # print_args "${packages[@]}"
    brew install "${packages[@]}"
    for p in "${other_packages[@]}"; do
        # print_args $p
        brew install $p
    done
}

function install_brew_app () {
    brew cask install bitbar macvim
}

function install_pip3 () {
    packages=(
        pip setuptools
        neovim ipython
        virtualenv
        vprof # visual profile packages
    )
    pip3 install -U "${packages[@]}"
}

function link_file () {
    bash "$DIR"linker.sh link
}

function install () {
    install_brew
    install_brew_app
    install_pip3
    link_file
}

if (($#==0)); then
    echo 'optional cmd is
    install -- install all
    install_brew
    install_brew_app
    install_pip3
    link_file
    '
else
    for i; do
        "$i"
    done
fi
