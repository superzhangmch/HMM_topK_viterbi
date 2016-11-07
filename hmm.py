# -*- coding:utf-8 -* 

"""
HMM topK viterbi
"""

class HMM(object):
    """
    Hidden Markov Model
    can do topK viterbi
    note:
        hidden states set should be composed of continuous integers 
                                starting from 1, like 1, 2, 3, ... M
        observable states set should be composed of continuous 
                            integers starting from 1, like 1, 2, 3, ... N
    """

    def __init__(self, matrix_A=None, matrix_B=None, array_PI=None):
        """
        # if matrix_A, matrix_B, array_PI are not set, 
                then A(), B(), PI(), o_2_i() should be re-implemented
        如果不提供matrix_A, matrix_B, array_PI，那么就需要继承本类，并重新实现A()
               B(), PI(), o_2_i() 等相关函数
        """
        self._m_o_2_i = {}
        if array_PI:
            self._PI = array_PI
        if matrix_A:
            self._m_A = matrix_A
        if matrix_B:
            self._m_B = matrix_B
            for i in xrange(len(matrix_B[0])):
                self._m_o_2_i[i + 1] = []
            for i in xrange(len(matrix_B)):
                for j in xrange(len(matrix_B[i])):
                    if matrix_B[i][j] != 0:
                        self._m_o_2_i[j + 1].append(i + 1)


    def A(self, i, j):
        """
        probability for hidden state i -> hidden state j
        for sparse probability matrix, you can  re-implement this function
        
        """
        return self._m_A[i-1][j-1]

    def B(self, i, j):
        """
        probability for hidden state i -> observable state j
        for sparse probability matrix, you can  re-implement this function
        """
        return self._m_B[i-1][j-1]

    def PI(self, i):
        """
        probability for initial hidden state i
        for sparse probability array, you can  re-implement this function
        """
        return self._PI[i-1]

    def o_2_i(self, o):
        """
        given the observable state o, returns all possible hidden states related to it
        """
        return self._m_o_2_i[o]

    
    def top_k_viterbi(self, o_seq, topK=1):
        """ 
        find topK most likely hidden states sequence for the given observable sequence(o_seq)
        o_seq: input sequence, format: o_seq = [1, 2, 33, 3, 44]
        topK: return topK best results
        """
        delta = []
        phy = []
        for i in xrange(len(o_seq)):
            delta.append({})
            phy.append({})
    
        t = 0
        o1 = o_seq[t]
        cur_i_list = self.o_2_i(o1)
        for i in cur_i_list:
            delta[t][i] = [0.] * topK
            delta[t][i][0] = self.PI(i) * self.B(i, o1)
            phy[t][i] = [[0, 0, delta[t][i][0]]] * topK
    
        last_i_list = cur_i_list
        for t in xrange(1, len(o_seq)):
            o_t = o_seq[t]
            cur_i_list = self.o_2_i(o_t)
            for i in cur_i_list:
                tmp = []
                for j in last_i_list:
                    for idx in xrange(topK):
                        P = delta[t-1][j][idx] * self.A(j, i) * self.B(i, o_t)
                        tmp.append([P, j, idx, P])
                tmp = sorted(tmp, key=lambda ele: ele[0], reverse=True)
    
                delta[t][i] = map(lambda ele: ele[0], tmp) + [0.] * topK
                phy[t][i] = map(lambda ele: [ele[1], ele[2], ele[3]], tmp) + [[-1, -1]] * topK
                delta[t][i] = delta[t][i][0: topK]
                phy[t][i] = phy[t][i][0: topK]
            last_i_list = cur_i_list
    
        result_p = []
        for i in delta[-1]:
            for idx in xrange(topK):
                result_p.append([delta[-1][i][idx], i, idx])
        result_p = sorted(result_p, key=lambda ele: ele[0], reverse=True)
        result_p = result_p[0: topK]
    
        result = []
        for p, i, idx in result_p:
            if p <= 0.:
                continue
            arr = [i]
            cur_i = i
            cur_idx = idx
            for t in xrange(len(o_seq) - 1, 0, -1):
                next_i, next_idx, P = phy[t][cur_i][cur_idx]
                arr.append(next_i)
                cur_i = next_i
                cur_idx = next_idx
    
            arr.reverse()
            result.append([p, arr])
        return result
    
