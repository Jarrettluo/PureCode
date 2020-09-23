# encoding: utf-8
"""
@version: 1.0
@author: 
@file: purecode.py
@time: 2020/4/2 10:53
"""
import codecs

class GetPureCode:
    """
    获得纯净的代码
    """
    def __init__(self,FilePath):
        self.anno_flag = '//'
        self.file_path = FilePath
        pass

    def delete_code(self):
        """
        删除注释条目
        :return:返回列表
        """
        f = codecs.open(self.file_path,encoding='UTF-8')
        code_list = f.readlines()
        f.close()
        self.new_code = []
        for code in code_list:
            code_splited_list = code.split(self.anno_flag) #按照注释的首行进行分开，例如#，//，/-,{!}
            if len(code_splited_list) <2:
                if code_splited_list[0].isspace() == False:
                    self.new_code.append(code_splited_list[0])
                else:
                    pass
            elif code_splited_list[0] != '':
                if code_splited_list[0].isspace() == False:
                    self.new_code.append(code_splited_list[0]+'\r\n')
                else:
                    pass
            else:
                pass
        return self.new_code

    def save_to_path(self):
        file_path_list = (self.file_path).split('/')
        file_path = '/'.join(file_path_list[0:-1])
        filename = file_path+'/PureCode_'+file_path_list[-1]
        contents = ''.join(self.new_code) #写入文件的字符必须是字符串
        try:
            fh = open(filename, 'w')
            fh.write(contents)
            fh.close()
        except Exception as err:
            return err
        else:
            return 1





