import sys
import json

def execute(pc_dir, blog_dir):
    col = 2
    friendlist = ''
    with open(pc_dir + '/friends.json', 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    for i, j in enumerate(data):
        if i % col == 0:
            friendlist += '<div class="row">'
        friendlist += f'''
<div class="col-6">
    <div class="card">
        <img class="avatar" src="{j['avatar']}"></img>
        <a href="{j['url']}" target="_blank"><strong>{j['name']}</strong></a>
        <br>
        <span>{j['description']}</span>
    </div>
</div>
'''
        if i % col == col - 1:
            friendlist += '</div>\n'
    if len(data) % col != 0:
        friendlist += '</div>\n'
    with open(pc_dir + '/friends.html', 'r', encoding='utf-8') as f:
        pagehtml = f.read().replace('$friendlist$', friendlist)
    with open(blog_dir + '/friends.html', 'w', encoding='utf-8') as f:
        f.write(pagehtml)
