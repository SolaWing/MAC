# https://github.com/fish-shell/fish-shell/issues/828
function ...
    cd ../..
end
function ....
    cd ../../..
end
function l --wraps 'ls -Ah'
    ls -Ah $argv
end
function ll --wraps 'ls -lh'
	ls -lh $argv
end
function la --wraps 'ls -lAh'
	ls -lAh $argv
end
function md --wraps 'mkdir -p'
	mkdir -p $argv
end
function mtab --wraps 'open -b org.vim.MacVim'
	open -b org.vim.MacVim $argv
end
function py --wraps 'python'
	python $argv
end
function py3 --wraps 'python3'
	python3 $argv
end
function b --wraps 'bundle exec'
    bundle exec $argv
end
function vim --wraps 'mvim'
	mvim $argv
end
function bvim --wraps 'nvim -b --noplugin'
	nvim -b --noplugin $argv
end
function v --wraps 'nvim'
	nvim $argv
end
function o --wraps 'open'
	open $argv
end
function tp --wraps '/Applications/TexturePacker.app/Contents/MacOS/TexturePacker'
	/Applications/TexturePacker.app/Contents/MacOS/TexturePacker $argv
end
function em --wraps 'open -a Emacs'
	open -a Emacs $argv
end
function pause --wraps 'kill -s SIGSTOP'
	kill -s SIGSTOP $argv
end
function resume --wraps 'kill -s SIGCONT'
	kill -s SIGCONT $argv
end

# git alias
function ga --wraps 'git add'
	git add $argv
end
function gbr --wraps 'git branch -vv'
	git branch -vv $argv
end
function gc --wraps 'git commit'
	git commit $argv
end
function gca --wraps 'git commit -a'
	git commit -a $argv
end
function gcm --wraps 'git commit --amend --no-edit'
	git commit --amend --no-edit $argv
end
function gcam --wraps 'git commit -a --amend --no-edit'
	git commit -a --amend --no-edit $argv
end
function gco --wraps 'git checkout'
	git checkout $argv
end
function gdt --wraps 'git difftool'
	git difftool $argv
end
function gdtm --wraps 'git difftool --diff-filter=MTU'
	git difftool --diff-filter=MTU $argv
end
function gd --wraps 'git diff'
	git diff $argv
end
function gf --wraps 'git fetch'
	git fetch $argv
end
function gp --wraps 'git pull'
	git pull $argv
end
function gpr --wraps 'git pull --rebase'
	git pull --rebase $argv
end
function gl --wraps 'git log'
	git log $argv
end
function gll --wraps 'git ls-files'
	git ls-files $argv
end
function glo --wraps 'git log --graph --oneline'
	git log --graph --oneline $argv
end
function gls --wraps 'git log --stat'
	git log --stat $argv
end
function gldel --wraps 'git log --diff-filter=D --summary'
	git log --diff-filter=D --summary $argv
end
function gm --wraps 'git merge'
	git merge $argv
end
function gmt --wraps 'git mergetool'
	git mergetool $argv
end
function gs --wraps 'git status'
	git status $argv
end
function gsub --wraps 'git submodule'
	git submodule $argv
end
function gsubu --wraps 'git submodule update --init --recursive'
	git submodule update --init --recursive $argv
end
function greset --wraps 'git reset'
	git reset $argv
end
function grebase --wraps 'git rebase'
	git rebase $argv
end
function gstash --wraps 'git stash'
	git stash $argv
end

function trm --wraps '/bin/rm'
	/bin/rm $argv
end

function rm --wraps /bin/rm
    if contains -- -f $argv
        /bin/rm $argv
    else
        python ~/bin/trash.py $argv
    end
end
