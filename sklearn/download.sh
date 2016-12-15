#!/bin/bash

FILE=data.csv
URL=http://home.ustc.edu.cn/~xxuan/$FILE

echo "Downloading data.csv..."
wget $URL -O $FILE
echo "Done."