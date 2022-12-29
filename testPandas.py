import pandas as pd

dict1 = {"miles": 0, "year": 23}
dict2 =  {"miles": 0, "year": 13}
dict3 =  {"miles": 0, "year": 23}

data = [dict1,dict2,dict3]

data = pd.DataFrame.from_dict(data, orient='columns', dtype=None, columns=None)

print (data)

data.reset_index()
data.to_csv("file_name.csv", sep=',', encoding='utf-8', index=False)