function ...
    cd ../..
end
function ....
    cd ../../..
end
function l
    ls -Ah $argv
end
function ll
	ls -lh $argv
end
function la
	ls -lAh $argv
end
function fd
	find . -type d -name $argv
end
function ff
	find . -type f -name $argv
end
function f
	find $argv
end
function md
	mkdir $argv
end
function mtab
	open -b org.vim.MacVim $argv
end
function py
	python $argv
end
function py3
	python3 $argv
end
function vim
	mvim $argv
end
function bvim
	nvim -b --noplugin $argv
end
function map
	xargs -n1 $argv
end
function v
	nvim $argv
end
function o
	open $argv
end
function tp
	/Applications/TexturePacker.app/Contents/MacOS/TexturePacker $argv
end
function em
	open -a Emacs $argv
end
function pause
	kill -s SIGSTOP $argv
end
function resume
	kill -s SIGCONT $argv
end

# git alias
function ga
	git add $argv
end
function gbr
	git branch $argv
end
function gc
	git commit $argv
end
function gca
	git commit -a $argv
end
function gcm
	git commit --amend -C head $argv
end
function gcam
	git commit -a --amend -C head $argv
end
function gco
	git checkout $argv
end
function gdt
	git difftool $argv
end
function gdtm
	git difftool --diff-filter=MTU $argv
end
function gd
	git diff $argv
end
function gf
	git fetch $argv
end
function gp
	git pull $argv
end
function gpr
	git pull --rebase $argv
end
function gl
	git log $argv
end
function gll
	git ls-files $argv
end
function glo
	git log --graph --oneline $argv
end
function gls
	git log --stat $argv
end
function gldel
	git log --diff-filter=D --summary $argv
end
function gm
	git merge $argv
end
function gmt
	git mergetool $argv
end
function gs
	git status $argv
end
function gsub
	git submodule $argv
end
function gsubu
	git submodule update --init --recursive $argv
end
function greset
	git reset $argv
end
function grebase
	git rebase $argv
end
function gstash
	git stash $argv
end
function trm
	/bin/rm $argv
end

function rm
    if contains -- -f $argv
        /bin/rm $argv
    else
        mv $argv ~/.Trash
    end
end
