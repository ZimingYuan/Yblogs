import sys
import json

def execute(pc_dir, blog_dir):
    perpage = 10
    title = '我的博客首页（第{}页）'
    f = open(pc_dir + '/passages.json', 'r', encoding='utf-8')
    data = json.loads(f.read())
    f.close()
    total = (len(data) + perpage - 1) // perpage
    url = ['/index.html']
    for i in range(1, total):
        url.append(f'/index/{i + 1}.html')
    f = open(pc_dir + '/index.html', 'r', encoding='utf-8')
    html = f.read()
    f.close()
    for page in range(total):
        pagehtml = html.replace('$title$', title.format(page + 1))
        slic = data[page * perpage:min((page + 1) * perpage, len(data))]
        bloglist = ''
        for i in slic:
            bloglist += f'''
<div class="card">
    <h4><a href="/html/{i['name']}.html">{i['name']}</a></h4><hr>
    <h5>摘要：</h5><p>{i['abstract']}</p>
    <em>{i['date']}</em>
</div>
'''
        for i in range(total):
            if i == page:
                bloglist += f'<button disabled>{i + 1}</button>\n'
            else:
                bloglist += f'<a href="{url[i]}"><button>{i + 1}</button></a>\n'
        pagehtml = pagehtml.replace('$bloglist$', bloglist)
        f = open(blog_dir + url[page], 'w', encoding='utf-8')
        f.write(pagehtml)
        f.close()
