import sys

# Lire api.py
with open('api.py', 'r') as f:
    content = f.read()

# Ajouter l'import Memory en haut (après les autres imports)
if 'from memory import Memory' not in content:
    # Trouver la dernière ligne d'import
    lines = content.split('\n')
    insert_idx = 0
    for i, line in enumerate(lines):
        if line.startswith('from ') or line.startswith('import '):
            insert_idx = i + 1
    
    lines.insert(insert_idx, '\nfrom memory import Memory\nmemory = Memory()\n')
    content = '\n'.join(lines)

# Ajouter les nouveaux endpoints avant if __name__
new_endpoints = '''
@app.route('/api/world', methods=['GET'])
def api_world():
    return jsonify(memory.get_world())

@app.route('/api/node/<node_id>', methods=['GET'])
def api_node(node_id):
    node = memory.get_node(node_id)
    if node:
        return jsonify(node)
    return jsonify({"error": "Not found"}), 404

@app.route('/api/search', methods=['GET'])
def api_search():
    q = request.args.get('q', '')
    return jsonify(memory.search(q))

@app.route('/api/fragments', methods=['POST'])
def api_add_fragment():
    data = request.json
    frag = memory.add_fragment(
        agent=data.get('agent'),
        node=data.get('node'),
        content=data.get('content'),
        metadata=data.get('metadata')
    )
    return jsonify(frag), 201
'''

if "if __name__" in content:
    content = content.replace("if __name__", new_endpoints + "\n\nif __name__")

# Backup + save
with open('api.py.backup.sprint1', 'w') as f:
    f.write(content)

with open('api.py', 'w') as f:
    f.write(content)

print("✅ api.py patched successfully")
