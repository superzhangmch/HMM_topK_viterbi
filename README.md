# HMM_topK_viterbi

  HMM 的 viterbi 算法一般只能找到 observable states sequence 的“一条”最佳 hidden state sequence。
  本实现可以找到topK条！
  
  所以名其曰： topK viterbi
  
  附带了两个基于 HMM 的例子：一个例子是“根据拼音串给出汉字句子”的中文输入法，另一个是英文的九宫格输入法。
