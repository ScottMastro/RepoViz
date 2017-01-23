#!/bin/bash

# colors
YELLOW='\e[33m'
RED='\e[1;31m'
BLUE='\e[1;34m'
GREEN='\e[1;32m'
PURPLE='\e[1;35m'
NC='\e[0m'   # No Color

# get directory of this script
dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# unit tests
python "$dir/../WavMaker/test_synthesizer.py"   && \
python "$dir/../WavMaker/test_mixer.py"         && \
python "$dir/../WavMaker/test_parser.py"        && \
python "$dir/../WavMaker/test_WavMaker.py"      && \
python "$dir/../Analyzer/test_git_log.py"       && \
python "$dir/../Analyzer/test_word_counter.py"


#integration tests
python "$dir/../Analyzer/git_log.py"            && \
python "$dir/../Analyzer/word_counter.py" "5"

if [[ $? != 0 ]]; then
    exit
fi

if [[ ! -e "$dir/../Analyzer/commits.txt" ]]; then
    echo -e "\n${RED}Integration test failed$NC Analyzer failed to create commits.txt file\n"
    exit 1
fi

if [[ -e "$dir/../Narratives2_ESS2/Narratives2_ESS2/data/out.wav" ]]; then
    rm "$dir/../Narratives2_ESS2/Narratives2_ESS2/data/out.wav"
fi
if [[ -d "$dir/../Narratives2_ESS2/Narratives2_ESS2/data/tmp/" ]]; then
    rm -rf "$dir/../Narratives2_ESS2/Narratives2_ESS2/data/tmp"
fi

python "$dir/../WavMaker/WavMaker.py"

if [[ $? != 0 ]]; then
    exit
fi

if [[ ! -e "$dir/../Narratives2_ESS2/Narratives2_ESS2/data/out.wav" ]]; then
    echo -e "\n${RED}Integration test failed$NC WavMaker failed to create out.wav file\n"
    exit 1
fi

echo -e "\n    All tests ${GREEN}Passed$NC\n"
