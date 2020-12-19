#!/usr/bin/env python3
 
# http://webcache.googleusercontent.com/search?q=cache:
import os
import re
from collections import Counter


for file in os.listdir("/home/k5shao/Downloads/"):
    if file.endswith('.html'):
        print(file)
        with open("/home/k5shao/Downloads/"+file, 'r') as input_file:
            str = input_file.read()
        
        # https://stackoverflow.com/questions/42132038/python-regex-matching-urls-in-page-source-code
        arr = re.findall('(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', str)
        # print(arr)
        # exit(0)
        for i, tokens in enumerate(arr):
            # this part does not need \/
            arr[i] = tokens[1]
        dic = Counter(arr)
        

        with open("/home/k5shao/Downloads/"+os.path.splitext(file)[0] + ".txt", "w") as output_file:
            output_file.write('\n'.join(f'{val} {key}' for key, val in dic.items()))

        os.remove("/home/k5shao/Downloads/"+file)
