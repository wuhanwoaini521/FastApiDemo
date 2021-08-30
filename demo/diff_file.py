# import difflib
# import sys

# def read_file(filename):
#     try:
#         with open(filename, 'r') as f:
#             return f.readlines()
#     except IOError:
#         print("没有找到文件")

#         sys.exit(1)

# def compare_file(file1, file2, out_file):
#     file1_content = read_file(file1)
#     file2_content = read_file(file2)

#     d = difflib.HtmlDiff()
#     result = d.make_file(file1_content, file2_content)

#     with open(out_file, 'w') as f:
#         f.writelines(result)
# if __name__ == '__main__':
#     compare_file(r'demo\text.txt', r'demo\text1.txt','text.html')
    


#!/usr/bin/python
import difflib
text1 = """text1:  #定义字符串1
This module provides classes and functions for comparing sequences.
including HTML and context and unified diffs."""
 
text1_lines = text1.splitlines() #以行进行分隔，以便进行对比
text2 = """text2: #定义第二个字符串
This module provides """
 
text2_lines = text2.splitlines()

text3 = """text1:  #定义字符串1
This module provides classes and functions for comparing sequences.
including HTML and context and unified diffs.1"""
 
text3_lines = text3.splitlines() #以行进行分隔，以便进行对比
d = difflib.Differ() #创建Differ对象
diff = d.compare(text1_lines, text3_lines)  #采用compare方法对字符串进行比较
print('\n'.join(list(diff)))


