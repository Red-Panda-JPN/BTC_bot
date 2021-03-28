#!/usr/bin/env python3

##
## 参考　
## https://qiita.com/shionhonda/items/bd2a7aaf143eff4972c4
## このサイトでは1分ごとにだったが、10秒ごとに変更する。
## さらにSFD対策用に現物-FXを同時にプロットする。
## SFDが発生した場合はFXのグラフを赤色に変更。
##

# ライブラリの呼び出し
import requests
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import time
from datetime import datetime
# リアルタイムプロットに必要
from ipywidgets import FloatProgress
from IPython.display import display, clear_output
# Jupyter環境でグラフを表示するのに必要
%matplotlib inline

# bitflyerのURL
bitflyer_URL = "https://api.bitflyer.jp/v1/getticker"
param = {'product_code' : "BTC_JPY"}
paramFX = {'product_code' : "FX_BTC_JPY"}
# 最終取引価格を格納する配列。現物用とFX用の二つを定義する。
raws = []
rawsFX = []
# プロットの準備
fig = plt.figure(figsize=(16,10))
axe = fig.add_subplot(111)

while True:
    # 10秒ごとに稼働
    if int(datetime.now().strftime('%S') [0:2])%10==0:
        clear_output(True)# プロット用データの更新
        #　現物のデータを取る。
        bids= requests.get(bitflyer_URL,param)
        data = bids.json()
        raws = np.append(raws, data.get('ltp'))
        #　FXのデータを取る。
        bidsFX= requests.get(bitflyer_URL, paramFX)
        dataFX = bidsFX.json()
        rawsFX = np.append(rawsFX, dataFX.get('ltp'))
        
        # 作図
        axe.get_yaxis().get_major_formatter().set_scientific(False)
        if  (abs((data.get('ltp')-dataFX.get('ltp')))/data.get('ltp'))*100  >=5:
            axe.plot(rawsFX,"red",linewidth=2,label="BTC/JPY price in bitflyer")
            axe.plot(raws,"grey",linewidth=2, linestyle="dashed")
            axe.set_title("BTC/JPY price in bitflyer FX")
            display(fig)
        else:   
            axe.plot(rawsFX,"black",linewidth=2,label="BTC/JPY price in bitflyer")
            axe.plot(raws,"grey",linewidth=2, linestyle="dashed")
            axe.set_title("BTC/JPY price in bitflyer FX")
            display(fig)
        # 5秒休憩
        time.sleep(5)
        axe.cla()
