import os
import sys
import requests
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime

WEBHOOK = os.environ.get("DISCORD_WEBHOOK_URL", "")

UNIVERSE = [
    ("7203.T", "トヨタ"), ("7267.T", "ホンダ"), ("7201.T", "日産"),
    ("7269.T", "スズキ"), ("7270.T", "SUBARU"), ("7211.T", "三菱自"),
    ("6902.T", "デンソー"), ("7272.T", "ヤマハ発"),
    ("6758.T", "ソニーG"), ("6501.T", "日立"), ("6752.T", "パナ"),
    ("6753.T", "シャープ"), ("6701.T", "NEC"), ("6702.T", "富士通"),
    ("6981.T", "村田製作所"), ("6954.T", "ファナック"), ("6861.T", "キーエンス"),
    ("6367.T", "ダイキン"), ("6857.T", "アドバンテスト"),
    ("6920.T", "レーザーテック"), ("7741.T", "HOYA"),
    ("7751.T", "キヤノン"), ("7731.T", "ニコン"), ("7974.T", "任天堂"),
    ("8035.T", "東京エレクトロン"), ("6098.T", "リクルート"), ("6988.T", "日東電工"),
    ("4063.T", "信越化学"), ("4502.T", "武田薬品"), ("4503.T", "アステラス"),
    ("4568.T", "第一三共"), ("4519.T", "中外製薬"), ("4523.T", "エーザイ"),
    ("4901.T", "富士フイルム"), ("4452.T", "花王"), ("4911.T", "資生堂"),
    ("3402.T", "東レ"), ("4005.T", "住友化学"), ("4188.T", "三菱ケミ"),
    ("8306.T", "三菱UFJ"), ("8316.T", "三井住友FG"), ("8411.T", "みずほ"),
    ("8591.T", "オリックス"), ("8604.T", "野村HD"), ("8766.T", "東京海上"),
    ("8725.T", "MS&AD"), ("8750.T", "第一生命"), ("8630.T", "SOMPO"),
    ("8001.T", "伊藤忠"), ("8002.T", "丸紅"), ("8031.T", "三井物産"),
    ("8053.T", "住友商事"), ("8058.T", "三菱商事"), ("8015.T", "豊田通商"),
    ("9432.T", "NTT"), ("9433.T", "KDDI"), ("9434.T", "SBモバイル"),
    ("9984.T", "ソフトバンクG"), ("4755.T", "楽天"),
    ("9501.T", "東電"), ("9503.T", "関西電力"), ("9531.T", "東京ガス"),
    ("5020.T", "ENEOS"), ("1605.T", "INPEX"),
    ("9020.T", "JR東"), ("9022.T", "JR東海"), ("9021.T", "JR西"),
    ("9064.T", "ヤマト"), ("9301.T", "三菱倉庫"),
    ("5108.T", "ブリヂストン"), ("5401.T", "日本製鉄"), ("5411.T", "JFE"),
    ("5713.T", "住友金属鉱山"), ("5802.T", "住友電工"), ("5201.T", "AGC"),
    ("2914.T", "JT"), ("2502.T", "アサヒ"), ("2503.T", "キリン"),
    ("2801.T", "キッコーマン"), ("2802.T", "味の素"), ("2269.T", "明治"),
    ("9983.T", "ファーリテ"), ("3382.T", "セブン&アイ"), ("8267.T", "イオン"),
    ("9843.T", "ニトリ"), ("7453.T", "良品計画"), ("4661.T", "OLC"),
    ("6301.T", "コマツ"), ("6326.T", "クボタ"), ("7011.T", "三菱重工"),
    ("7013.T", "IHI"), ("7012.T", "川崎重工"),
    ("5991.T", "ニッパツ"), ("7259.T", "アイシン"), ("7282.T", "豊田合成"),
    ("6473.T", "ジェイテクト"), ("7278.T", "エクセディ"), ("6479.T", "ミネベアミツミ"),
    ("6963.T", "ローム"), ("6806.T", "ヒロセ電機"), ("6976.T", "太陽誘電"),
    ("6770.T", "アルプスアルパイン"), ("6594.T", "ニデック"), ("6723.T", "ルネサス"),
    ("6762.T", "TDK"), ("6728.T", "アルバック"),
    ("6268.T", "ナブテスコ"), ("6103.T", "オークマ"), ("6383.T", "ダイフク"),
    ("6674.T", "GSユアサ"), ("7276.T", "小糸製作所"), ("6856.T", "堀場製作所"),
    ("6471.T", "日本精工"), ("6305.T", "日立建機"),
    ("4042.T", "東ソー"), ("4182.T", "三菱ガス化学"), ("4204.T", "積水化学"),
    ("4205.T", "日本ゼオン"), ("4912.T", "ライオン"), ("4530.T", "久光製薬"),
    ("4902.T", "コニカミノルタ"),
    ("3659.T", "ネクソン"), ("3774.T", "IIJ"), ("4704.T", "トレンドマイクロ"),
    ("2432.T", "DeNA"), ("4689.T", "LINEヤフー"), ("9684.T", "スクエニ"),
    ("9697.T", "カプコン"), ("9766.T", "コナミG"),
    ("8473.T", "SBI"), ("8424.T", "芙蓉総合リース"), ("8308.T", "りそな"),
    ("8593.T", "三菱HC"),
    ("4507.T", "塩野義"), ("4528.T", "小野薬品"), ("4536.T", "参天製薬"),
    ("4540.T", "ツムラ"), ("2282.T", "日本ハム"), ("2871.T", "ニチレイ"),
    ("2875.T", "東洋水産"), ("2897.T", "日清食品"), ("2809.T", "キユーピー"),
    ("3086.T", "Jフロント"), ("8233.T", "高島屋"), ("3099.T", "三越伊勢丹"),
    ("2670.T", "ABCマート"), ("7532.T", "パンパシHD"), ("8252.T", "丸井"),
    ("4666.T", "パーク24"),
    ("1801.T", "大成建設"), ("1803.T", "清水建設"), ("1808.T", "長谷工"),
    ("1812.T", "鹿島"), ("8802.T", "三菱地所"), ("8801.T", "三井不動産"),
    ("8830.T", "住友不動産"),
    ("9001.T", "東武"), ("9005.T", "東急"), ("9007.T", "小田急"),
    ("9101.T", "日本郵船"), ("9104.T", "商船三井"), ("9107.T", "川崎汽船"),
    ("9502.T", "中部電力"), ("9508.T", "九州電力"), ("9532.T", "大阪ガス"),
    ("7912.T", "大日本印刷"), ("7911.T", "凸版印刷"), ("3769.T", "GMOペイメント"),
    ("2587.T", "サントリーBF"),
]


