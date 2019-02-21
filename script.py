import os
import requests
import sys

from collections import Counter

"""
usage(python3):

pip install requests
python script.py 201902W3
"""

folders = ['Algorithm', 'Review', 'Tip', 'Share']


def write_by_utf8(obj, text: str):
    obj.write(text.encode('utf8'))


def get_name(filename: str) -> str:
    """ 获取文件作者名"""
    return filename.split('-')[-1][:-3]


def get_achieve_goal_authors(week: str) -> list:
    """ 获取完成ARTS的作者名 """
    folders_authors = []
    for folder in folders:
        folder_authors = map(get_name, os.listdir(folder + '/' + week))
        folders_authors.extend(folder_authors)
    author_counts = Counter(folders_authors)  # 每个作者达成的个数
    achieve_authors = [name for name, count in author_counts.items() if int(count) > 3]  # 完成目标的作者
    return achieve_authors


def generate_image(size='1200x800', image_type='nature') -> str:
    """
    随机抓取一张unsplash的图片
    https://source.unsplash.com/
    """
    url = 'https://source.unsplash.com/{size}/?{type}'.format(size=size, type=image_type)
    try:
        image_url = requests.get(url, timeout=4).url
    except requests.exceptions.RequestException:
        print('Fetch image timeout, Retry or add images manually!')
        image_url = ''
    return image_url


def generate_partners(length, week: str) -> str:
    """ 生成Partners模块"""
    achieve_authors = get_achieve_goal_authors(week)
    text = '这是ARTS计划的第*{}*周，一共有*{}*位同学完成了目标\n\n'.format(length, len(achieve_authors))
    text += '## Partners\n\n'
    for author in achieve_authors:
        if author + '.md' in os.listdir('./Partners'):
            text += '[@{}](../{}/{})\n\n'.format(author, 'Partners', author+'.md')
        else:
            text += '@{}\n\n'.format(author)
    return text


def generate_folders(week: str) -> str:
    """ 生成ARTS模块"""
    text = ''
    for folder in folders:
        text += '## {}\n\n'.format(folder)
        if folder == 'Algorithm':
            text += '[这里](../Algorithm/{})\n\n'.format(week)
            continue
        files = os.listdir(folder + '/' + week)
        for file in files:
            text += '[{}](../{}/{}/{})\n\n'.format(file[:-3], folder, week, file.replace(' ', '%20'))
    return text


def main(week: str):
    length = len(os.listdir('./Weekly/'))
    if week + '.md' not in os.listdir('./Weekly'):
        length += 1
    image_url = generate_image()
    partners_text = generate_partners(length, week)
    arts_text = generate_folders(week)
    with open('./Weekly/' + week + '.md', 'ab') as md:
        write_by_utf8(md, '# Weekly #{}\n\n'.format(length))
        write_by_utf8(md, '![]({})\n\n'.format(image_url))
        write_by_utf8(md, partners_text)
        write_by_utf8(md, arts_text)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])