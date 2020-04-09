#!/bin/bash
# 这种install会缺乏维护，然后就没人用啊。应该是作为更新源头或者从现有环境中导出的迁移脚本。

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
        ripgrep
        fd
        clang-format
        laurent22/massren/massren # file rename util
        tmux
        httpie
        graphviz

        mitmproxy
        node
        pngquant
        carthage
    )

    other_packages=(
        '--HEAD universal-ctags/universal-ctags/universal-ctags'
        # '--HEAD d12frosted/emacs-plus/emacs-plus --without-librsvg --without-imagemagick@6'
    )

    set -x # log command
    # print_args "${packages[@]}"
    brew install "${packages[@]}"
    for p in "${other_packages[@]}"; do
        # print_args $p
        brew install $p
    done
}

function install_brew_app () {
    apps=(
        bitbar macvim firefox gitup hammerspoon
    )
    brew cask install "${apps[@]}"
}

function install_pip3 () {
    packages=(
        pip setuptools
        neovim
        ipython
        virtualenv
        # vprof # visual profile packages
    )
    pip3 install -U "${packages[@]}"
}

function link_file () {
    bash "$DIR"linker.sh link
}

function install_rbenv_gems () {
    gem install gem-ctags yard
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
    install_rbenv_gems
    '
else
    for i; do
        "$i"
    done
fi
