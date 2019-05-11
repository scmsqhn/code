#!/bin/bash

echo $1
echo $2
echo $1 10000 nz>> $2.txt
tail $2.txt
