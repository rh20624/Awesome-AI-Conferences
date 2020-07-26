
'''
Function: Analyze the ICML-2020 one sentence summary, generate the word cloud and statistical infofilermation;

reference: 
    - https://www.paperdigest.org/2020/07/icml-2020-highlights/ （ICML 论文整理）
    - https://blog.csdn.net/qq_23926575/article/details/85291955 （词云图）
    - https://blog.csdn.net/u010255642/article/details/83305099 (停用词)
Input: 
    html page from "Paper Digest";
Output:
    statistical information of ICML-2020 accepted papers;
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

html_path = "Paper Digest_ ICML 2020 Highlights – Paper Digest.html"
num_paper = 1084  # number of papaer accpted by ICML 2020
num_tuple = 5 # 每一篇论文要提取的内容条数:(index,title,author,title_link,summary)
papers = list()

## 从html页面拿到index,tile,link,author,summary
def extract_info(filepath):
    with open(filepath, "rb") as f:
        html = f.read().decode("utf-8")
        dom = etree.HTML(html)

        base_url = "/html/body/div[3]/section/div/div/div/div[2]/table/tbody/tr["
        for i in range(num_paper):
            i = i + 2
            s = [0 for ii in range(num_tuple)]
            for j in range(num_tuple):
                j_path = dom.xpath(base_url + str(i) + "]/td[" + str(j+1) + "]/text()")
                if(j == 0): 
                    s[0] = j_path
                elif(j == 2):
                    s[3] = j_path
                elif(j == 3):
                    s[4] = j_path
                else:
                    s[1] = dom.xpath(base_url + str(i) + "]/td[" + "2" + "]/a/text()") # 获取title
                    s[2] = dom.xpath(base_url + str(i) + "]/td[" + "2" + "]/a/@href") # 获取paper链接
                # print(s)
            papers.append((s[0],s[1],s[2],s[3],s[4]))  # 用tuple表示index,title,link,author,summary

        print(len(papers))
        # print(papers[:4])

## 定制化关键词，比如GNN,GAN,graph neural network(s)...
def get_keywords():
    pass

## 计算标题和总结中出现不同关键词的频率
def count_keyword():
    word_dict = {}
    for tup in papers:
        # 处理标题关键词
        title = tup[1][0] # 每一个论文的title
        title = title.split(" ") #title 转换为list
        # 过滤停止词语
        title = [t for t in title if t not in list_stopWords]
        for i in title:
            word_dict[i] = word_dict.get(i, 0) + 1

        # # 处理summary关键词
        # summary = tup[4][0]
        # summary = summary.split(" ")
        # summary = [t for t in summary if t not in list_stopWords]
        # for j in summary:
        #     word_dict[j] = word_dict.get(j,0) + 1

    # sort the word_dict
    print(type(word_dict))
    word_dict_list = sorted(word_dict.items(), key=lambda x: x[1] ,reverse=True)
    # print(word_dict[:30])

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
    for tup in papers:
        title = tup[1][0] # title is a string now
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
        
        # t = ''.join('%s' % id for id in t)
        # t.replace("(", "%|")
        # t.replace(")", "||")
        # t.replace(",", "||")
        # t.replace("'", " ")
        print(t)
    
    topic_dict_num = {}
    for (key,value) in topic_dict.items():
        topic_dict_num[key+"@"+str(value)] = value
    

    return topic_dict_num




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

word_dict = count_keyword()

author_dict = count_author()

topic_dict = count_topic()

# plot_wordcloud(author_dict)

# plot_wordcloud(word_dict)

plot_wordcloud(topic_dict)