def compute_indicators(df):
    df = df.copy()
    c, h, l, v = df["Close"], df["High"], df["Low"], df["Volume"]
    df["SMA5"] = c.rolling(5).mean()
    df["SMA25"] = c.rolling(25).mean()
    df["SMA75"] = c.rolling(75).mean()
    df["SMA200"] = c.rolling(200).mean()
    df["EMA13"] = c.ewm(span=13, adjust=False).mean()
    delta = c.diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, np.nan)
    df["RSI"] = 100 - 100 / (1 + rs)
    low14 = l.rolling(14).min()
    high14 = h.rolling(14).max()
    fast_k = (c - low14) / (high14 - low14) * 100
    df["Stoch_K"] = fast_k.rolling(3).mean()
    df["Stoch_D"] = df["Stoch_K"].rolling(3).mean()
    ema12 = c.ewm(span=12, adjust=False).mean()
    ema26 = c.ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["MACD_Sig"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_Hist"] = df["MACD"] - df["MACD_Sig"]
    tr = pd.concat([h - l, (h - c.shift(1)).abs(), (l - c.shift(1)).abs()],
                   axis=1).max(axis=1)
    up_move = h - h.shift(1)
    down_move = l.shift(1) - l
    plus_dm = up_move.where((up_move > down_move) & (up_move > 0), 0.0)
    minus_dm = down_move.where((down_move > up_move) & (down_move > 0), 0.0)
    atr = tr.ewm(alpha=1/14, adjust=False).mean()
    plus_di = 100 * plus_dm.ewm(alpha=1/14, adjust=False).mean() / atr
    minus_di = 100 * minus_dm.ewm(alpha=1/14, adjust=False).mean() / atr
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)
    df["+DI"] = plus_di
    df["-DI"] = minus_di
    df["ADX"] = dx.ewm(alpha=1/14, adjust=False).mean()
    ma20 = c.rolling(20).mean()
    std20 = c.rolling(20).std()
    df["BB_Up"] = ma20 + 2 * std20
    df["BB_Lo"] = ma20 - 2 * std20
    df["Vol_MA20"] = v.rolling(20).mean()
    return df


