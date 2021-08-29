#!/bin/sh
DATASET="larusso94/shark-species"
DATA_DIR="data"

if [ -d ${DATA_DIR} ]; then
  echo ${DATA_DIR}' exists, please remove it before running the script'
  exit 1
fi

mkdir -p ${DATA_DIR} && \
kaggle datasets download -d ${DATASET} && \
unzip -q archive.zip && \
