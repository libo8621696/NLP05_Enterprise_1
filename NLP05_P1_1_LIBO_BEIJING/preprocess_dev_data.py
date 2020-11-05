# 1）数据处理、解析，提取语料信息。

## 采用python自带的json包来对json文件进行解析
import json 
import os
##通过观察dureader的数据集和SQuAD2.0的数据集，发现二者的结构是相同的，因此，可以考虑将这两种数据集采用统一的函数进行调用。
##在这个版本中，主要测试较小的开发数据集，检验代码的正确性，所以这里选取的json文件为demo文件夹中的小文件demo_train.json和根目录下的dev-v2.0.json，能够较快得出相应的结果。
## 读取相应文件夹中的数据，形成列表reader_list，提取关键字'context'上下文信息列表
def get_data_from_file(filePath = 'None.json'):
    with open(filePath,'r') as reader_train:
        reader = json.load(reader_train)
    reader_list = (reader['data'])[0]['paragraphs']
    reader_context_list = [element['context'] for element in reader_list]
    return reader_context_list


dureader_context_list = get_data_from_file('dureader_robust-data/demo/demo_train.json')
print("dureader dev length is:")
print(len(dureader_context_list))

squad2_context_list = get_data_from_file('dev-v2.0.json')
print('squad2 dev length')
print(len(squad2_context_list))

# 2）使用分词工具处理语料。
## 导入jieba分词工具包并开启enable_paddle()模式对dureader的中文内容进行分词
import jieba
jieba.enable_paddle()
## 导入nltk分词工具包对SQuAD2.0的英文内容进行分词
import nltk
## 定义分词函数cut，将列表中的每个context对应的值进行分词形成分词列表,其中num参数默认设置为0，即为中文分词，否则为英文分词
def cut(context_list,num=0):
    segment_list = []
    if num == 0:
        segment_list = [list(jieba.cut(element)) for element in context_list]
    else:
        segment_list = [list(nltk.word_tokenize(element)) for element in context_list]
    return segment_list


## 建立一个二重列表sample_words，该列表的每个单元是完成对context进行分词的单词列表；
## 后缀为cn的是中文二重列表，后缀为en的是英文二重列表。
sample_words_cn = cut(dureader_context_list,0)

sample_words_en = cut(squad2_context_list, 1)

## 考虑到分词后的列表中含有太多的无意义助词，
## 因此利用百度的停用词表'stopwords.txt'来过滤掉意义不打的中文和英文内容
with open('stopwords.txt', 'r') as stw:
    stwlist = stw.read().split('\n')

## 采用get_words函数从
def get_words(sample_words):
    words = []
    for words_list in sample_words:
        for word in words_list:
            if word.strip() not in stwlist:
                words.append(word.strip())
    return words


# 3）对词频进行统计排序，输出到文本文件。
from collections import defaultdict

## 建立函数get_dict_to_text,参数是vocab, words和filePath，将字典输出到指定位置的文本中

def get_dict_to_text(sample_words, filePath = 'countercount.txt'):
    counts = defaultdict(lambda: 0)
    words = get_words(sample_words)
    vocab = list(set(words))
    for word in vocab:
        counts[word] = words.count(word)
    file_reader = open(filePath, 'w')
    for k, v in sorted(counts.items(), key=lambda item: item[1], reverse=True):
        file_reader.write(str(k) + ' ' + str(v) + '\n')
    file_reader.close()
    return 0

##　调用get_dict_to_text函数，将相应的二重列表转换为文本文档
get_dict_to_text(sample_words_cn, 'dict_dureader_dev.txt')
get_dict_to_text(sample_words_en, 'dict_squad2_dev.txt')


