### 代码结构(fastText_ja049/目录下)
+ data/ 数据
        +  train.csv 原始的训练数据
        + raw_comments.json 美团抓取的数据
        + 其他3个.json 是comments.py运行生成的结果
+ model/   保存了训练的模型    
        + fasttext_model.pkl 默认default参数1/3原训练集的size
            + fasttext_model00.pkl 默认default参数1/10原训练集的size    
+ webPage_show  前端展示页面  [临时展示网址](www.aimofashi.com)
        + 显示数据可通过js/data.js来修改
        + 点击index.html在浏览器中查看
+  600comments_(393valid).html  之前爬取的数据用网页显示
+  comments.py 
        +  评论预处理的parse_raw_comment_json函数，提供测试的评论
        +  模型训练后用filter_comments来返回真值列表
+  main_train.py  训练模型
        + 在安装好环境的python下`python main_train.py`可默认不加参数
+  util.py  
        + load_data_from_csv 读取源训练集并控制size
        + seg_words 分词预处理，stop_words可以自定义加入一些无意义的高频词
        + predict 模型训练好只好按照之前方案 全部为-2来判断是否菜品，默认使用fasttext_model
+  requirement.txt  依赖包
        + `pip install -r  requirement.txt`安装，注意fasttext的版本不能太高，否则不兼容，其他库的版本可忽略，当然得用py3.5+
        +  如果是windows环境可能有不是很方便安装
###  结果分析(可作论文参考)
+   原数据集train.csv当中的标签本省是不均衡的，这不符合**独立同分布**假设

+    trainning set一共105000行，下表预测用的是1/3size训练的fasttext_model.pkl 
     
     +   可以发现，同一个model对于不同数据集的预测基本是稳定的，在[-2,-1,0,1]之间的相对大小也和训练集接近
     
     |                         | 原train.csv      | train.csv预测   | valid.csv预测   |
     | :---------------------- | ---------------- | --------------- | --------------- |
     | dish_look -2            | 75975次(72.36%)  | 87784次(83.6%)  | 12584次(83.89%) |
     | dish_look -1            | 3178次(3.02%)    | 1829次(1.74%)   | 244次(1.63%)%'  |
     | dish_look  0            | 4675次(4.45%)    | 669次(0.64%)    | 96次(0.64%)     |
     | dish_look   1           | 21172次(20.16%)  | 14718次(14.02%) | 2076次(13.84%)  |
     |                         |                  |                 |                 |
     | dish_taste  -2          | 5070次(4.83%)    | 4196次(4.0%)    | 592次(3.95%)    |
     | dish_taste  -1          | 4363次(4.16%)    | 3599次(3.43%)   | 457次(3.05%)    |
     | dish_taste   0          | 40200次(38.2%)   | 37224次(35.45%) | 5322次(35.48%)  |
     | dish_taste   1          | 55367次(52.73%)  | 59981次(57.12%) | 8629次(57.53%)  |
     |                         |                  |                 |                 |
     | dish_portion  -2        | 56917 次(54.21%) | 65333次(62.22%) | 9434次(62.89%)  |
     | dish_portion  -1        | 10018 次(9.54%)  | 7408次(7.06%)   | 1046次(6.97%)   |
     | dish_portion  0         | 9506 次(9.05%)   | 4568次(4.35%)   | 625次(4.17%)    |
     | dish_portion  1         | 28559 次(27.20%) | 27691次(26.37%) | 3895次(25.97%)  |
     |                         |                  |                 |                 |
     | dish_recomendation -2   | 84767 次(80.73%) | 91599次(87.24%) | 13118次(87.45%) |
     | dish_recomendation -1   | 2275 次(2.17%)   | 1150次(1.1%)    | 137次(0.91%)    |
     | dish_recomendation   0  | 1988 次(1.89%)   | 595次(0.57%)    | 81次(0.54%)     |
     | dish_recomendation   -1 | 15970 次(15.21%) | 11656次(11.1%)  | 1664次(11.09%)  |
     
+   展示页面通过修改webPage_show/js/data.js中的数据自定义评论和相关比例(文本编辑，注意引号和逗号，且都是半角)
