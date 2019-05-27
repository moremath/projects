#!/usr/bin/env python
# -*- coding: utf-8 -*-


# jieba是nlp的常用库
import jieba
import pandas as pd
import numpy as np
import config
from sklearn.externals import joblib


# 过滤掉 停用词,这里有很大优化空间
stop_words = []
cols = ['dish_look','dish_taste','dish_portion','dish_recommendation',] 


def load_data_from_csv(file_name, header=0, encoding="utf-8"):
    one_col_name ="id"
    count_rows = pd.read_csv(file_name, header=header, encoding=encoding,usecols=[ one_col_name]).shape[0]
    # 可以先从1/10的size开始
    size_rows = count_rows//3
    
    data_df = pd.read_csv(file_name, header=header, encoding=encoding,
    # usercols是选取一部分列(col)
    #usecols=['others_willing_to_consume_again','others_overall_experience','dish_recommendation','dish_look','dish_taste','dish_portion','price_discount','price_cost_effective','content','id'],
    #usecols=['dish_recommendation','dish_look','dish_taste','dish_portion','content','id'],
    # 精简的col
    usecols= cols + ['content','id']        
    #如果想缩减输入行，可以取消下行注释；如果行不连续读取会error，比如用skiprows= lambda x: x%3 ==0,
    #nrows= size_rows,
    )
    #print(file_name,'size_rows:',size_rows)
    return data_df


# 对评论分词
def seg_words(contents):
    '''
    最终得到评论的字符串列表，每条评论分词后词语间用空格分隔
    '''
    contents_segs = list()
    for content in contents:
        rcontent = content.replace("\r\n", " ").replace("\n", " ")
        segs = [word for word in jieba.cut(rcontent) if word not in stop_words]
        contents_segs.append(" ".join(segs))
    return contents_segs


# 测试用官方csv表格测试
def predict_from_csv(csv_file_path,col,model_name='fasttext_model.pkl'):
    # csv 格式要与train valid 等官方数据集的表头一致,比如下行的['content']    
    comments_list = seg_words( load_data_from_csv(csv_file_path)['content'] )
    comments_format= np.asarray([comments_list]).T
    clsf = joblib.load(config.model_path + model_name)
    return clsf[col].predict(comments_format).astype(int)
    

def get_clsf(csv_file_path,model_name='fasttext_model.pkl'):
    # csv 格式要与train valid 等官方数据集的表头一致,比如下行的['content']    
    comments_list = seg_words( load_data_from_csv(csv_file_path)['content'] )
    comments_format= np.asarray([comments_list]).T
    clsf = joblib.load(config.model_path + model_name)
    return clsf,comments_format


# 预测 
def predict(comments_list,model_name='fasttext_model.pkl'):
    '''
    comments_list: list of string ,e.g: ['','哈哈','挺不错，好，还会再去','味道一般，偶尔吃吃还可以']
    model_name: model目录下pkl文件名
    return : list of Boolean ,e.g: [True,False,True, ...]
    '''
    # 为了方便测试，直接传入的评论字符串列表  不必以csv文件
    comments_list = seg_words
    # 加载模型
    clsf = joblib.load(config.model_path + model_name)
    # 转秩 成n x 1   clsf predict参数是 [ ['xxx'],['xxx'],... ]的形式
    comments_format = np.asarray([comments_list]).T
    # predict方法返回一维的np.array( [...])，astype(int)，是将float-->int：
    #clsf[col].predict(comments_format).astype(int)
    # 合并不同col的评价到newaxis,写得有点绕
    cols_index = None
    for col in cols:
        col_index = clsf[col].predict(comments_format).astype(int)[:,np.newaxis]
        if cols_index is not None:            
            cols_index = np.append(
                cols_index,
                col_index,
                axis=1 
            )
        else:
            cols_index = col_index
    # 原数据集中有四个指数 1(好评),0(中立评价),-1(差评),-2(未提及)
    # 如果cols中label的预测全是-2 指数，判定为False
    no_index_sum = -2 *len(cols)
    return [ 
        sum(indexs) != no_index_sum
        for indexs in cols_index 
         ] 
    
        
    
    
