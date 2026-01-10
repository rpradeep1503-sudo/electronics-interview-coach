import re 
with open('evaluator.py', 'r') as f: 
    lines = f.readlines() 
for i in range(len(lines)): 
    lines[i] = lines[i].replace(') -, Any]:', ') -, Any]:') 
with open('evaluator.py', 'w') as f: 
    f.writelines(lines) 
print("Fixed the syntax error") 
