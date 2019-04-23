import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ファイルの読み取り
df=pd.read_csv('3group.csv')

# グラフの基本フォント 　
plt.rcParams['font.family']='Times New Roman'
plt.rcParams['font.size']=17
plt.rcParams["mathtext.fontset"] = 'cm'


# 以下，入力項目--------------------------------------------

plt.figure(figsize=(6, 5)) #ウインドウサイズ

label_list = ['A','B','C'] # 凡例に記載されるグループ名
color_list = ['white','k','lightgray'] # 各グループのカラー
label_x = "X label"    # x label name
label_y = "Y label"    # y label name
label_fontsize = 17

# 凡例の位置　（anchor: upperleft）
legend_x = 0.05
legend_y = 0.99
legend_fontsize = 15

bar_width=0.24 # 棒グラフの幅
ymin = 0       # y軸の最小値
ymax = 30      # y軸の最大値 

p_height= 1.2 # p value の位置調整用（y方向）
p_fontsize = 12

# サンプル数などのテキストボックス（anchor: upperleft，座標はグラフ内の値．xは'count'に基づく．）
textbox = " n=3\n Mean${\\pm}$S.D.\n   *p<0.05\n **p<0.01"
textbox_x = 0.9
textbox_y = 22
textbox_fontsize = 15

# -------------------------------------------------------


# 空の行列を用意
l = np.arange(3)
y_arr = np.zeros(3*max(df['count'])).reshape((max(df['count']),3))
ye_arr = np.zeros(3*max(df['count'])).reshape((max(df['count']),3))

# データの行列化
for i in l:
    y_arr[:,i] = df['group'+str(i)]
    ye_arr[:,i] = df['group'+str(i)+'e']


# 後の'*'表示用
p12= df['p12']
p23= df['p23']
p13= df['p13']

# 棒グラフの描画
for i in l:
    plt.bar(df['count']+(i-1/2)*bar_width, y_arr[:,i], color = color_list[i], label = label_list[i], 
        width = bar_width, linewidth = 1.5, edgecolor ='k', yerr = ye_arr[:,i], ecolor ='k', capsize = 4.0)


# p value の表示
def label_diff1(i, text, X, Y):
    x = X[i]
    dx = bar_width*0.8
    props = {'connectionstyle': 'bar', 'arrowstyle': '-',
             'shrinkA': 0, 'shrinkB': 0, 'linewidth': 1}
    plt.annotate(text, xy=(x, Y + ymax/100), fontsize=p_fontsize)
    plt.annotate('', xy=(x, Y), xytext=(x+dx, Y), arrowprops=props)
def label_diff2(i, text, X, Y):
    x = X[i]
    dx = bar_width*2
    props = {'connectionstyle': 'bar', 'arrowstyle': '-',
             'shrinkA': 3, 'shrinkB': 3, 'linewidth': 1}
    plt.annotate(text, xy=(x, Y + ymax/40), fontsize=p_fontsize)
    plt.annotate('', xy=(x, Y), xytext=(x+dx, Y), arrowprops=props)

for k in range(0,max(df['count'])): 
    Ya = max(y_arr[k,:]) + (ye_arr[k, 0]+ye_arr[k, 1]+ye_arr[k, 2])/3 + p_height
    Yb = Ya + p_height
    over = 0
    if p12[k] >= 1:
        if p12[k] == 1:
            pv = ' *'
        elif p12[k] == 2:
            pv = '**' 
        label_diff1(k, pv, df['count']-bar_width/2, Ya)
        over = 1
    if p23[k] >= 1:
        if p23[k] == 1:
            pv = ' *'
        elif p23[k] == 2:
            pv = '**' 
        label_diff1(k, pv, df['count']+bar_width*(1/2+0.2), Ya)
        over = 1
    if p13[k] >= 1:
        if p13[k] == 1:
            pv = '   *'
        elif p13[k] == 2:
            pv = '  **'
        if over == 1:
            label_diff2(k, pv, df['count']-bar_width/2, Yb)
        else:
            label_diff2(k, pv, df['count']-bar_width/2, Ya)


# 横軸の値変換 （CSVファイルのxの値に変換し直す．）
plt.locator_params(axis='x',nbins=0)
plt.xticks(df['count']+bar_width/2, df['x'])


# 軸の体裁
plt.xlim(0.5,max(df['count'])+0.8)
plt.ylim(ymin, ymax)
plt.xlabel(label_x, fontsize = label_fontsize)
plt.ylabel(label_y, fontsize = label_fontsize)

# 凡例
leg=plt.legend(bbox_to_anchor=(legend_x, legend_y), loc='upper left', borderaxespad=0,fontsize=legend_fontsize)
leg.get_frame().set_alpha(1)
leg.get_frame().set_edgecolor('white')

# n値などの記載
plt.text(textbox_x, textbox_y, textbox, BackgroundColor='white', ha='left',va ='top',fontsize=textbox_fontsize)

# (x10^5)の記載
# plt.text(5,ymax,"${(\\times10^5)}$",ha='left',va ='bottom', fontsize=text_fontsize)

# 主目盛りをグラフの内側に表示
plt.tick_params(which='both',direction='in')

# x軸の目盛を消す
plt.tick_params(bottom=False)

# ウインドウサイズにグラフをフィット
plt.tight_layout()

plt.show() 