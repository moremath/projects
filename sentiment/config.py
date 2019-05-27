#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


# 训练数据下载 https://github.com/tinySean/Fine-grained-user-commenting-emotions
data_path = os.path.abspath('.') + "/data"
train_data_path = data_path + "/train.csv"
model_path = os.path.abspath('.') + "/model/"


# 从美团爬取的json (可以调取api，也可以用无头浏览器翻页)
raw_comments_json = data_path + '/raw_comments.json'
