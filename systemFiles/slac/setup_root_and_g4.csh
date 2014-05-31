
# Set up root 5.28 
setenv ROOTSYS /nfs/slac/g/exo/mgmarino/rhel6/root/5.28.00h
setenv PATH $ROOTSYS/bin:$PATH 
if ($?LD_LIBRARY_PATH) then
   setenv LD_LIBRARY_PATH ${ROOTSYS}/lib:${LD_LIBRARY_PATH}
else
   setenv LD_LIBRARY_PATH ${ROOTSYS}/lib
endif

if ($?PYTHONPATH) then
   setenv PYTHONPATH `root-config --libdir`:$PYTHONPATH
else
   setenv PYTHONPATH `root-config --libdir`
endif




# Set up MySQL (used by calibration system)
# Use version supplied by rhel5
#setenv MYSQL_HOME /afs/slac.stanford.edu/package/tww/prod/i386_linux26/TWWfsw/mysql5081r
#setenv PATH $MYSQL_HOME/bin:$PATH

# Set up Geant4/CLHEP
#source /afs/slac.stanford.edu/package/geant4/9.3.p02/env-rhel5-32.csh > /dev/null
source /afs/slac.stanford.edu/package/geant4/9.3.p02/env-rhel6-64.csh > /dev/null


