import sys 
 
with open('evaluator.py', 'r') as f: 
    lines = f.readlines() 
 
# Fix line 12 (index 11) 
if len(lines) 
    lines[11] = '                       category: str, difficulty: str) -, Any]:\n' 
    print('Fixed line 12') 
else: 
    print('File has less than 12 lines') 
 
with open('evaluator.py', 'w') as f: 
    f.writelines(lines) 
print('File saved') 
