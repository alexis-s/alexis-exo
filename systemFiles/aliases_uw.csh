# @(#)Cshrc 1.3 88/02/08 SMI
# aliases for all shells


#--------------------------------------------------------------------
# general
#--------------------------------------------------------------------

alias cp        'cp -i'
alias mv        'mv -i'
alias pwd       'echo $cwd'
alias ls	'ls -Gh'
#alias dir       'ls -alh'
#alias xterm     'xterm -geometry 200x60'
alias up 	'cd ..'
alias root      'root -l'
alias screen    'screen -l'
alias gdb       'gdb -silent'
alias top       'top -o cpu' # order by cpu usage
#alias vi        'vim -s ~/.virc'
alias vir       'vi -R' # read-only vi 

alias mgdo 'cd $MGDODIR'
#alias dawn 'dawn -d' # batch mode

# aliases from jason?:
#alias ls	'ls --color'
#alias findf     'find . -name'
#alias top       'top -d 1'
alias remake    'make clean; make'
alias remake2    'make clean; make -j2; make'
#alias rsupd     'rsync -e ssh -avu'
#alias rsupdz    'rsync -e ssh -avuz'

#alias rsync      'rsync -azh --exclude='.*.swp' --progress'
#alias rsync      'rsync -azhv --progress'
#alias rsync      'rsync -azh'

alias pdflatex    'pdflatex -halt-on-error'
alias mage 'cd ${MAGEDIR}'

alias rmtextempfiles 'rm *.aux *.log *.out *.bbl *.blg *.lot *.lof *.toc *.brf'

alias todo      'cat ~/ewi/todo/todo.txt'

