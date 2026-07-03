import sys

with open('api.py', 'r') as f:
    content = f.read()

# Remplacer la ligne Memory()
old = 'memory = Memory()'
new = 'memory = Memory(graph_file="data/octopus_data.json")'

content = content.replace(old, new)

with open('api.py', 'w') as f:
    f.write(content)

print("✅ api.py fixed")
