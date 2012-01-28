import re

def _is_cjk(char):
    return any(r[0] <= ord(char) <= r[1] for r in CJK_CODEPOINT_RANGES)

def is_cjk(s):
    return any(_is_cjk(char) for char in s)

def is_pinyin(s):
    # replace tone mark numbers in the query with the empty string.
    return all(re.sub(r'\d', '', word) in PINYIN_SYLLABLES for word in s.split())

CJK_CODEPOINT_RANGES = [
    (0x2e80, 0x9fcf),   # chinese chars (kanji), kana, hangul compatibility jamo, a bunch more.
    (0xac00, 0xd7af),   # hangul syllables
    (0x1100, 0x11ff),   # hangul jamo
    (0xf900, 0xfaff),   # CJK compatability ideographs
    (0xff00, 0xffff),   # halfwidth/fullwidth forms + specials.
    (0x20000, 0x2ffff), # supplementary ideographic plane. why not.
    ]

# screen scraping w/ jquery trick: you can get this list from wikipedia.
# go to: http://en.wikipedia.org/wiki/Pinyin_table
# and from the console run these lines of jquery:
# results = []
# $('.wikitable td').each(function () {results.push($(this).text())});
# results.join('\n') // print it out
PINYIN_SYLLABLES_RAW = '''
zhi
chi
shi

ri
zi
ci
si

a

ba
pa
ma
fa
da
ta
na
la
ga
ka
ha

zha
cha
sha

za
ca
sa
o
bo
po
mo
fo

lo

e

me

de
te
ne
le
ge
ke
he

zhe
che
she
re
ze
ce
se
ye

ai
bai
pai
mai

dai
tai
nai
lai
gai
kai
hai

zhai
chai
shai

zai
cai
sai
ei
bei
pei
mei
fei
dei
tei
nei
lei
gei

hei

zhei

shei

zei

ao
bao
pao
mao

dao
tao
nao
lao
gao
kao
hao

zhao
chao
shao
rao
zao
cao
sao
ou

pou
mou
fou
dou
tou
nou
lou
gou
kou
hou

zhou
chou
shou
rou
zou
cou
sou
an
ban
pan
man
fan
dan
tan
nan
lan
gan
kan
han

zhan
chan
shan
ran
zan
can
san
en
ben
pen
men
fen
den

nen

gen
ken
hen

zhen
chen
shen
ren
zen
cen
sen
ang
bang
pang
mang
fang
dang
tang
nang
lang
gang
kang
hang

zhang
chang
shang
rang
zang
cang
sang
eng
beng
peng
meng
feng
deng
teng
neng
leng
geng
keng
heng

zheng
cheng
sheng
reng
zeng
ceng
seng
er

yi
bi
pi
mi

di
ti
ni
li

ji
qi
xi

ya

dia

lia

jia
qia
xia

yo

ye
bie
pie
mie

die
tie
nie
lie

jie
qie
xie

yai

yao
biao
piao
miao

diao
tiao
niao
liao

jiao
qiao
xiao

you

miu

diu

niu
liu

jiu
qiu
xiu

yan
bian
pian
mian

dian
tian
nian
lian

jian
qian
xian

yin
bin
pin
min

nin
lin

jin
qin
xin

yang

niang
liang

jiang
qiang
xiang

ying
bing
ping
ming

ding
ting
ning
ling

jing
qing
xing

wu
bu
pu
mu
fu
du
tu
nu
lu
gu
ku
hu

zhu
chu
shu
ru
zu
cu
su
wa

gua
kua
hua

zhua
chua
shua
rua

wo

duo
tuo
nuo
luo
guo
kuo
huo

zhuo
chuo
shuo
ruo
zuo
cuo
suo
wai

guai
kuai
huai

zhuai
chuai
shuai

wei

dui
tui

gui
kui
hui

zhui
chui
shui
rui
zui
cui
sui
wan

duan
tuan
nuan
luan
guan
kuan
huan

zhuan
chuan
shuan
ruan
zuan
cuan
suan
wen

dun
tun

lun
gun
kun
hun

zhun
chun
shun
run
zun
cun
sun
wang

guang
kuang
huang

zhuang
chuang
shuang

weng

dong
tong
nong
long
gong
kong
hong

zhong
chong

rong
zong
cong
song
yu

nu:
lu:

ju
qu
xu

yue

nu:e
lu:e

jue
que
xue

yuan

juan
quan
xuan

yun

jun
qun
xun

yong

jiong
qiong
xiong
'''

# for fast lookup,
# put each of these into a (hash-based) python set instead of a big string.
PINYIN_SYLLABLES = set(line.strip() for line in PINYIN_SYLLABLES_RAW.split() if line.strip())
