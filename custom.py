import json
import gzip

def pdarse(path):
    g = gzip.open(path, 'r') 
   
    for l in g: 
        yield json.dumps(eval(l)) 


f = open("output.json", 'w') 
f.write('{')
index = 0
for l in pdarse("qa_Grocery_and_Gourmet_Food.json.gz"): 
    f.write(str(index)+':'+l + ',\n')
    index = index +1
f.write('}')

