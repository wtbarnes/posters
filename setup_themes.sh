#!/bin/bash
#Set up latex beamerposter style files in appropriate directories

#Usage:
# To create all symlinks
# $ ./setup_themes.sh /path/to/my/texmf/
# To clean up all symlinks
# $ ./setup_themes.sh /path/to/my/texmf/ clean

#Notes:
# This script is necessary because it is "good practice" to keep all .sty files in $TEXMFHOME/tex/latex rather than just link to local copies
# Running this script twice will fail because all of the symlinks already exist
# Run with the clean option to clean up all symlinks

#set texmf root from command line; include trailing slash
#directory structure should follow $TEXMFHOME/tex/latex/beamer/
TEXMFHOME=$1"tex/latex/beamer/beamerposter/"
#get path to latex-beamerposter (even if script not run inside this dir)
PATH2FILE=$(cd `dirname $0` && pwd)"/"
BEAMERPOSTERDIR=$PATH2FILE"latex-beamerposter/"

#check for existence of beamerposter directory
if ! [ -d "$TEXMFHOME" ]; then
  mkdir $TEXMFHOME
fi

#clean up symlinks
if [ "$2" == "clean" ]; then
  #remove beamerposter.sty link
  echo "Removing symlink to beamerposter.sty in ${TEXMFHOME}beamerposter.sty"
  rm $TEXMFHOME"beamerposter.sty"
  #remove all theme symlinks
  for theme in ${BEAMERPOSTERDIR}themes/*.sty; do
    THEME_NAME=$(basename $theme)
    echo "Removing symlink to ${THEME_NAME} in ${TEXMFHOME}${THEME_NAME}"
    rm ${TEXMFHOME}${THEME_NAME}
  done
  #exit with no errors
  exit 0
fi

#create symlink to beamerposter style file in TEXMFHOME
echo "Creating symlink to beamerposter.sty in ${TEXMFHOME}beamerposter.sty"
ln -s $BEAMERPOSTERDIR"beamerposter.sty" $TEXMFHOME"beamerposter.sty"

#create symlinks to all beamerposter themes in TEXMFHOME
for theme in ${BEAMERPOSTERDIR}themes/*.sty; do
  THEME_NAME=$(basename $theme)
  echo "Creating symlink to ${THEME_NAME} in ${TEXMFHOME}${THEME_NAME}"
  ln -s $theme ${TEXMFHOME}${THEME_NAME}
done
