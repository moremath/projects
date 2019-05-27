#!/usr/bin/env python
# -*- coding: utf-8 -*-


import config
from util import predict
import json


path = config.raw_comments_json
saved_comments_path = config.data_path+ '/parsed_comments.json'
comments_yes_path,comments_no_path = config.data_path+'/comments_yes_list.json',config.data_path+'/comments_no_list.json'


def save(data, path):
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        f.write(s)
        
        
# 解析美团json数据
def parse_raw_comment_json():
    with open(path,encoding='utf-8') as f0:
        raw_data=f0.read()
        raw_data =json.loads( raw_data)
        comments = [ record['comment'] for record in raw_data['data']['comments'] ] 
        save( comments ,saved_comments_path)


# 用模型predict来筛选评论
def filter_comments( ):
    with open(saved_comments_path) as f:
        comments_list = json.load(f)
    true_false_result = predict(comments_list)
    comments_yes,comments_no = [],[]
    for i, flag in enumerate(true_false_result):
        if flag:
            comments_yes.append(comments_list[i])
        else:
            comments_no.append(comments_list[i])
    # 保存筛选的评论 ，非必须
    save(comments_yes,comments_yes_path)
    save(comments_no,comments_no_path)
    return comments_yes,comments_no
            


