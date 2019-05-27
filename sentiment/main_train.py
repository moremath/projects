#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import config
import logging
import os

import numpy as np

from skift import FirstColFtClassifier
from sklearn.externals import joblib
from util import load_data_from_csv, seg_words


# 这个logging可以简化，不用GPU跑的话，processName和threadName无需标记
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] <%(processName)s> (%(threadName)s) %(message)s')
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    # 完全可以封装成main函数，放在函数参数中；argparse是出于命令行参数的风格
    parser = argparse.ArgumentParser()
    parser.add_argument('-mn', '--model_name', type=str, nargs='?',
                        default='fasttext_model.pkl',
                        help='the name of model')
    parser.add_argument('-lr', '--learning_rate', type=float, nargs='?',
                        default=1.0)
    parser.add_argument('-ep', '--epoch', type=int, nargs='?',
                        default=10)
    parser.add_argument('-wn', '--word_ngrams', type=int, nargs='?',
                        default=1)
    parser.add_argument('-mc', '--min_count', type=int, nargs='?',
                        default=1)

    args = parser.parse_args()
    model_name = args.model_name
    learning_rate = args.learning_rate
    epoch = args.epoch
    word_ngrams = args.word_ngrams
    min_count = args.min_count

    # 加载模型
    logger.info("start load load...")
    train_data_df = load_data_from_csv(config.train_data_path)
    # iloc 是整数索引 ，[:, 1]取的索引1，csv第二列的评论
    content_train = train_data_df.iloc[:, 1]

    logger.info("start seg train data...")
    content_train = seg_words(content_train)
    logger.info("complete seg train data")

    logger.info("prepare train format...")
    # 从1 x n ---> n x 1的转秩 
    train_data_format = np.asarray([content_train]).T
    logger.info("complete formate train data")
    #表头
    columns = train_data_df.columns.values.tolist()

    # 训练模型
    logger.info("start train model")
    classifier_dict = dict()
    # 0,1是id,content,label从索引2开始
    for column in columns[2:]:
        train_label = train_data_df[column]
        logger.info("start train %s model" % column)
        # 为了使用fasttext的sklearn的分类器 调参是套路，不必深究
        sk_clf = FirstColFtClassifier(
            lr=learning_rate, 
            epoch=epoch,
            wordNgrams=word_ngrams,
            minCount=min_count,
            verbose=2,
            )
        sk_clf.fit(train_data_format, train_label)
        logger.info("complete train %s model" % column)
        classifier_dict[column] = sk_clf
    logger.info("complete train model")
    
    #保存模型
    logger.info("start save model...")
    model_path = config.model_path
    if not os.path.exists(model_path):
        os.makedirs(model_path)
    joblib.dump(classifier_dict, model_path + model_name)
    logger.info("complete sava model")
