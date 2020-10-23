set DIR (dirname (status -f))

# Add RBENV init hook
status --is-interactive; and source (rbenv init -|psub)
set -xg PATH ~/.cargo/bin $PATH

set -xg EDITOR  'nvim'
set -xg LANG  'zh_CN.UTF-8'
set -xg CLICOLOR  1
set -xg GREP_OPTIONS  '--color=auto --exclude-dir=.cvs --exclude-dir=.git --exclude-dir=.hg --exclude-dir=.svn'
set -xg GREP_COLOR  '1;32'
set -xg HISTCONTROL  ignoreboth:erasedups		# for 'ignoreboth': ignore duplicates and /^\s/
set -xg HISTSIZE  9999
set -xg JAVA_HOME  "/System/Library/Java/JavaVirtualMachines/1.6.0.jdk/Contents/Home"
set -xg FZF_DEFAULT_OPTS ' --bind="alt-j:down,alt-k:up,alt-h:backward-char,alt-l:forward-char,alt-space:jump,`:jump-accept" --color="pointer:15"'
# --exact'
set -xg MANPAGER 'nvim +Man!'
set -xg HOMEBREW_NO_AUTO_UPDATE 1
set -xg USER_ID '6572338443358044419'

# set -xg RUBYOPT '--jit -W:no-deprecated -W:no-experimental'
# set -xg CP_CACHE_DIR $HOME/Library/Caches/CocoaPods/1.8.4

function fish_prompt
    set_color green
    echo -n (count (jobs -p))":"(basename (pwd))' $ '
    set_color normal
end

function fish_title
    basename (pwd)
end

# set -xg fish_user_abbreviations # prevent save abbreviations
source $DIR/alias.fish

