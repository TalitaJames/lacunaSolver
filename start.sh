#!/bin/bash
fileNameDate=$(date +%Y%m%d-%H%M%S)

python3 src/main.py |& tee ./out/logs/$fileNameDate.log