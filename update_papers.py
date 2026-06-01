import requests, json, datetime, time 

# 全疾患・解析ロジック統合 
DISEASES = { 
  　"stroke": "Stroke Rehabilitation", 
  　"knee": "Knee Osteoarthritis", 
  　"back": "Low Back Pain", 
  　"cardio": "Cardiac Rehabilitation", 
  　"frailty": "Sarcopenia", 
  　"shoulder": "Frozen Shoulder" 
} 
def　generate_hint(title): 
　　 t = title.lower() 
     # キーワード判別による専門的アドバイス 
     if "stroke" in t: 
         if"upper" in t: 
         return "【脳卒中・上肢】課題指向型訓練とCI療法の併用が推奨されます。" return "【脳卒中】早期離床と高頻度の反復訓練がエビデンスの核です。" 
     if "knee" in t or "osteoarthritis" in t: 
         return "【膝OA】筋力強化は疼痛改善に高いエビデンス。継続期間が重要です。" 
     if "frailty" in t: 
         return "【高齢者】タンパク質摂取とレジスタンストレーニングの併用を推奨。" 
     if "shoulder" in t: 
         return "【肩関節】急性期の炎症管理と、慢性期の肩甲帯機能改善を優先。" 
     return "【臨床ヒント】タイトルから関連ガイドラインを確認し、個別適応を検討してください。" 

def fetch_all(): 
    all_data = {"last_update": datetime.datetime.now().strftime("%Y-%m-%d"), "diseases": {}} 
    for key, query inDISEASES.items(): 
        # PubMed検索 
        url = f"https://nih.gov{query}+AND+meta-analysis&reldate=1&retmode=json" 
        try: 
            res = requests.get(url).json() 
            ids = res.get('esearchresult', {}).get('idlist', []) 
            papers = [] 
            for pid in ids[:3]: # 最新3件
                title_url = f"https://nih.gov{pid}&retmode=json" 
                title = requests.get(title_url).json()['result'][pid]['title'] 
                papers.append({"title": title, "url": f"https://nih.gov{pid}/", "hint": generate_hint(title)}) 
            all_data["diseases"][key] = papers 
        except: continue
        time.sleep(1) # サーバー負荷対策 

    with open('papers.json', 'w', encoding='utf-8') as f: 
        json.dump(all_data, f, ensure_ascii=False, indent=4) 
if __name__ == "__main__": 
    fetch_all()
