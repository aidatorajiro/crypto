# MONOALPHABETIC SUBSTITUTION SOLVING HELPER!
# This program can be used to decide whether the ciphertext is using monoalphabetic substitution and to decrypt it.

# Vectorize each character of monoalphabetic substitution ciphertext (the corpuses of encrypted text) and plaintext (random Japanese corpuses of romaji expression), then compare the vectors.

# You have to download https://github.com/ku-nlp/KWDLC in order to run this program.

# the constant kanamap is derived from https://github.com/jikyo/romaji4p/blob/master/romaji/mapping.py (Copyright 2018 Junnosuke Moriya)
# original code is licensed under Apache License 2.0
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0

import glob
from mono_kana_setting import cipher_char_whitelist

kanamap = {
    'あ': 'a',
    'い': 'i',
    'う': 'u',
    'え': 'e',
    'お': 'o',
    'うぁ': 'wha',
    'うぃ': 'whi',
    'うぇ': 'whe',
    'うぉ': 'who',
    'ゐ': 'wi',
    'ゑ': 'we',
    'ぁ': 'xa',
    'ぃ': 'xi',
    'ぅ': 'xu',
    'ぇ': 'xe',
    'ぉ': 'xo',
    'いぇ': 'ye',
    'か': 'ka',
    'き': 'ki',
    'く': 'ku',
    'け': 'ke',
    'こ': 'ko',
    'きゃ': 'kya',
    'きぃ': 'kyi',
    'きゅ': 'kyu',
    'きぇ': 'kye',
    'きょ': 'kyo',
    'くゃ': 'qya',
    'くゅ': 'qyu',
    'くょ': 'quo',
    'くぁ': 'qwa',
    'くぃ': 'qwi',
    'くぅ': 'qwu',
    'くぇ': 'qwe',
    'くぉ': 'qwo',
    'が': 'ga',
    'ぎ': 'gi',
    'ぐ': 'gu',
    'げ': 'ge',
    'ご': 'go',
    'ぎゃ': 'gya',
    'ぎぃ': 'gyi',
    'ぎゅ': 'gyu',
    'ぎぇ': 'gye',
    'ぎょ': 'gyo',
    'ぐぁ': 'gwa',
    'ぐぃ': 'gwi',
    'ぐぅ': 'gwu',
    'ぐぇ': 'gwe',
    'ぐぉ': 'gwo',
    'さ': 'sa',
    'し': 'si',
    'す': 'su',
    'せ': 'se',
    'そ': 'so',
    'しゃ': 'sya',
    'しぃ': 'syi',
    'しゅ': 'syu',
    'しぇ': 'sye',
    'しょ': 'syo',
    'すぁ': 'swa',
    'すぃ': 'swi',
    'すぅ': 'swu',
    'すぇ': 'swe',
    'すぉ': 'swo',
    'ざ': 'za',
    'じ': 'zi',
    'ず': 'zu',
    'ぜ': 'ze',
    'ぞ': 'zo',
    'じゃ': 'zya',
    'じぃ': 'zyi',
    'じゅ': 'zyu',
    'じぇ': 'zye',
    'じょ': 'zyo',
    'た': 'ta',
    'ち': 'ti',
    'つ': 'tu',
    'て': 'te',
    'と': 'to',
    'ちゃ': 'tya',
    'ちぃ': 'tyi',
    'ちゅ': 'tyu',
    'ちぇ': 'tye',
    'ちょ': 'tyo',
    'つぁ': 'tsa',
    'つぃ': 'tsi',
    'つぇ': 'tse',
    'つぉ': 'tso',
    'てゃ': 'tha',
    'てぃ': 'thi',
    'てゅ': 'thu',
    'てぇ': 'the',
    'てょ': 'tho',
    'とぁ': 'twa',
    'とぃ': 'twi',
    'とぅ': 'twu',
    'とぇ': 'twe',
    'とぉ': 'two',
    'だ': 'da',
    'ぢ': 'di',
    'づ': 'du',
    'で': 'de',
    'ど': 'do',
    'ぢゃ': 'dya',
    'ぢぃ': 'dyi',
    'ぢゅ': 'dyu',
    'ぢぇ': 'dye',
    'ぢょ': 'dyo',
    'でゃ': 'dha',
    'でぃ': 'dhi',
    'でゅ': 'dhu',
    'でぇ': 'dhe',
    'でょ': 'dho',
    'どぁ': 'dwa',
    'どぃ': 'dwi',
    'どぅ': 'dwu',
    'どぇ': 'dwe',
    'どぉ': 'dwo',
    'っ': 'xtu',
    'な': 'na',
    'に': 'ni',
    'ぬ': 'nu',
    'ね': 'ne',
    'の': 'no',
    'にゃ': 'nya',
    'にぃ': 'nyi',
    'にゅ': 'nyu',
    'にぇ': 'nye',
    'にょ': 'nyo',
    'は': 'ha',
    'ひ': 'hi',
    'ふ': 'hu',
    'へ': 'he',
    'ほ': 'ho',
    'ひゃ': 'hya',
    'ひぃ': 'hyi',
    'ひゅ': 'hyu',
    'ひぇ': 'hye',
    'ひょ': 'hyo',
    'ふぁ': 'fwa',
    'ふぃ': 'fwi',
    'ふぅ': 'fwu',
    'ふぇ': 'fwe',
    'ふぉ': 'fwo',
    'ふゃ': 'fya',
    'ふゅ': 'fyu',
    'ふょ': 'fyo',
    'ば': 'ba',
    'び': 'bi',
    'ぶ': 'bu',
    'べ': 'be',
    'ぼ': 'bo',
    'びゃ': 'bya',
    'びぃ': 'byi',
    'びゅ': 'byu',
    'びぇ': 'bye',
    'びょ': 'byo',
    'ぱ': 'pa',
    'ぴ': 'pi',
    'ぷ': 'pu',
    'ぺ': 'pe',
    'ぽ': 'po',
    'ぴゃ': 'pya',
    'ぴぃ': 'pyi',
    'ぴゅ': 'pyu',
    'ぴぇ': 'pye',
    'ぴょ': 'pyo',
    'ま': 'ma',
    'み': 'mi',
    'む': 'mu',
    'め': 'me',
    'も': 'mo',
    'みゃ': 'mya',
    'みぃ': 'myi',
    'みゅ': 'myu',
    'みぇ': 'mye',
    'みょ': 'myo',
    'や': 'ya',
    'ゆ': 'yu',
    'よ': 'yo',
    'ゃ': 'xya',
    'ゅ': 'xyu',
    'ょ': 'xyo',
    'ら': 'ra',
    'り': 'ri',
    'る': 'ru',
    'れ': 're',
    'ろ': 'ro',
    'りゃ': 'rya',
    'りぃ': 'ryi',
    'りゅ': 'ryu',
    'りぇ': 'rye',
    'りょ': 'ryo',
    'わ': 'wa',
    'を': 'wo',
    'ん': 'n',
    'ゎ': 'xwa',
    'ア': 'a',
    'イ': 'i',
    'ウ': 'u',
    'エ': 'e',
    'オ': 'o',
    'ウァ': 'wha',
    'ウィ': 'whi',
    'ウェ': 'whe',
    'ウォ': 'who',
    'ヰ': 'wi',
    'ヱ': 'we',
    'ァ': 'xa',
    'ィ': 'xi',
    'ゥ': 'xu',
    'ェ': 'xe',
    'ォ': 'xo',
    'イェ': 'ye',
    'カ': 'ka',
    'キ': 'ki',
    'ク': 'ku',
    'ケ': 'ke',
    'コ': 'ko',
    'キャ': 'kya',
    'キィ': 'kyi',
    'キュ': 'kyu',
    'キェ': 'kye',
    'キョ': 'kyo',
    'クャ': 'qya',
    'クュ': 'qyu',
    'クョ': 'quo',
    'クァ': 'qwa',
    'クィ': 'qwi',
    'クゥ': 'qwu',
    'クェ': 'qwe',
    'クォ': 'qwo',
    'ガ': 'ga',
    'ギ': 'gi',
    'グ': 'gu',
    'ゲ': 'ge',
    'ゴ': 'go',
    'ギャ': 'gya',
    'ギィ': 'gyi',
    'ギュ': 'gyu',
    'ギェ': 'gye',
    'ギョ': 'gyo',
    'グァ': 'gwa',
    'グィ': 'gwi',
    'グゥ': 'gwu',
    'グェ': 'gwe',
    'グォ': 'gwo',
    'ヵ': 'xka',
    'ヶ': 'xke',
    'サ': 'sa',
    'シ': 'si',
    'ス': 'su',
    'セ': 'se',
    'ソ': 'so',
    'シャ': 'sya',
    'シィ': 'syi',
    'シュ': 'syu',
    'シェ': 'sye',
    'ショ': 'syo',
    'スァ': 'swa',
    'スィ': 'swi',
    'スゥ': 'swu',
    'スェ': 'swe',
    'スォ': 'swo',
    'ザ': 'za',
    'ジ': 'zi',
    'ズ': 'zu',
    'ゼ': 'ze',
    'ゾ': 'zo',
    'ジャ': 'zya',
    'ジィ': 'zyi',
    'ジュ': 'zyu',
    'ジェ': 'zye',
    'ジョ': 'zyo',
    'タ': 'ta',
    'チ': 'ti',
    'ツ': 'tu',
    'テ': 'te',
    'ト': 'to',
    'チャ': 'tya',
    'チィ': 'tyi',
    'チュ': 'tyu',
    'チェ': 'tye',
    'チョ': 'tyo',
    'ツァ': 'tsa',
    'ツィ': 'tsi',
    'ツェ': 'tse',
    'ツォ': 'tso',
    'テャ': 'tha',
    'ティ': 'thi',
    'テュ': 'thu',
    'テェ': 'the',
    'テョ': 'tho',
    'トァ': 'twa',
    'トィ': 'twi',
    'トゥ': 'twu',
    'トェ': 'twe',
    'トォ': 'two',
    'ダ': 'da',
    'ヂ': 'di',
    'ヅ': 'du',
    'デ': 'de',
    'ド': 'do',
    'ヂャ': 'dya',
    'ヂィ': 'dyi',
    'ヂュ': 'dyu',
    'ヂェ': 'dye',
    'ヂョ': 'dyo',
    'デャ': 'dha',
    'ディ': 'dhi',
    'デュ': 'dhu',
    'デェ': 'dhe',
    'デョ': 'dho',
    'ドァ': 'dwa',
    'ドィ': 'dwi',
    'ドゥ': 'dwu',
    'ドェ': 'dwe',
    'ドォ': 'dwo',
    'ッ': 'xtu',
    'ナ': 'na',
    'ニ': 'ni',
    'ヌ': 'nu',
    'ネ': 'ne',
    'ノ': 'no',
    'ニャ': 'nya',
    'ニィ': 'nyi',
    'ニュ': 'nyu',
    'ニェ': 'nye',
    'ニョ': 'nyo',
    'ハ': 'ha',
    'ヒ': 'hi',
    'フ': 'hu',
    'ヘ': 'he',
    'ホ': 'ho',
    'ヒャ': 'hya',
    'ヒィ': 'hyi',
    'ヒュ': 'hyu',
    'ヒェ': 'hye',
    'ヒョ': 'hyo',
    'ファ': 'fwa',
    'フィ': 'fwi',
    'フゥ': 'fwu',
    'フェ': 'fwe',
    'フォ': 'fwo',
    'フャ': 'fya',
    'フュ': 'fyu',
    'フョ': 'fyo',
    'バ': 'ba',
    'ビ': 'bi',
    'ブ': 'bu',
    'ベ': 'be',
    'ボ': 'bo',
    'ビャ': 'bya',
    'ビィ': 'byi',
    'ビュ': 'byu',
    'ビェ': 'bye',
    'ビョ': 'byo',
    'パ': 'pa',
    'ピ': 'pi',
    'プ': 'pu',
    'ペ': 'pe',
    'ポ': 'po',
    'ピャ': 'pya',
    'ピィ': 'pyi',
    'ピュ': 'pyu',
    'ピェ': 'pye',
    'ピョ': 'pyo',
    'ヴァ': 'va',
    'ヴィ': 'vi',
    'ヴ': 'vu',
    'ヴェ': 've',
    'ヴォ': 'vo',
    'ヴャ': 'vya',
    'ヴュ': 'vyu',
    'ヴョ': 'vyo',
    'マ': 'ma',
    'ミ': 'mi',
    'ム': 'mu',
    'メ': 'me',
    'モ': 'mo',
    'ミャ': 'mya',
    'ミィ': 'myi',
    'ミュ': 'myu',
    'ミェ': 'mye',
    'ミョ': 'myo',
    'ヤ': 'ya',
    'ユ': 'yu',
    'ヨ': 'yo',
    'ャ': 'xya',
    'ュ': 'xyu',
    'ョ': 'xyo',
    'ラ': 'ra',
    'リ': 'ri',
    'ル': 'ru',
    'レ': 're',
    'ロ': 'ro',
    'リャ': 'rya',
    'リィ': 'ryi',
    'リュ': 'ryu',
    'リェ': 'rye',
    'リョ': 'ryo',
    'ワ': 'wa',
    'ヲ': 'wo',
    'ン': 'n',
    'ヮ': 'xwa',
}

