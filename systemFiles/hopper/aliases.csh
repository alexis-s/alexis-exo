
# source the generic csh aliases
source $HOME/alexis-exo/systemFiles/aliases.csh


alias myjobs 'qstat -u alexis3'

alias myjobs 'qstat | grep alexis ; echo "total:" ; qstat | grep alexis | wc -l ; echo "running" ; qstat | grep alexis | grep " R " | wc -l'
