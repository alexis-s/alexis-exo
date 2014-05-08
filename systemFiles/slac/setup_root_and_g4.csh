
# Set up root 5.28 
setenv ROOTSYS /afs/slac.stanford.edu/package/cernroot/vol35/52800svn/Linux26SL5_i386_gcc412
setenv PATH $ROOTSYS/bin:$PATH 
if ($?LD_LIBRARY_PATH) then
   setenv LD_LIBRARY_PATH ${ROOTSYS}/lib:${LD_LIBRARY_PATH}
else
   setenv LD_LIBRARY_PATH ${ROOTSYS}/lib
endif

# Set up MySQL (used by calibration system)
# Use version supplied by rhel5
#setenv MYSQL_HOME /afs/slac.stanford.edu/package/tww/prod/i386_linux26/TWWfsw/mysql5081r
#setenv PATH $MYSQL_HOME/bin:$PATH

# Set up Geant4/CLHEP
source /afs/slac.stanford.edu/package/geant4/9.3.p02/env-rhel5-32.csh > /dev/null