def make_char_to_index_table(text):
    chars = sorted(set(text))
    table = {}
    for i in range(len(chars)):
        table[chars[i]] = i
    return chars, table

plain_chars, plain_table = make_char_to_index_table(''.join(kanamap.values()))
cipher_chars, cipher_table = make_char_to_index_table(cipher_char_whitelist)
assert len(plain_table) == len(cipher_table)
num_chars = len(plain_table)

def kana_to_romaji(kana):
    i = 0
    out = ''
    while True:
        segment = kana[i:i+2]
        if segment == '':
            break
        if segment in kanamap:
            out += kanamap[segment]
            i += 2
            continue
        segment = kana[i:i+1]
        if segment == '':
            break
        if segment in kanamap:
            out += kanamap[segment]
            i += 1
            continue
        i += 1
    return out

def learn(mat, corps, table):
    for line in corps:
        for i in range(1, len(line) - 1):
            for (x, y) in [(i - 1, i),(i + 1, i)]:
                mat[table[line[x]], table[line[y]]] += 1
                mat[table[line[y]], table[line[x]]] += 1

import numpy as np

from sklearn.decomposition import PCA

import matplotlib.pyplot as plt

#def normalize(mat):
#    return (mat - mat.mean(1).reshape(mat.shape[0],1)) / (mat.std(1).reshape(mat.shape[0],1))

