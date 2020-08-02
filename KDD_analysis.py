'''
Function: KDD 2020 accepted paper analysis;

reference: 
    - https://www.kdd.org/kdd2020/accepted-papers (KDD 2020 accepted papers)
    - https://blog.csdn.net/qq_23926575/article/details/85291955 （词云图）
    - https://blog.csdn.net/u010255642/article/details/83305099 (停用词)
Input: 
    html page from KDD 2020;
Output:
    statistical information of KDD-2020 accepted papers;
    word cloud;
'''

## 解析html页面
from lxml import etree

## 过滤停止词
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize,word_tokenize
# nltk.download("stopwords")
#英文停止词
list_stopWords=list(set(stopwords.words('english')))

import matplotlib.pyplot as plt
from wordcloud import WordCloud
import requests    # 根据url拿到指定的网页html 

# 添加定制的停止词
my_stoplist = ['A','via','on','On','The','using','From']
for a in my_stoplist:
    list_stopWords.append(a)

# 定义topic短语词组
topic_list = ['GNN', 'GCN', 'graph',
'convolutional neural networks','CNN','convolutional neural networks',
'GAN', 'GANs', "generative adversarial","generative adversarial",
'reinforcement learning','Q-learning', 
'online learning', "real time", "real-time",
'Differential Privacy', "private", "privacy", 
'time series', 
"semi-supervised",
"unsupervised",
"meta-learning", "few-shot",
"interpretability","Explanability",
"Knowledge Distillation","co-training","co-teaching",
"transfer learning", 'knowledge transfer',
'multi-task',
'uncertainty',
'Federated', 'Federated learning']

html_path = "KDD 2020 _ Accepted Papers.html"
num_paper = 1084  # number of papaer accpted by ICML 2020
num_tuple = 5 # 每一篇论文要提取的内容条数:(index,title,author,title_link,summary)
papers = list()
titles = list()
authors = list()


## content block
# /html/body/main/div[2]/section/div/div[1]/div[2]/div/ul/li[51]

## author, title
# /html/body/main/div[2]/section/div/div[1]/div[2]/div/ul/li[51]/div/span[2] 
# /html/body/main/div[2]/section/div/div[1]/div[2]/div/ul/li[51]/div/span[1]

## 从html页面拿到index,tile,link,author,summary
def extract_info(filepath):
    # f = requests.get(html_path,verify=False)
    with open(filepath, "rb") as f:
        html = f.read().decode("utf-8")
        dom = etree.HTML(html)

        ## 根据class name查看论文数量; research track, application track
        class_obj_1 = dom.xpath('/html/body/main/div[2]/section/div/div[1]/div[1]/div/ul')
        class_obj_2 = dom.xpath('/html/body/main/div[2]/section/div/div[1]/div[2]/div/ul')

        num_1, num_2 = 0, 0
        for _ in class_obj_1[0]:
            num_1 += 1
        for _ in class_obj_2[0]:
            num_2 += 1
        print("Total num, research track, and application track of paper in KDD 2020 is = ", num_1+num_2, num_1, num_2)
        base_url_1 = "/html/body/main/div[2]/section/div/div[1]/div[1]/div/ul/"
        base_url_2 = '/html/body/main/div[2]/section/div/div[1]/div[2]/div/ul/'

        # /html/body/main/div[2]/section/div/div[1]/div[1]/div/ul/li[1]/div/span[2]/text()
        ## 1. process research track papers
        for i in range(num_1):
            
            temp = dom.xpath(base_url_1 + 'li[' + str(i+1) + ']/div/span[1]/text()')[0].__str__()
            titles.append(temp)
            temp = dom.xpath(base_url_1 + 'li[' + str(i+1) + ']/div/span[2]/text()')[1].__str__()
            authors.append(temp.replace('   ','').replace('\n','').strip())

        ## 2. process application track papers
        for j in range(num_2):
            temp = dom.xpath(base_url_2 + 'li[' + str(j+1) + ']/div/span[1]/text()')[0].__str__()
            titles.append(temp)
            temp = dom.xpath(base_url_2 + 'li[' + str(j+1) + ']/div/span[2]/text()')[1].__str__()
            authors.append(temp.replace('   ','').replace('\n','').strip())


