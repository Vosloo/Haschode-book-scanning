#!/bin/bash

echo "Compiling tester.cpp"
g++ -Wall -o main.exe tester.cpp
echo "Done"

echo "Running computations"
python ./scanner.py
echo "Done"

echo -e "Running checks\n"
for filename in ./data/*.txt; do
    echo $filename

    ./main.exe "$filename" "solutions/$(basename "$filename" .txt).txt"; 

    echo
done
echo "Done"