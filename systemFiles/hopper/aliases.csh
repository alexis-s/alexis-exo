
# source the generic csh aliases
source $HOME/alexis-exo/systemFiles/aliases.csh


alias myjobs 'qstat -u alexis3'

alias myjobs 'qstat | grep alexis ; echo "total:" ; qstat | grep alexis | wc -l ; echo "running" ; qstat | grep alexis | grep " R " | wc -l'

alias sourceroot 'source $ROOTSYS/bin/thisroot.csh'
alias loadroot 'setenv LD_LIBRARY_PATH $ROOTSYS/lib:${LD_LIBRARY_PATH}'

# https://www.nersc.gov/users/accounts/user-accounts/production-project-accounts/
alias loginexo200 'module load osg; myproxy-logon -s nerscca.nersc.gov; gsissh localhost -l exo200'
