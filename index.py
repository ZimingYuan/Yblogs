import sys
import json

def execute(pc_dir, blog_dir, blog_title, categories):
    perpage = 10
    title = '{} - {}（第{}页）'
    data_dict = {i: [] for i in categories.keys()}
    data_dict['index'] = []
    categories['index'] = '主页'
    with open(pc_dir + '/passages.json', 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
        for i in data:
            data_dict[i['category']].append(i)
            data_dict['index'].append(i)
        
    for category, data in data_dict.items():
        total = (len(data) + perpage - 1) // perpage
        url = [f'/{category}.html']
        for i in range(1, total):
            url.append(f'/{category}/{i + 1}.html')
        with open(pc_dir + f'/{category}.html', 'r', encoding='utf-8') as f:
            html = f.read()
        for page in range(total):
            pagehtml = html.replace('$title$', title.format(blog_title, categories[category], page + 1))
            slic = data[page * perpage:min((page + 1) * perpage, len(data))]
            bloglist = ''
            for i in slic:
                bloglist += f'''
<div class="card">
    <h4><a href="/html/{i['name']}.html">{i['name']}</a></h4><hr>
    <p>{i['abstract']}</p>
    <em>
    <svg width="1em" height="1em" viewBox="0 0 35 35" data-name="Layer 2" id="e73e2821-510d-456e-b3bd-9363037e93e3" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"><path d="M11.933,15.055H3.479A3.232,3.232,0,0,1,.25,11.827V3.478A3.232,3.232,0,0,1,3.479.25h8.454a3.232,3.232,0,0,1,3.228,3.228v8.349A3.232,3.232,0,0,1,11.933,15.055ZM3.479,2.75a.73.73,0,0,0-.729.728v8.349a.73.73,0,0,0,.729.728h8.454a.729.729,0,0,0,.728-.728V3.478a.729.729,0,0,0-.728-.728Z"></path><path d="M11.974,34.75H3.52A3.233,3.233,0,0,1,.291,31.521V23.173A3.232,3.232,0,0,1,3.52,19.945h8.454A3.232,3.232,0,0,1,15.2,23.173v8.348A3.232,3.232,0,0,1,11.974,34.75ZM3.52,22.445a.73.73,0,0,0-.729.728v8.348a.73.73,0,0,0,.729.729h8.454a.73.73,0,0,0,.728-.729V23.173a.729.729,0,0,0-.728-.728Z"></path><path d="M31.522,34.75H23.068a3.233,3.233,0,0,1-3.229-3.229V23.173a3.232,3.232,0,0,1,3.229-3.228h8.454a3.232,3.232,0,0,1,3.228,3.228v8.348A3.232,3.232,0,0,1,31.522,34.75Zm-8.454-12.3a.73.73,0,0,0-.729.728v8.348a.73.73,0,0,0,.729.729h8.454a.73.73,0,0,0,.728-.729V23.173a.729.729,0,0,0-.728-.728Z"></path><path d="M27.3,15.055a7.4,7.4,0,1,1,7.455-7.4A7.437,7.437,0,0,1,27.3,15.055Zm0-12.3a4.9,4.9,0,1,0,4.955,4.9A4.935,4.935,0,0,0,27.3,2.75Z"></path></g></svg>
    {categories[i['category']]}
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <svg width="1em" height="1em" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path d="M3 9H21M7 3V5M17 3V5M6 13H8M6 17H8M11 13H13M11 17H13M16 13H18M16 17H18M6.2 21H17.8C18.9201 21 19.4802 21 19.908 20.782C20.2843 20.5903 20.5903 20.2843 20.782 19.908C21 19.4802 21 18.9201 21 17.8V8.2C21 7.07989 21 6.51984 20.782 6.09202C20.5903 5.71569 20.2843 5.40973 19.908 5.21799C19.4802 5 18.9201 5 17.8 5H6.2C5.0799 5 4.51984 5 4.09202 5.21799C3.71569 5.40973 3.40973 5.71569 3.21799 6.09202C3 6.51984 3 7.07989 3 8.2V17.8C3 18.9201 3 19.4802 3.21799 19.908C3.40973 20.2843 3.71569 20.5903 4.09202 20.782C4.51984 21 5.07989 21 6.2 21Z" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </g></svg>
    {i['date']}
    </em>
</div>
'''
            bloglist += '<div style="padding-top: 2em; text-align: center">\n'
            if page > 0:
                bloglist += f'<a href="{url[page - 1]}"><button style="padding: 0.4em 0.8em; margin: 0; border-radius: 50%; border: none">&lt;</button></a>\n'
            buttonlist = []
            for i in range(total):
                if i == page:
                    buttonlist.append(f'<button disabled style="padding: 0.4em; width: 2.3em; margin: 0; border-radius: 50%">{i + 1}</button>')
                else:
                    buttonlist.append(f'<a href="{url[i]}"><button style="padding: 0.4em; width: 2.3em; margin: 0; border-radius: 50%; border: none">{i + 1}</button></a>')
            if page - 1 > 1:
                buttonlist = [buttonlist[0], '...'] + buttonlist[page - 1:]
                tmppage = 3
            else:
                tmppage = page
            if len(buttonlist) - 1 - (tmppage + 1) > 1:
                buttonlist = buttonlist[:tmppage + 2] + ['...', buttonlist[-1]]
            bloglist += '\n'.join(buttonlist) + '\n'
            if page < total - 1:
                bloglist += f'<a href="{url[page + 1]}"><button style="padding: 0.4em 0.8em; margin: 0; border-radius: 50%; border: none">&gt;</button></a>\n'
            bloglist += '</div>\n'
            pagehtml = pagehtml.replace('$bloglist$', bloglist)
            with open(blog_dir + url[page], 'w', encoding='utf-8') as f:
                f.write(pagehtml)
