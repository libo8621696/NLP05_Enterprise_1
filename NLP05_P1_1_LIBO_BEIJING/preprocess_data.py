# 1）数据处理、解析，提取语料信息。(程序逻辑正确20，代码简洁无bug30)

## 采用python自带的json包来对json文件进行解析
import json 
import os

## 读取dureader_robust-data/demo中的demo/demo_train.json数据，形成列表dureader_list，避免数据量太大造成机器负担太重
with open('dureader_robust-data/demo/demo_train.json', 'r') as dureader_train:
    dureader = json.load(dureader_train)

dureader_list = (dureader['data'])[0]['paragraphs']



## 解析train.json数据中的context信息并形成语料列表squad2_context_list 
squad2_context_list = [element['context'] for element in squad2_list]


## 只读读取SQuAd2.0数据集中的dev-v2.0数据，形成列表squad_list，避免数据量太大造成机器负担太重
with open('dev-v2.0.json', 'r') as squad_dev:
    squad2 = json.load(squad_dev)

squad2_list = (squad2['data'])[0]['paragraphs']

## 解析train.json数据中的context信息并形成语料列表squad2_context_list 
squad2_context_list = [element['context'] for element in squad2_list]

## 得到squad2_context_list集合的长度为14520
print('squad2 dev length')
print(len(squad2_context_list))

# 2）使用分词工具处理语料。(工具使用正确20)
## 导入jieba分词工具包并开启enable_paddle()模式
import jieba 
jieba.enable_paddle()  
## 定义分词函数，将列表中的每个元素进行分词形成分词列表
def cut(context_list): 
    return [list(jieba.cut(element)) for element in context_list]


sample_words = cut(dureader_context_list)


with open('stopwords.txt', 'r') as stw:
    stwlist = stw.read().split('\n')


# print(sample_words[:2])
words = []

for words_list in sample_words:
    for word in words_list:
        if word.strip() not in stwlist:
            words.extend(word)
words_extracted = words
vocabulary = set(words_extracted)
print(len(vocabulary))

# 3）对词频进行统计排序，输出到文本文件。(程序逻辑正确20，代码简洁无bug30)
from collections import defaultdict
counts = defaultdict(lambda: 0)
for word in vocabulary:
    counts[word] = words.count(word)
counts_sorted = sorted(counts.items(), key=lambda item:item[1],reverse=True)
# print(counts_sorted)

## 将字典输出到文本

### 打开文本dict_dureader.txt
file_dureader = open('dict_dureader.txt', 'w')

### 按照遍历字典的元素，将每项元素的key和value分拆组成字符串，添加分隔符和换行符
for k,v in sorted(counts.items(), key=lambda item:item[1],reverse=True):
	file_dureader.write(str(k)+' '+str(v)+'\n')
	
### 关闭文件
file_dureader.close()


# 4）整体程序运行无bug(20)