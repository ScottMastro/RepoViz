#!/bin/bash

# get directory of this script
srcDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# print usage if requested 
if [[ "$1" == "-help" || "$1" == "-h" ]]; then 
    echo -e "\n    Usage: ./run.sh <path_to_git_dir>\n"
    echo -e "    Where:\n"
    echo -e "    <path_to_git_dir>        is the path to where the .git file is (optional, default is ./)\n"
    exit
fi

function checkReturnValue {
    if [[ $1 != 0 ]]; then
        exit
    fi
}

# get number of topwords from config.txt
numWords=`awk '/number_words=/{split($0, spl,"="); print spl[2]}' $srcDir/config.txt`

# run the first git analyzer
python "$srcDir/Analyzer/git_log.py" $1
checkReturnValue $?

# run the second git analyzer
python "$srcDir/Analyzer/word_counter.py" $numWords
checkReturnValue $?

if [[ -e "$srcDir/Narratives2_ESS2/Narratives2_ESS2/data/out.wav" ]]; then
    rm "$srcDir/Narratives2_ESS2/Narratives2_ESS2/data/out.wav"
fi
if [[ -d "$srcDir/Narratives2_ESS2/Narratives2_ESS2/data/tmp/" ]]; then
    rm -rf "$srcDir/Narratives2_ESS2/Narratives2_ESS2/data/tmp"
fi

# make a wav file from the git data
python "$srcDir/WavMaker/WavMaker.py"
checkReturnValue $?

# run Narratives2 to play the wav file and show the visualization
if [[ -e "$srcDir/Narratives2_ESS2/Narratives2_ESS2/application.linux32/Narratives2_ESS2" ]]; then
    "$srcDir/Narratives2_ESS2/Narratives2_ESS2/application.linux32/Narratives2_ESS2"
elif [[ -e "$srcDir/Narratives2_ESS2/Narratives2_ESS2/application.linux64/Narratives2_ESS2" ]]; then
    "$srcDir/Narratives2_ESS2/Narratives2_ESS2/application.linux64/Narratives2_ESS2"
else
    echo "\nCould not find a linux executable for the Narratives visualizer\n"
fi
