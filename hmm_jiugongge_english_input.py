# -*- coding:utf-8 -* 

"""
英文九宫格输入法
(就是按1可以输入abc中某个，按2输入def中某个那样)
"""

from hmm import HMM
import sys
# m_A, m_B, m_PI 中数据来自于对莎士比亚某些作品的统计
from model_data_for_english import m_A, m_B, m_PI

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # 先输入英文，然后转化为1~9的表示，然后用这个数字序列，试图重新找到原单词
        print "usage: python this.py english_word [topK]"
        print " topK: find topK most likely candicates"
        sys.exit(-1)
    def i_2_sym(arr):
        m = " abcdefghijklmnopqrstuvwxyz "
        s = []
        for i in arr:
            s.append(m[i])
        return "".join(s)
    
    sym_2_i = {}
    arr = ["abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz", " "]
    for i in xrange(len(arr)):
        for j in arr[i]: 
            sym_2_i[j] = str(i + 1)
    
    aa = sys.argv[1].strip().lower() + " "
    s = []
    last = " "
    for i in aa:
        if i not in "abcdefghijklmnopqrstuvwxyz":
            i  = " "
        if last == " " and i == " ": 
            continue
        last = i
        s.append(sym_2_i[i])
    s = map(int, s)
    h = HMM(m_A, m_B, m_PI)
    top_K = 20
    try:
        top_K = int(sys.argv[2])
    except:
        pass
    ret = h.top_k_viterbi(s, top_K)
    for i in xrange(len(ret)):
        s1 =  i_2_sym(ret[i][1])
        print "%d\t%s\t" % (i + 1, s1),  ret[i][0]
