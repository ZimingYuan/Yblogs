import sys
import json

def execute(pc_dir, blog_dir, categories):
    perpage = 10
    title = '我的博客（第{}页）'
    data_dict = {i: [] for i in categories}
    with open(pc_dir + '/passages.json', 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
        for i in data:
            data_dict[i['category']].append(i)
    for category, data in data_dict.items():
        total = (len(data) + perpage - 1) // perpage
        url = [f'/{category}.html']
        for i in range(1, total):
            url.append(f'/{category}/{i + 1}.html')
        with open(pc_dir + f'/{category}.html', 'r', encoding='utf-8') as f:
            html = f.read()
        for page in range(total):
            pagehtml = html.replace('$title$', title.format(page + 1))
            slic = data[page * perpage:min((page + 1) * perpage, len(data))]
            bloglist = ''
            for i in slic:
                bloglist += f'''
<div class="card">
    <h4><a href="/html/{i['name']}.html">{i['name']}</a></h4><hr>
    <p>{i['abstract']}</p>
    <em>{i['date']}</em>
</div>
'''
            bloglist += '<div style="padding-top: 2em; text-align: center">\n'
            for i in range(total):
                if i == page:
                    bloglist += f'<button disabled style="padding: 0.2em 0.6em; margin: 0.1em">{i + 1}</button>\n'
                else:
                    bloglist += f'<a href="{url[i]}"><button style="padding: 0.2em 0.6em; margin: 0.1em">{i + 1}</button></a>\n'
            bloglist += '</div>\n'
            pagehtml = pagehtml.replace('$bloglist$', bloglist)
            with open(blog_dir + url[page], 'w', encoding='utf-8') as f:
                f.write(pagehtml)
