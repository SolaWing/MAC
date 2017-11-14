#!/bin/bash

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
        # d12frosted/emacs-plus/emacs-plus --without-librsvg --without-imagemagick@6
        laurent22/massren/massren
        tmux
        httpie

        mitmproxy
        node
        pngquant
        carthage
    )

    other_packages=(
        '--HEAD universal-ctags/universal-ctags/universal-ctags'
        '--HEAD d12frosted/emacs-plus/emacs-plus --without-librsvg --without-imagemagick@6'
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

if (($#==0)); then
    echo 'use `'$0' install` to install brew packages'
elif [[ $1 == install ]]; then
    install_brew
    install_brew_app
fi
