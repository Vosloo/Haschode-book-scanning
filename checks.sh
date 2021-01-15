#!/bin/bash

python ./genetic.py
echo

for filename in ./data/*.txt; do
    #if [[ $filename == "./data/d_tough_choices.txt" ]]; then 
    #    continue; 
    #fi; 

    echo $filename

    ./main.exe "$filename" "solutions/$(basename "$filename" .txt).txt"; 

    echo
done