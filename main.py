import cv2
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import pandas as pd
from tqdm import tqdm
import os

#delete export img
for d in os.listdir('export/'):
    os.remove(os.path.join('export/', d))

#page color
page_dark = 'pages/page_dark.jpg'
page_yellow = 'pages/page_yellow.jpg'
page_white = 'pages/page_white.jpg'

#font style
fontpath = 'fonts/NanumSquareR.ttf'
japanese_fontpath = 'fonts/GenShinGothic-Heavy.ttf'

#font color
white = 255, 255, 255
black = 0, 0, 0

#font size
q_font = ImageFont.truetype(japanese_fontpath, 400)
a_font = ImageFont.truetype(fontpath, 200)
hiragana_font = ImageFont.truetype(japanese_fontpath, 100)

#text position
question_position = 1251, 807
answer_position = 1251, 2423
hiragana_position = 1251, 370

f = open('database.csv', 'r', encoding='UTF8')
lines = f.readlines()
df = pd.DataFrame(lines)

row = 0
filecount = 1

for i in tqdm(range(len(df)), desc='image processing'):
    q_column = lines[row].split(",")[0]
    a_column = lines[row].split(",")[1]
    hiragana_column = lines[row].split(",")[2]

    q_text = q_column
    a_text = a_column
    hiragana_text = hiragana_column

    img = cv2.imread(page_dark, cv2.IMREAD_COLOR)
    img = Image.fromarray(img)
    draw = ImageDraw.Draw(img)
    draw.text((question_position), q_text, font=q_font, fill=(white), anchor='ms')
    draw.text((answer_position), a_text, font=a_font, fill=(white), anchor='ms')
    draw.text((hiragana_position), hiragana_text, font=hiragana_font, fill=(white), anchor='ms')

    img = np.array(img)

    cv2.imwrite('export/{}.png'.format(filecount), img)

    row = row + 1
    filecount = filecount + 1

    if i > len(df):
        break

#make PDF
path_dir = 'export/'
file_list = os.listdir(path_dir)
img_list = []
img_path = 'export/'+file_list[0];
im_buf = Image.open(img_path)
cvt_rgb_0 = im_buf.convert('RGB')
for j in tqdm(file_list, desc='PDF exporting'):
    img_path = 'export/' + j;
    im_buf = Image.open(img_path)
    cvt_rgb = im_buf.convert('RGB')
    img_list.append(cvt_rgb)
del img_list[0]
cvt_rgb_0.save('export.pdf', save_all=True, append_images=img_list)

print('Export to PDF completed.')
os.system('pause')