def score_one(df):
    score = 0
    triggers = []
    c = df["Close"].iloc[-1]
    c1 = df["Close"].iloc[-2]
    o = df["Open"].iloc[-1]
    o1 = df["Open"].iloc[-2]
    h = df["High"].iloc[-1]
    l = df["Low"].iloc[-1]
    v = df["Volume"].iloc[-1]
    sma5, sma25 = df["SMA5"], df["SMA25"]
    sma75, sma200 = df["SMA75"], df["SMA200"]
    ema13 = df["EMA13"]
    rsi, k, d_ = df["RSI"], df["Stoch_K"], df["Stoch_D"]
    hist, macd, sig = df["MACD_Hist"], df["MACD"], df["MACD_Sig"]
    plus_di, minus_di, adx = df["+DI"], df["-DI"], df["ADX"]
    bb_up, bb_lo = df["BB_Up"], df["BB_Lo"]
    vol20 = df["Vol_MA20"].iloc[-1]

    # 1-5 トレンド
    if sma25.iloc[-1] > sma25.iloc[-3] and sma25.iloc[-5] <= sma25.iloc[-7]:
        score += 1; triggers.append("MA25上向き転換")
    if c > sma25.iloc[-1] and c1 <= sma25.iloc[-2]:
        score += 1; triggers.append("MA25上抜け")
    if c > sma5.iloc[-1] > sma25.iloc[-1]:
        score += 1; triggers.append("MA正配列")
    if sma5.iloc[-1] > sma25.iloc[-1] and sma5.iloc[-2] <= sma25.iloc[-2]:
        score += 1; triggers.append("GC5×25")
    min_div = (df["Close"] / df["SMA200"] - 1).iloc[-20:].min()
    if min_div < -0.10 and c > c1:
        score += 1; triggers.append("200MA回帰")

    # 6-10 オシレータ
    for lb in range(1, 4):
        if pd.notna(rsi.iloc[-lb]) and pd.notna(rsi.iloc[-lb-1]):
            if rsi.iloc[-lb] > 30 and rsi.iloc[-lb-1] <= 30:
                score += 1; triggers.append("RSI30上抜け"); break
    if (k.iloc[-1] > d_.iloc[-1] and k.iloc[-2] <= d_.iloc[-2] and k.iloc[-1] < 30):
        score += 1; triggers.append("ストキャスGC")
    if hist.iloc[-1] > 0 and hist.iloc[-2] <= 0:
        score += 1; triggers.append("MACDヒスト陽転")
    if (macd.iloc[-1] > sig.iloc[-1] and macd.iloc[-2] <= sig.iloc[-2] and macd.iloc[-1] < 0):
        score += 1; triggers.append("MACD-GC")
    close_low_idx = df["Close"].iloc[-20:].idxmin()
    if close_low_idx in rsi.index:
        low_rsi = rsi.loc[close_low_idx]
        if c <= df["Close"].iloc[-20:].quantile(0.2) and rsi.iloc[-1] > low_rsi + 5:
            score += 1; triggers.append("RSIダイバ")

    # 11-15 方向強度
    if pd.notna(plus_di.iloc[-1]) and pd.notna(minus_di.iloc[-1]) and plus_di.iloc[-1] > minus_di.iloc[-1]:
        score += 1; triggers.append("+DI>-DI")
    if (adx.iloc[-5:].min() < 20 and adx.iloc[-1] > adx.iloc[-2] and adx.iloc[-1] > 15):
        score += 1; triggers.append("ADX低位上昇")
    touched_bb = (df["Low"].iloc[-3:] <= bb_lo.iloc[-3:] * 1.01).any()
    if touched_bb and c > c1:
        score += 1; triggers.append("ボリバン下限反発")
    bb_width = (bb_up - bb_lo) / df["Close"]
    if (bb_width.iloc[-1] > bb_width.iloc[-5] * 1.1
        and bb_width.iloc[-10:-5].mean() < bb_width.iloc[-30:].mean() * 0.7):
        score += 1; triggers.append("BBスクイーズ")
    if (df["Low"].iloc[-1] > df["Low"].iloc[-2] > df["Low"].iloc[-3]
        and df["Low"].iloc[-3] < df["Low"].iloc[-4]):
        score += 1; triggers.append("安値切り上げ")

    # 16-20 出来高ローソク
    if pd.notna(vol20) and v > vol20 * 2 and c > o:
        score += 1; triggers.append("出来高急増")
    body = abs(c - o)
    lower_wick = min(c, o) - l
    upper_wick = h - max(c, o)
    if body > 0 and lower_wick > body * 2 and upper_wick < body * 0.5:
        score += 1; triggers.append("ハンマー")
    if c1 < o1 and c < o:
        prev_body = o1 - c1
        today_body = o - c
        if (prev_body > 0 and today_body > 0 and today_body < prev_body
            and h <= o1 and l >= c1):
            score += 1; triggers.append("陰の陰はらみ")
    if c > o:
        prev3 = all(df["Close"].iloc[-kk] < df["Open"].iloc[-kk] for kk in range(2, 5))
        if prev3:
            score += 1; triggers.append("3日陰線後の陽線")
    low20 = df["Low"].iloc[-20:].min()
    if df["Low"].iloc[-3:].min() <= low20 * 1.02 and c > c1:
        score += 1; triggers.append("20日安値反発")

    # 21-30 線の方向
    if sma5.iloc[-1] > sma5.iloc[-3]:
        score += 1; triggers.append("SMA5上向き")
    if sma25.iloc[-1] > sma25.iloc[-3]:
        score += 1; triggers.append("SMA25上向き")
    if sma75.iloc[-1] > sma75.iloc[-3]:
        score += 1; triggers.append("SMA75上向き")
    if sma200.iloc[-1] > sma200.iloc[-5]:
        score += 1; triggers.append("SMA200上向き")
    if sma5.iloc[-1] > sma5.iloc[-3] and sma25.iloc[-1] > sma25.iloc[-3]:
        score += 1; triggers.append("SMA5&25上向き")
    if (sma5.iloc[-1] > sma5.iloc[-3] and sma25.iloc[-1] > sma25.iloc[-3]
        and sma75.iloc[-1] > sma75.iloc[-3]):
        score += 1; triggers.append("SMA5&25&75上向き")
    if (c > sma5.iloc[-1] > sma25.iloc[-1] > sma75.iloc[-1] > sma200.iloc[-1]
        and sma5.iloc[-1] > sma5.iloc[-3] and sma25.iloc[-1] > sma25.iloc[-3]
        and sma75.iloc[-1] > sma75.iloc[-3] and sma200.iloc[-1] > sma200.iloc[-5]):
        score += 1; triggers.append("PPP完成")
    if (sma5.iloc[-1] > sma5.iloc[-3] and sma5.iloc[-5] <= sma5.iloc[-7]):
        score += 1; triggers.append("SMA5上向き転換")
    if adx.iloc[-1] > adx.iloc[-3]:
        score += 1; triggers.append("ADX上向き")
    if plus_di.iloc[-1] > plus_di.iloc[-3]:
        score += 1; triggers.append("+DI上向き")

    # 31-40 相場師朗系
    ema13_up = ema13.iloc[-1] > ema13.iloc[-2]
    ema13_up_prev = ema13.iloc[-2] > ema13.iloc[-3]
    hist_up = hist.iloc[-1] > hist.iloc[-2]
    hist_up_prev = hist.iloc[-2] > hist.iloc[-3]
    today_red = (not ema13_up) and (not hist_up)
    prev_red = (not ema13_up_prev) and (not hist_up_prev)
    today_green = ema13_up and hist_up
    prev_green = ema13_up_prev and hist_up_prev
    if prev_red and not today_red:
        score += 1; triggers.append("インパルス赤消滅")
    if today_green and not prev_green and not prev_red:
        score += 1; triggers.append("インパルス青→緑")
    body_mid = (o + c) / 2
    if (sma5.iloc[-1] >= sma5.iloc[-2] * 0.995
        and body_mid > sma5.iloc[-1] and c > o):
        score += 1; triggers.append("下半身")
    for lb in range(2, 7):
        dist = abs(sma5.iloc[-lb] - sma25.iloc[-lb]) / sma25.iloc[-lb]
        if dist < 0.01:
            today_dist = (sma5.iloc[-1] - sma25.iloc[-1]) / sma25.iloc[-1]
            if today_dist > 0.015:
                score += 1; triggers.append("ものわかれ上")
            break
    recent9_low_idx = df["Low"].iloc[-9:].idxmin()
    days_since_low = len(df) - 1 - df.index.get_loc(recent9_low_idx)
    if 1 <= days_since_low <= 9 and c > df["Low"].iloc[-9:].min() * 1.02:
        score += 1; triggers.append("9の法則反発")
    high20 = df["High"].iloc[-21:-1].max()
    range_ratio = (df["High"].iloc[-21:-1].max() - df["Low"].iloc[-21:-1].min()) / df["Close"].iloc[-21:-1].mean()
    if range_ratio < 0.08 and c > high20:
        score += 1; triggers.append("横ばいブレイク")
    round_numbers = [100, 500, 1000, 2000, 3000, 5000, 10000, 20000, 30000, 50000]
    for rn in round_numbers:
        if c1 < rn <= c:
            score += 1; triggers.append(f"節目{rn}円突破")
            break
    recent_high = df["High"].iloc[-60:-5].max()
    if recent_high * 0.92 <= c <= recent_high * 0.98 and c > c1:
        score += 1; triggers.append("前回高値手前押し目")
    lows_recent = df["Low"].iloc[-20:]
    low_idx1 = lows_recent.iloc[:10].idxmin()
    low_idx2 = lows_recent.iloc[10:].idxmin()
    if low_idx1 in df.index and low_idx2 in df.index:
        low1 = df["Low"].loc[low_idx1]
        low2 = df["Low"].loc[low_idx2]
        if low2 > low1:
            score += 1; triggers.append("上昇TL反発")
    lows30 = df["Low"].iloc[-30:]
    sorted_lows = lows30.nsmallest(5)
    if len(sorted_lows) >= 2:
        low_diff = (sorted_lows.max() - sorted_lows.min()) / sorted_lows.min()
        if low_diff < 0.03 and c > lows30.min() * 1.05:
            score += 1; triggers.append("ダブルボトム簡易")

    return score, triggers