def normalize(mat):
    return (mat - mat.mean()) / (mat.std())

if __name__ == '__main__':
    
    with open("mono_kana_cipher.txt") as f:
        corps_cipher = (''.join([c for c in f.read() if c in cipher_chars or c == '\n'])).split('\n')
    
    corps_plain = []
    for filename in glob.glob('KWDLC/knp/*/*'):
        with open(filename) as f:
            for line in f:
                if not (line == 'EOS\n' or line[0] == '#' or line[0] == '+' or line[0] == '*'):
                    kana = line.split(' ')[1]
                    corps_plain.append(kana_to_romaji(kana))
    
    mats = []
    
    args = [[corps_cipher, cipher_table, cipher_chars], [corps_plain, plain_table, plain_chars]]
    
    for corps, table, chars in args:
        mat = np.zeros((num_chars,num_chars),dtype=np.float32)
        
        learn(mat, corps, table)
        
        mat = normalize(mat)
        
        mats.append(mat)
    
    pca = PCA(n_components=2)
    
    mats_reduced = pca.fit_transform(np.concatenate(mats))
    
    for i in range(len(args)):
        plt.scatter(mats_reduced[(i)*num_chars:(i + 1)*num_chars,:][:,0], mats_reduced[(i)*num_chars:(i + 1)*num_chars,:][:,1])
    
    print(mats_reduced, mats_reduced.shape, num_chars)
    
    for i, v in enumerate(mats_reduced):
        plt.annotate(args[i // num_chars][2][i % num_chars], xy=(v[0], v[1]))
    
    plt.show()