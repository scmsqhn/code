#!/bin/bash

cd ../../dockerfile/
pwd -P
docker build -t python:3.6 .
