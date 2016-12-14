#!/usr/bin/en sh
rm -rf img_train_lmdb
../../caffe/build/tools/convert_imageset --gray \
--resize_height=28 --resize_width=28 \
/home/gzr/np2016/Caffe train.txt img_train_lmdb
