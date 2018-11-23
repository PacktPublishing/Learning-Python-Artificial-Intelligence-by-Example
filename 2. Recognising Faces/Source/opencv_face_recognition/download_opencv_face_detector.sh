#!/usr/bin/env bash

PROTO_TEXT="deploy.prototxt"
CAFFE_MODEL="res10_300x300_ssd_iter_140000_fp16.caffemodel"
OPEN_FACE_MODEL="nn4.small2.v1.t7"

if [ ! -f "./face_detector/${PROTO_TEXT}" ]; then
    wget https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt -P ./face_detector
fi
if [ ! -f "./face_detector/${CAFFE_MODEL}" ]; then
    wget https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20180205_fp16/res10_300x300_ssd_iter_140000_fp16.caffemodel -P ./face_detector
fi
if [ ! -f "./openface/${OPEN_FACE_MODEL}" ]; then
    wget https://storage.cmusatyalab.org/openface-models/nn4.small2.v1.t7 -P ./openface
fi
