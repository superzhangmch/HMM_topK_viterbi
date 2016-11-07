# -*- coding:utf-8 -* 
"""
split chinese to seperate chars
"""

class Chinese(object):
    """ chinese relative """

    @staticmethod
    def utf82gbk(utf8):
        """ utf8 to gbk """
        return utf8.decode("utf8").encode("gbk")
    
    @staticmethod
    def gbk2utf8(gbk):
        """ gbk to utf8 """
        return gbk.decode("gbk").encode("utf8")
    
    @staticmethod
    def gbkline_2_chars(line):
        """ gbkline_2_chars """
        ret = Chinese.utf8line_2_chars(Chinese.gbk2utf8(line))
        for i in xrange(len(ret)):
            ret[i] = Chinese.utf82gbk(ret[i])
        return ret
    
    @staticmethod
    def gbkline_2_utf8chars(line):
        """ gbkline_2_chars """
        ret = Chinese.utf8line_2_chars(Chinese.gbk2utf8(line))
        return ret
    
    @staticmethod
    def utf8line_2_chars(line):
        """ line2chars """
        char_set = []
        last_char = ""
        for i in xrange(len(line)):
            char = line[i]
            char_i = ord(char)
            if char_i & 0b10000000 == 0:
                if last_char:
                    char_set.append(last_char)
                    last_char = ""
                char_set.append(char)
            elif char_i & 0b11000000 == 0b11000000:
                if last_char:
                    char_set.append(last_char)
                    last_char = ""
                last_char = char
            else:
                last_char += char
        if last_char:
            char_set.append(last_char)
            last_char = ""
        return char_set
    

if __name__ == "__main__":
    char_set = Chinese.gbkline_2_chars("aabÄãºÃ°¡hh")
    print "--"
    for i in char_set:
        print i
