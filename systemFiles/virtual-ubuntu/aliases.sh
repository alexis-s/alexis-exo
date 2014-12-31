

#--------------------------------------------------------------------
# general
#--------------------------------------------------------------------

alias top='top -o cpu' # order by cpu usage
alias mv='mv -i'
alias cp='cp -i'
#alias myjobs='qstat | grep alexis | wc -l'
alias myjobs='echo running:; showq | grep alexis | grep Running | wc -l; echo total:; showq | grep alexis | wc -l'

#alias pwd='echo $cwd'
#alias ls='ls -Gh'
#alias dir       'ls -alh'
#alias xterm     'xterm -geometry 200x60'
alias up='cd ..'
alias root='root -l'
alias screen='screen -l'
alias vir='vi -R' # read-only vi 
alias ls='ls -G'

alias remake='make clean; make'

