import os
import glob
import shutil

blog_dir = 'myblog'
md_dir = 'markdown'
pc_dir = 'process'
force_html = False
force_img = False

if not os.path.exists(blog_dir):
    print('mkdir ' + blog_dir)
    os.mkdir(blog_dir)
htmlf = blog_dir + '/html'
if not os.path.exists(htmlf):
    print('mkdir ' + htmlf)
    os.mkdir(htmlf)
for i in glob.glob(md_dir + '/*.md'):
    mtime = os.path.getmtime(i)
    html = blog_dir + '/html/' + i[len(md_dir) + 1:-3] + '.html'
    if force_html or not os.path.exists(html) or mtime > os.path.getmtime(html):
        command = f'pandoc --template={pc_dir}/template.html -c /extra/classless.css --mathjax {i} -o {html}'
        print(command)
        os.system(command)

if not os.path.exists(blog_dir + '/img'):
    print(f'cp {md_dir}/img {blog_dir}')
    shutil.copytree(md_dir + '/img', blog_dir + '/img')
else:
    for i in glob.glob(md_dir + '/img/*'):
        img = blog_dir + i[len(md_dir):]
        if force_img or not os.path.exists(img) or mtime > os.path.getmtime(img):
            print(f'cp {i} {img}')
            shutil.copy(i, img)

extraf = blog_dir + '/extra'
if not os.path.exists(extraf):
    print('mkdir ' + extraf)
    os.mkdir(extraf)
print(f'cp {pc_dir}/classless.css {blog_dir}/extra')
shutil.copy(pc_dir + '/classless.css', blog_dir + '/extra')
print(f'cp {pc_dir}/passages.json {blog_dir}/extra')
shutil.copy(pc_dir + '/passages.json', blog_dir + '/extra')
print(f'cp {pc_dir}/search.html {blog_dir}')
shutil.copy(pc_dir + '/search.html', blog_dir)

categories = ['index']
for i in categories:
    indexf = blog_dir + '/' + i
    if not os.path.exists(indexf):
        print('mkdir ' + indexf)
        os.mkdir(indexf)
print('execute index.py')
from index import execute
execute(pc_dir, blog_dir, categories)
print('execute friends.py')
from friends import execute
execute(pc_dir, blog_dir)
