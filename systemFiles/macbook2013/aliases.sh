
# copied from cenpa-rocks 07 Feb 2013 -- AGS



#-------------------------------------------------------------------------------
# SSH

alias ssh_corn='ssh -Y alexis4@corn.stanford.edu'

alias sync_farmShare='rsync -avzh -e 'ssh' --progress alexis4@corn.stanford.edu:~/bucket/farmShare ~/bucket'


#-------------------------------------------------------------------------------
# EXO
#-------------------------------------------------------------------------------



#--------------------------------------------------------------------
# general
#--------------------------------------------------------------------

alias startVirtualUbuntu='VBoxHeadless -s ubuntu_14_04_1_LTS &'

alias runbkgmodel='qsub ~/malbekWork/bkgSpectrumPrediction/predictionByContaminant/runItAll.csh'
alias tailbkgmodel='tail -f -n 200 ~/malbekWork/bkgSpectrumPrediction/predictionByContaminant/logFiles/malbekPredictionContaminants.out | grep " component"'

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

alias rmtexfiles='rm *.aux *.log *.out *.toc'

# elog
alias startupELOG='$SOFTWAREDIR/elog/elogd -p 8080 -c $SOFTWAREDIR/elog/elogd.cfg -D'
alias restartELOG='killall elogd; startupELOG'

alias truecrypt='/Applications/TrueCrypt.app/Contents/MacOS/Truecrypt --text'

alias launchSecondDropbox='HOME=$HOME/stanford-Dropbox; /Applications/Dropbox.app/Contents/MacOS/Dropbox &'

alias canopyPython='/Users/alexis/Library/Enthought/Canopy_64bit/User/bin/pythonw'