## 定制化关键词，比如GNN,GAN,graph neural network(s)...
def get_keywords():
    pass

## 计算标题和总结中出现不同关键词的频率
def count_keyword():
    word_dict = {}
    # print(titles[:10])
    # dede
    for title in titles:
        ## 处理title 得到单词
        # print(type(title))
        
        title = title.split(" ")
        # print(title)
        
        ## 过滤停止词语
        title = [t for t in title if t not in list_stopWords]
        for i in title:
            word_dict[i] = word_dict.get(i, 0) + 1
                   

    # sort the word_dict
    # print(type(word_dict))
    word_dict_list = sorted(word_dict.items(), key=lambda x: x[1] ,reverse=True)
    # print(word_dict_list[:30])

    ## 把论文数量添加到每个关键词的后面
    word_dict_num = {}
    for (key,value) in word_dict.items():
        word_dict_num[key+"@"+str(value)] = value

    return word_dict_num

### 计算作者名字出现的频率并加以排序
def count_author():
    author_dict = {}
    for tup in papers:
        author = tup[3][0]
        author = author.split(",")
        # 过滤停止词

        for i in author:
            author_dict[i] = author_dict.get(i,0) + 1
    # 按照名字出现顺序排序
    author_list = sorted(author_dict.items(), key=lambda x: x[1],reverse=True)
    print(author_list[:10])
    print(len(author_list))
    for i in range(10):
        print(author_list[i])
    
    # 把论文数量添加到作者名字后面，作为key; name+num --> key
    author_dict_num = {}
    for (key,value) in author_dict.items():
        author_dict_num[key+"@"+str(value)] = value
    
    return author_dict_num


## 根据主题（专业名词短语）进行统计，排序，分类；
def count_topic():
    topic_dict = {}
    for title in titles:
        # title = tup[1][0] # title is a string now
        # title.lower() # 转换为小写
        import re
        for t in topic_list:
            result = bool(re.search(t, title, re.IGNORECASE))  #大小写无关
            if(result == True):    
                topic_dict[t] = topic_dict.get(t,0) + 1
    
    # 排序
    topic_dict_list = sorted(topic_dict.items(), key=lambda x: x[1], reverse=True)

    print(topic_dict_list)
    for t in topic_dict_list:
        
        t = ''.join('%s' % id for id in t)
        t.replace("(", "%|")
        t.replace(")", "||")
        t.replace(",", "||")
        t.replace("'", "  ")
        print(t)
    
    topic_dict_num = {}
    for (key,value) in topic_dict.items():
        topic_dict_num[key+"@"+str(value)] = value
    

    return topic_dict_num


## 根据作者的所属机构进行排名
def count_institution():
    pass


def plot_wordcloud(word_dict):
    '''根据词频字典生成词云图'''
    wc = WordCloud(
        max_words=500,  # 最多显示词数
        # max_font_size=100,  # 字体最大值
        background_color="white",  # 设置背景为白色，默认为黑色
        width = 2000,  # 设置图片的宽度
        height= 1000,  # 设置图片的高度
        margin= 10  # 设置图片的边缘
    )
    print(type(word_dict), len(word_dict))
    wc.generate_from_frequencies(word_dict)  # 从字典生成词云
    plt.imshow(wc)  # 显示词云
    plt.axis('off')  # 关闭坐标轴
    plt.show()  # 显示图像


extract_info(html_path)

# word_dict = count_keyword()

# author_dict = count_author()

topic_dict = count_topic()

# plot_wordcloud(author_dict)

# plot_wordcloud(word_dict)

plot_wordcloud(topic_dict)