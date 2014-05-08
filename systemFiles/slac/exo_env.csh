
# pre-3/2014, per EXO confluence:
# https://confluence.slac.stanford.edu/x/gwIkBQ
source /nfs/slac/g/exo/software/builds/current/setup.csh

# to add exo fitting, 14 MAr 2014:
setenv LD_LIBRARY_PATH $EXOLIB/fitting/lib:$LD_LIBRARY_PATH


# 12 Mar 2014, per EXO https://confluence.slac.stanford.edu/x/gwIkBQ
# was not using this as of 12 Mar 2014, since default python is 2.7

setenv PYTHONPATH ${ROOTSYS}/lib
if ($?LD_LIBRARY_PATH) then
   setenv LD_LIBRARY_PATH /opt/TWWfsw/python25/lib/python2.5/config:${LD_LIBRARY_PATH}
else
  setenv LD_LIBRARY_PATH /opt/TWWfsw/python25/lib/python2.5/config
endif