def send_discord(message):
    if not WEBHOOK:
        print("Webhook未設定のためコンソール出力のみ")
        print(message)
        return
    for i in range(0, len(message), 1900):
        chunk = message[i:i+1900]
        try:
            r = requests.post(WEBHOOK, json={"content": chunk}, timeout=15)
            r.raise_for_status()
        except Exception as e:
            print(f"Discord送信失敗: {e}")


def main():
    print(f"開始: {datetime.now()}")
    results = []
    for idx, (tkr, name) in enumerate(UNIVERSE, 1):
        if idx % 20 == 0:
            print(f"  {idx}/{len(UNIVERSE)}")
        try:
            df = yf.download(tkr, period="300d", interval="1d",
                             progress=False, auto_adjust=True)
            if df is None or len(df) < 300:
                continue
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            df = compute_indicators(df)
            score, triggers = score_one(df)
            results.append({
                "ticker": tkr, "name": name,
                "close": float(df["Close"].iloc[-1]),
                "score": score, "triggers": triggers,
            })
        except Exception as e:
            print(f"  {tkr} skip: {e}")
            continue

    results.sort(key=lambda x: -x["score"])
    today = datetime.now().strftime("%Y-%m-%d")

    lines = [f"📊 **買いシグナル通知 {today}**", "", "**【Top10】スコア上位**"]
    for i, r in enumerate(results[:10], 1):
        medal = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else f"{i}."
        lines.append(f"{medal} 【{r['score']}/40】 {r['ticker']} {r['name']} {r['close']:,.0f}円")
    lines.append("")
    lines.append("**【Top3の詳細】**")
    for r in results[:3]:
        lines.append(f"・{r['ticker']} {r['name']}")
        lines.append(f"  → {', '.join(r['triggers'][:8])}")

    message = "\n".join(lines)
    print(message)
    send_discord(message)
    print("完了")


if __name__ == "__main__":
    main()
