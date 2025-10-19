import json
import re
from datetime import datetime, timezone, timedelta
from urllib.parse import quote
import xml.etree.ElementTree as ET

TZ = timezone(timedelta(hours=8))

# 新增：解析创作时间与更新时间
def parse_published_updated(text: str):
    pub = None
    upd = None
    m_pub = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', text)
    if m_pub:
        try:
            y, mth, d = map(int, m_pub.groups())
            pub = datetime(y, mth, d, tzinfo=TZ)
        except ValueError:
            pub = None
    m_upd = re.search(r'（(\d{4})\.(\d{1,2})\.(\d{1,2})更新）', text)
    if m_upd:
        try:
            y, mth, d = map(int, m_upd.groups())
            upd = datetime(y, mth, d, tzinfo=TZ)
        except ValueError:
            upd = None
    if upd is None:
        upd = pub
    return pub, upd

def load_passages(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
    for item in data:
        pub, upd = parse_published_updated(item.get('date', ''))
        item['published'] = pub
        item['updated'] = upd
    return data

def build_feed(passages, blog_author, blog_title, blog_url, categories):
    feed = ET.Element('feed', attrib={'xmlns': 'http://www.w3.org/2005/Atom'})
    title = ET.SubElement(feed, 'title')
    title.text = blog_title

    fid = ET.SubElement(feed, 'id')
    fid.text = blog_url + '/'

    updated = ET.SubElement(feed, 'updated')
    if passages:
        updated.text = passages[0]['updated'].isoformat()
    else:
        updated.text = datetime.now(TZ).isoformat()

    for p in passages:
        entry = ET.SubElement(feed, 'entry')
        etitle = ET.SubElement(entry, 'title')
        etitle.text = p['name']

        eauthor = ET.SubElement(entry, 'author')
        aname = ET.SubElement(eauthor, 'name')
        aname.text = blog_author

        href = f"/html/{quote(p['name'])}.html"
        ET.SubElement(entry, 'link', attrib={'href': href})

        idt = f"{blog_url}/html/{quote(p['name'])}.html"
        eid = ET.SubElement(entry, 'id')
        eid.text = idt

        ET.SubElement(entry, 'category', attrib={'term': categories.get(p.get('category', ''), '')})

        eupdated = ET.SubElement(entry, 'updated')
        eupdated.text = p['updated'].isoformat()

        epublished = ET.SubElement(entry, 'published')
        epublished.text = p['published'].isoformat()

        esummary = ET.SubElement(entry, 'summary')
        esummary.text = p.get('abstract', '')


    return feed

def write_feed(feed, out_path):
    from xml.dom import minidom
    xml_bytes = ET.tostring(feed, encoding='utf-8')
    dom = minidom.parseString(xml_bytes)
    pretty_bytes = dom.toprettyxml(indent='  ', encoding='utf-8')
    with open(out_path, 'wb') as f:
        f.write(pretty_bytes)

def execute(blog_dir, pc_dir, blog_author, blog_title, blog_url, categories):
    json_path = f'{pc_dir}/passages.json'
    out_path = f'{blog_dir}/extra/atom.xml'

    passages = load_passages(json_path)
    feed = build_feed(passages, blog_author, blog_title, blog_url, categories)
    write_feed(feed, out_path)