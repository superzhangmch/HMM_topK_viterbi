# -*- coding:utf-8 -* 

"""
chinese input use HMM

"""

from hmm import HMM
import cPickle as pickle
# 汉字转 hidden state id. 汉字需要是 UTF8 格式，下同
hz2ID = pickle.load(open("chinese/word_map.dat", "rb"))
# hidden state id 转汉字
ID2hz = pickle.load(open("chinese/word_rev_map.dat", "rb"))
# 转移概率矩阵. 
# 格式 HzTransP = {(汉字1_id, 汉字2_id): 概率} 表示第一个字后面可能跟有第二个字的概率
HzTransP = pickle.load(open("chinese/word_p_m_final.dat", "rb"))
# 起始状态矩阵. 格式 startHzP = {汉字id: 概率} 表示一句话以该汉字开头的概率
startHzP = pickle.load(open("chinese/first_p_m.dat", "rb"))
# ======================
# Note:
# 以上两个概率数据是从某个语料库统计来的
# 只需替换以上数据，就可以采用新的模型
# ======================

from chinese import Chinese
from pinyin_hz_trans import map_pinyin_2_hanzi
from pinyin_hz_trans import map_hanzi_2_pinyin

# 拼音转observable state ID. 拼音需要小写
py2ID = {}
# observable state ID转拼音
ID2py = {}
i = 1
for py in map_pinyin_2_hanzi:
    py2ID[py] = i
    ID2py[i] = py
    i += 1

# 汉字ID转拼音ID, 会用于生成hidden state往observable state的转换概率
hzID_2_pyID = {}
for hz in map_hanzi_2_pinyin:
    if hz in hz2ID:
        py = map_hanzi_2_pinyin[hz]
        hz_id = hz2ID[hz]
        py_id = py2ID[py]
        hzID_2_pyID[hz_id] = py_id

# 查询出拼音ID对应有哪些汉字ID，这个只是为了加速viterbi计算
pyID_2_hzIDs = {}
for py in map_pinyin_2_hanzi:
    hz_list = map_pinyin_2_hanzi[py]
    py_id = py2ID[py]
    pyID_2_hzIDs[py_id] = []
    for hz in hz_list:
        if hz in hz2ID:
            pyID_2_hzIDs[py_id].append(hz2ID[hz])

class my_HMM(HMM):
    """
    重新实现 A(), B() 等几个函数
    """

    def A(self, i, j):
        """     
        probability for hidden state i -> hidden state j
        """
        k = (i, j)
        if k in HzTransP:
            return HzTransP[k]
        else:
            return 0.0

    def B(self, i, j):
        """     
        probability for hidden state i -> observable state j
        """
        if i in hzID_2_pyID and hzID_2_pyID[i] == j:
            return 1.0
        else:
            return 0.0

    def PI(self, i):
        """     
        probability for initial hidden state i
        """
        if i in startHzP:
            return startHzP[i]
        else:
            return 0.0

    def o_2_i(self, o):
        """     
        given the observable state o, returns all possible hidden states related to it
        """
        if o in pyID_2_hzIDs:
            return pyID_2_hzIDs[o]
        else:
            return []

if __name__ == "__main__":

    def hzIDs_2_sentence(arr):
        """
        汉字ID序列转汉字句子
        """
        s = []
        for i in arr:
            s.append(ID2hz[i])
        return "".join(s)

    import sys
    h = my_HMM()
    top_K = 20
    is_input_py=True
    try:
        top_K = int(sys.argv[1])
    except:
        pass
    try:
        is_input_py = True if int(sys.argv[2]) else False
    except:
        pass
    if is_input_py:
        print "please input pinyins seperated by space"
    else:
        print "please input gbk-chinese sentence"

    while True:
        print "--------------"
        input_str = raw_input("Input: ")
        if input_str[0: 4] == "exit":
            sys.exit()
        print "input = [%s]" % (input_str)
        s = []
        if is_input_py:
            # 输入是空格隔开的拼音
            input_str = input_str.lower().split(" ")
            for i in input_str:
                if i not in py2ID:
                    print "pinyin=%s not found" % (i)
                    continue
                s.append(py2ID[i])
        else:
            # 输入是gbk 中文句子，会先转成拼音
            input_str = Chinese.gbkline_2_utf8chars(input_str)
            s = []
            for i in input_str:
                if i not in hz2ID:
                    print "hanzi=%s not found" % (i)
                    continue
                s.append(hzID_2_pyID[hz2ID[i]])

        ret = h.top_k_viterbi(s, top_K)
        print "No.\tsentence\tprobability"
        for i in xrange(len(ret)):
            s1 =  Chinese.utf82gbk(hzIDs_2_sentence(ret[i][1]))
            print "%d\t%s\t" % (i + 1, s1),  ret[i][0]
