# 모듈
import pandas
import os
import re
import tqdm

# 폴더
DIR_WORD = './word/'   # 최종 txt 파일 저장 폴더
if not os.path.exists(DIR_WORD): os.mkdir(DIR_WORD)

# 함수 정의

# 엑셀 처리후 txt로 변환
def ETT(excel):
    if not os.path.exists(DIR_WORD + 'ETT/'): os.mkdir(DIR_WORD + 'ETT/')
    data = pandas.read_excel('./dic/'+ excel)                                       # 표준국어대사전 엑셀파일 경로
    row = data.iloc[:, :3]
    col = row[((row['구성 단위'] == '단어') & (row['고유어 여부'] == '고유어')) | ((row['구성 단위'] == '단어') & (row['고유어 여부'] == '한자어'))]
    col = col.rename(columns={'어휘': '가'})
    txt = col.iloc[:, :1]
    txt.to_csv(DIR_WORD + 'ETT/' + excel[:-5] + '.txt', index=0)

# 2글자인 한글단어 제외한 모든 문자 제거
def clean_txt(txt_file):
    if not os.path.exists(DIR_WORD + 'clean_txt'): os.mkdir(DIR_WORD + 'clean_txt')
    with open(DIR_WORD + 'ETT/' + txt_file, mode='r', encoding='utf-8') as txt:
        with open(DIR_WORD + 'clean_txt/' + txt_file, mode='w', encoding='utf-8') as txt2:
            while True:
                word = txt.readline()
                word = re.sub('[^가-힣]', '', word)
                if len(word)==2:
                    txt2.write(word + '\n')
                elif not word: break

# 중복제거
def set_txt(txt_file):
    if not os.path.exists(DIR_WORD + 'set_txt'): os.mkdir(DIR_WORD + 'set_txt')
    with open(DIR_WORD + 'clean_txt/' + txt_file, mode='r', encoding='utf-8') as txt:
        with open(DIR_WORD + 'set_txt/' + txt_file, mode='w', encoding='utf-8') as txt2:
            txtList = list(set(txt.readlines()))
            txtList.sort()
            for i in txtList: txt2.write(i)

# 초성 판별 후 ㄱㄱ~ㅎㅎ.txt에 각각 저장
def chosung_txt(txt_file):
    chosungList = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    with open(DIR_WORD + 'set_txt/' + txt_file, mode='r', encoding='utf-8') as txt:
        while True:
            word = txt.readline().strip()
            chosung1 = ''
            if not word: break
            else:
                for i in list(word):
                    code = ((ord(i) - ord('가')) // 588)
                    chosung1 += chosungList[code]
                with open(DIR_WORD + chosung1 + '.txt', mode='a', encoding='utf-8') as txt2:
                    txt2.write(word + '\n')

# 기능 구현
if len(os.listdir(DIR_WORD)) != 351:
    excelList = os.listdir('./dic/')
    for i in tqdm.tqdm(excelList, desc='Loading... ', ncols=80,unit='단어'):
        ETT(i)
        i = i[:-5] + '.txt'
        clean_txt(i)
        set_txt(i)
        chosung_txt(i)

    # 필요없는 파일,폴더 삭제
    reList = os.listdir(DIR_WORD)
    dirlist = []
    for i in reList:
        if not '.txt' in i:
            dirlist += [i]
    for i in dirlist:
        for j in os.listdir(DIR_WORD + i):
            os.remove(DIR_WORD + i + '/' + j)
        os.rmdir(DIR_WORD + i)


