# -*- coding: utf-8 -*-
from os.path import join
from codecs import open

def build_corpus(split, make_vocab=True, data_dir="../dataset/dxy"):
    features_list = []
    with open(join(data_dir,'keywords.txt'),'r',encoding='utf-8') as f:
        for line in f.readlines():
            features_list.append(line.strip().split(' ')[0])
            #print(features_list[0])

    '''
    创建特征词列表、特征词+tag字典（特征词作为key，tag作为value）
    '''

    #将features_dict中的特征词和tag存入字典  特征词为key，tag为value
    dict={}
    with open(join(data_dir,'keywords.txt'),'r',encoding='utf-8') as f:
        for line in f.readlines():
            item = line.split(' ')
            #print(item)
            if len(item) >1:
                dict[item[0]]=item[1]
            else :
                with open(join(data_dir,'error.txt'),'a',encoding='utf-8') as f:
                    f.write(line+"\n")


    '''
    根据字典中的word和tag进行自动标注，用字典中的key作为关键词去未标注的文本中匹配，匹配到之后即标注上value中的tag
    '''
    file_input = join(data_dir,split+'.txt')
    file_output = join(data_dir,split+'_labeled.txt')
    index_log = 0
    word_list = []
    tag_list = []
    word_lists = []
    tag_lists = []
    with open(file_input,'r',encoding='utf-8') as f:
        for line in f.readlines():
            #print(line)
            word_list = list(line.strip())
            tag_list = ["O" for i in range(len(word_list))]

            for keyword in features_list:
                #print(keyword)
                while 1:
                    index_start_tag = line.find(keyword,index_log)
                    #当前关键词查找不到就将index_log=0,跳出循环进入下一个关键词
                    if index_start_tag == -1:
                        index_log = 0
                        break
                    index_log = index_start_tag+1
                    #print(keyword,":",index_start_tag)
                    #只对未标注过的数据进行标注，防止出现嵌套标注
                    for i in range(index_start_tag, index_start_tag + len(keyword)):
                        if index_start_tag == i:
                            if tag_list[i] == 'O':
                                tag_list[i] = "B-"+dict[keyword].replace("\n",'')  # 首字
                        else:
                            if tag_list[i] == 'O':
                                tag_list[i] = "I-"+dict[keyword].replace("\n",'')  # 非首字

            #print(word_list,tag_list)
            with open(file_output,'a',encoding='utf-8') as output_f:
                for w,t in zip(word_list,tag_list):
                        #print(w+" "+t)
                        if w != '	' and w != ' ':
                            output_f.write(w+" "+t+'\n')
                            #output_f.write(w + " "+t)
                output_f.write('\n')

    #print(word_list)
    word_lists.append(word_list)
    tag_lists.append(tag_list)
    #print(len(word_lists))
    #print(len(tag_lists))
    if make_vocab:
        word2id = build_map(word_lists)
        tag2id = build_map(tag_lists)
        return word_lists, tag_lists, word2id, tag2id
    else:
        return word_lists, tag_lists


def build_map(lists):
    maps = {}
    for list_ in lists:
        for e in list_:
            if e not in maps:
                maps[e] = len(maps)

    return maps
            
build_corpus('train', False)
