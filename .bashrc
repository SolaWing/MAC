echo "load bash_rc"
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm

if [[ -f ~/.bash_profile ]]; then
  . ~/.bash_profile
fi
alias pc_log="rdt xl -om"
alias ios_log="rdt xl -o"
alias pc_log="rdt xl -om"
alias ios_log="rdt xl -o"

[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
