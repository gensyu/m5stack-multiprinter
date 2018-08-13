# coding: utf-8

charset = './mycharset.txt'
jp_bdf = './font/mplus_j12r.bdf'
en_bdf = './font/mplus_f12r.bdf'

shift_jis = []
jisx0208 = []
unicode = []
with open('./lib/JIS0208.TXT', 'r') as f:
    for line in f:
        if line[0] == '#':
            pass
        else:
            sjis, jisx, unic, _ = line.strip().split('\t')
            shift_jis.append(int(sjis,16))
            jisx0208.append( int(jisx,16))
            unicode.append(int(unic,16))

def jis2uni(n):
    return unicode[jisx0208.index(n)]

def jpbdf2dict(filename):
    convert_flag = False
    dataline_flag = False
    dotlist = []
    text_dict = {}
    s = ''
    with open(filename, 'r') as f:
        for line in f:    
            if line.startswith('STARTCHAR'):
                jiscode = int(line.strip().split(' ')[1], 16)
                convert_flag = True
                try:
                    s = chr(jis2uni(jiscode))
                except :
                    convert_flag = False
                    continue
            if line.startswith('ENDCHAR'):
                if convert_flag:
                    text_dict[s] = dotlist
                dataline_flag = False
                convert_flag = False
                dotlist = []

            if dataline_flag and convert_flag:
                dotlist.append(int(line, 16))

            if line.startswith('BITMAP'):
                dataline_flag = True
    return text_dict

def bdf2dict(filename):
    convert_flag = False
    dataline_flag = False
    dotlist = []
    text_dict = {}
    s = ''
    with open(filename, 'r') as f:
        for line in f:    
            if line.startswith('STARTCHAR'):
                code = int(line.strip().split(' ')[1], 16)
                convert_flag = True
                s = chr(code)
            if line.startswith('ENDCHAR'):
                if convert_flag:
                    text_dict[s] = dotlist
                dataline_flag = False
                convert_flag = False
                dotlist = []

            if dataline_flag and convert_flag:
                dotlist.append(int(line, 16))

            if line.startswith('BITMAP'):
                dataline_flag = True
    return text_dict

def main():
    # フォントファイルからデータ取得
    jp_font = jpbdf2dict(jp_bdf)
    alphabet = bdf2dict(en_bdf)
    
    fontdata  = {}
    fontdata.update(jp_font)
    fontdata.update(alphabet)

    # 文字セットファイル読み込み
    with open(charset, 'r', encoding='utf-8') as f:
        fontset = f.read()
        fontset = [x for x in fontset]
    
    # 並べ替えて保存
    fontset.sort()
    with open('../data/charset.text', 'w', encoding='utf-8') as f:
        f.write(''.join(fontset))

    # 文字セットファイルからバイナリファイル出力
    with open('../data/fontset.bin', 'wb') as f:
        for i, key in enumerate(fontset):
            for val in fontdata[key]:
                f.write(val.to_bytes(2, 'little'))


if __name__ == '__main__':
    main()    