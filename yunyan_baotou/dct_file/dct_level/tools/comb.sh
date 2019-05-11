#!/bin/bash

cat ../*.txt > comb.txt | sort | uniq > comb_sort.txt
