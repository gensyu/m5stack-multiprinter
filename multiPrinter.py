from m5stack import lcd

class Printer(object):
    def __init__(self, charset, fontset):
        self.charset_file = charset
        self.fontset_file = fontset
        self.ff_set = {}
        with open(self.charset_file, 'r', encoding='utf-8') as f:
            self.charset = f.read()

    def _get_ff(self, s):
        # 文字列から1文字ずつフォント情報取得
        uniq = sorted(set(s))
        for key in self.ff_set:
            try:
                uniq.remove(key)
            except:
                pass
        if len(uniq) > 0:
            self.ff_set.update(dict.fromkeys(uniq, b''))
            with open(self.fontset_file, 'rb') as f:
                for c in uniq:
                    pos = self.charset.find(c)
                    if pos < 0:
                        pos = 1
                    f.seek(pos * 2 * 13, 0)
                    self.ff_set[c] = f.read(13 * 2)

    def multiprint(self, s, base_x, base_y, scale=1):
        '''文字をM5StackのLCDに出力
        
        Arguments:
            s -- Strings
            base_x : int -- X出力基準位置
            base_y : int -- Y出力基準位置
        
        Keyword Arguments:
            scale {int} -- 文字大きさ (default: {1})
        
        Returns:
            [int] -- 文字列が使用するpixel数
        '''

        self._get_ff(s)
        for c in s:
            if ord(c) < 256:
                width = 7
            else:
                width = 15
            y = 0
            if base_x > 320:
                base_x = base_x + 2 * width
                continue
            for i in range(13):
                d = int.from_bytes(self.ff_set[c][2 * i:2 * (i + 1)], 'little')
                for x in range(width):
                    if base_x + x * 2 * scale < 0:
                        continue
                    if base_x + x * 2 * scale >= 320:
                        continue
                    if d >> (width - x) & 1 == 1:
                        lcd.rect(base_x + x * 2 * scale, base_y + y * 2,
                                 2 * scale, 2 * scale, 0xFFFFFF, 0xFFFFFF)
                        # print('@@', end='')
                    else:
                        lcd.rect(base_x + x * 2 * scale, base_y + y * 2,
                                 2 * scale, 2 * scale, 0x000000, 0x000000)
                        # print('  ', end='')
                # print('')
                y = y + scale
            base_x = base_x + 2 * scale * width
        return base_x

    def onelinePrint(self, s, base_x, base_y):
        lcd.rect(0, base_y, base_x, 26, 0x000000, 0x000000)
        x_pos = self.printStr(s, base_x, base_y, 2)
        width = 320 - x_pos
        if width > 0:
            lcd.rect(x_pos, base_y, width, 26, 0x000000, 0x000000)
        return x_pos

    def confirmPrint(self, s):
        '''出力確認用
        
        Arguments:
            s {[int]} -- Strings
        '''

        self._get_ff(s)
        for c in s:
            if ord(c) < 256:
                width = 7
            else:
                width = 15
            y = 0
            for i in range(13):
                d = int.from_bytes(self.ff_set[c][2 * i:2 * (i + 1)], 'little')
                for x in range(width):
                    if d >> (width - x) & 1 == 1:
                        print('@@', end='')
                    else:
                        print('  ', end='')
                print('')


def main():
    myprinter = Printer('./tools/mycharset.txt', './tools/fontset.bin')
    # myprinter.Print('Hello world!')
    # myprinter.Print('こんにちは')
    myprinter.Print('常用漢字もバッチリ！', 0, 0)
    # myprinter.confirmPrint('Hello world!')
    # myprinter.confirmPrint('こんにちは')
    # myprinter.confirmPrint('常用漢字もバッチリ！')


if __name__ == '__main__':
    main()
