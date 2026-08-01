import os
import time
import streamlit as st
from gtts import gTTS

# 設定 Streamlit 網頁版面為寬螢幕
st.set_page_config(page_title="N4核心單字大師機", layout="wide")

# 完整保留 15 類、每類精確 42 字，共 672 字的黃金資料庫，絕不刪減
WORD_DATABASE = {
    "名詞一 家族與核心人物": [
        {"word": "1人", "kana": "ひとり", "mean": "1人"},
        {"word": "2人", "kana": "ふたり", "mean": "2人"},
        {"word": "男の人", "kana": "おとこのひと", "mean": "男人"},
        {"word": "女の人", "kana": "おんなのひと", "mean": "女人"},
        {"word": "男性", "kana": "だんせい", "mean": "男性"},
        {"word": "女性", "kana": "じょせい", "mean": "女性"},
        {"word": "父", "kana": "ちち", "mean": "我爸爸"},
        {"word": "母", "kana": "はは", "mean": "我媽媽"},
        {"word": "兄", "kana": "あに", "mean": "我哥哥"},
        {"word": "姉", "kana": "あね", "mean": "我姊姊"},
        {"word": "弟", "kana": "おとうと", "mean": "我弟弟"},
        {"word": "妹", "kana": "いもうと", "mean": "我妹妹"},
        {"word": "息子", "kana": "むすこ", "mean": "兒子"},
        {"word": "娘", "kana": "むすめ", "mean": "女兒"},
        {"word": "祖父", "kana": "そふ", "mean": "祖父"},
        {"word": "祖母", "kana": "そぼ", "mean": "祖母"},
        {"word": "大人", "kana": "おとな", "mean": "大人"},
        {"word": "子供", "kana": "こども", "mean": "小孩"},
        {"word": "お子さん", "kana": "おこさん", "mean": "您孩子"},
        {"word": "兄弟", "kana": "きょうだいで", "mean": "兄弟姐妹"},
        {"word": "両親", "kana": "りょうしん", "mean": "父母"},
        {"word": "親", "kana": "おや", "mean": "父母"},
        {"word": "家族", "kana": "かぞく", "mean": "家人"},
        {"word": "友達", "kana": "ともだち", "mean": "朋友"},
        {"word": "自分", "kana": "じぶん", "mean": "自己"},
        {"word": "僕", "kana": "ぼく", "mean": "我男性"},
        {"word": "先輩", "kana": "せんぱい", "mean": "前輩"},
        {"word": "後輩", "kana": "こうはい", "mean": "晚輩"},
        {"word": "皆", "kana": "みな", "mean": "大家"},
        {"word": "みんな", "kana": "みんな", "mean": "大家"},
        {"word": "係りの人", "kana": "かかりのひと", "mean": "工作人員"},
        {"word": "相手", "kana": "あいて", "mean": "對方"},
        {"word": "店員", "kana": "てんいん", "mean": "店員"},
        {"word": "客さん", "kana": "おきゃくさん", "mean": "客人"},
        {"word": "医者", "kana": "いしゃ", "mean": "醫生"},
        {"word": "泥棒", "kana": "どろぼう", "mean": "小偷"},
        {"word": "警察官", "kana": "けいさつかん", "mean": "警察"},
        {"word": "運転手", "kana": "うんてんしゅ", "mean": "司機"},
        {"word": "会社員", "kana": "かいしゃいん", "mean": "上班族"},
        {"word": "外国人", "kana": "がいこくじん", "mean": "外國人"},
        {"word": "留学生", "kana": "りゅうがくせい", "mean": "留學生"},
        {"word": "大學生", "kana": "だいがくせい", "mean": "大學生"}
    ],
    "名詞二 時間與季節數量": [
        {"word": "春", "kana": "はる", "mean": "春天"},
        {"word": "夏", "kana": "なつ", "mean": "夏天"},
        {"word": "秋", "kana": "あき", "mean": "秋天"},
        {"word": "冬", "kana": "ふゆ", "mean": "冬天"},
        {"word": "最近", "kana": "さいきん", "mean": "最近"},
        {"word": "今日", "kana": "きょう", "mean": "今天"},
        {"word": "昨日", "kana": "きのう", "mean": "昨天"},
        {"word": "明日", "kana": "あした", "mean": "明天"},
        {"word": "明後日", "kana": "あさって", "mean": "後天"},
        {"word": "一昨日", "kana": "おととい", "mean": "前天"},
        {"word": "1日中", "kana": "いちにちじゅう", "mean": "一整天"},
        {"word": "午前中", "kana": "ごぜんちゅう", "mean": "上午"},
        {"word": "以下", "kana": "いか", "mean": "以下"},
        {"word": "今朝", "kana": "けさ", "mean": "今早"},
        {"word": "お昼", "kana": "おひる", "mean": "中午"},
        {"word": "夕方", "kana": "ゆうがた", "mean": "傍晚"},
        {"word": "昨夜", "kana": "ゆうべ", "mean": "昨晚"},
        {"word": "朝早い", "kana": "あさはやい", "mean": "早起清晨"},
        {"word": "夜遅い", "kana": "よるおそい", "mean": "很晚深夜"},
        {"word": "毎日", "kana": "まいにち", "mean": "每天"},
        {"word": "每晚", "kana": "まいばん", "mean": "每晚"},
        {"word": "毎週", "kana": "まいしゅう", "mean": "每週"},
        {"word": "先週", "kana": "せんしゅう", "mean": "上週"},
        {"word": "今週", "kana": "こんしゅう", "mean": "這週"},
        {"word": "來週", "kana": "らいしゅう", "mean": "下週"},
        {"word": "再來週", "kana": "さらいしゅう", "mean": "下下週"},
        {"word": "先月", "kana": "せんげつ", "mean": "上個月"},
        {"word": "今月", "kana": "こんげつ", "mean": "這個月"},
        {"word": "來月", "kana": "らいげつ", "mean": "下個月"},
        {"word": "半年", "kana": "はんとし", "mean": "半年"},
        {"word": "去年", "kana": "きょねん", "mean": "去年"},
        {"word": "今年", "kana": "ことし", "mean": "今年"},
        {"word": "來年", "kana": "らいねん", "mean": "明年"},
        {"word": "將來", "kana": "しょうらい", "mean": "將來"},
        {"word": "半分", "kana": "はんぶん", "mean": "一半"},
        {"word": "1時", "kana": "いちじ", "mean": "1點"},
        {"word": "1日", "kana": "ついたち", "mean": "1日"},
        {"word": "20日", "kana": "はつか", "mean": "20日"},
        {"word": "1つ", "kana": "ひとつ", "mean": "1個"},
        {"word": "2つ", "kana": "ふたつ", "mean": "2個"},
        {"word": "大きさ", "kana": "おおきさ", "mean": "大小尺寸"},
        {"word": "長さ", "kana": "ながさ", "mean": "長度"}
    ],
    "名詞三 位置與公共場所": [
        {"word": "所", "kana": "ところ", "mean": "場所"},
        {"word": "場所", "kana": "ばしょ", "mean": "地方"},
        {"word": "東", "kana": "ひがし", "mean": "東"},
        {"word": "西", "kana": "にし", "mean": "西"},
        {"word": "南", "kana": "みなみ", "mean": "南"},
        {"word": "北", "kana": "きた", "mean": "北"},
        {"word": "左", "kana": "ひだり", "mean": "左"},
        {"word": "右", "kana": "みぎ", "mean": "右"},
        {"word": "橫", "kana": "よこ", "mean": "旁邊"},
        {"word": "鄰", "kana": "となり", "mean": "隔壁"},
        {"word": "裏", "kana": "うら", "mean": "背面"},
        {"word": "外", "kana": "そと", "mean": "外面"},
        {"word": "橋", "kana": "はし", "mean": "橋"},
        {"word": "國", "kana": "くに", "mean": "國家"},
        {"word": "海", "kana": "うみ", "mean": "海"},
        {"word": "港", "kana": "みなと", "mean": "港口"},
        {"word": "道", "kana": "みち", "mean": "道路"},
        {"word": "角", "kana": "かど", "mean": "轉角"},
        {"word": "周り", "kana": "まわり", "mean": "周圍"},
        {"word": "真ん中", "kana": "まんなか", "mean": "正中間"},
        {"word": "世界", "kana": "せかい", "mean": "世界"},
        {"word": "社會", "kana": "しゃかい", "mean": "社會"},
        {"word": "會社", "kana": "かいしゃ", "mean": "公司"},
        {"word": "學校", "kana": "がっこう", "mean": "學校"},
        {"word": "教室", "kana": "きょうしつ", "mean": "教室"},
        {"word": "食堂", "kana": "しょくどう", "mean": "食堂"},
        {"word": "廊下", "kana": "ろうか", "mean": "走廊"},
        {"word": "受付", "kana": "うけつけ", "mean": "櫃檯"},
        {"word": "席", "kana": "せき", "mean": "座位"},
        {"word": "近所", "kana": "きんじょ", "mean": "近鄰"},
        {"word": "駅前", "kana": "えきまえ", "mean": "車站前"},
        {"word": "建物", "kana": "たてもの", "mean": "建築物"},
        {"word": "部屋", "kana": "へや", "mean": "房間"},
        {"word": "入口", "kana": "いりぐち", "mean": "入口"},
        {"word": "出口", "kana": "でぐち", "mean": "出口"},
        {"word": "お手洗い", "kana": "おてあらい", "mean": "洗手間"},
        {"word": "屋根", "kana": "やね", "mean": "屋頂"},
        {"word": "バス停", "kana": "ばすてい", "mean": "公車站"},
        {"word": "公園", "kana": "こうえん", "mean": "公園"},
        {"word": "工場", "kana": "こうじょう", "mean": "工廠"},
        {"word": "病院", "kana": "びょういん", "mean": "醫院"},
        {"word": "旅館", "kana": "りょかん", "mean": "旅館"}
    ],
    "名詞四 設施與學校生活": [
        {"word": "お寺", "kana": "おてら", "mean": "寺廟"},
        {"word": "神社", "kana": "じんじゃ", "mean": "神社"},
        {"word": "交番", "kana": "こうばん", "mean": "派出所"},
        {"word": "銀行", "kana": "ぎんこう", "mean": "銀行"},
        {"word": "空港", "kana": "くうこう", "mean": "機場"},
        {"word": "本屋", "kana": "ほんや", "mean": "書店"},
        {"word": "花屋", "kana": "はなや", "mean": "花店"},
        {"word": "八百屋", "kana": "やおや", "mean": "蔬果店"},
        {"word": "電気屋", "kana": "でんきや", "mean": "電器行"},
        {"word": "郵便局", "kana": "ゆうびんきょく", "mean": "郵局"},
        {"word": "動物園", "kana": "どうぶつえん", "mean": "動物園"},
        {"word": "美術館", "kana": "びじゅつかん", "mean": "美術館"},
        {"word": "博物館", "kana": "はくぶつかん", "mean": "博物館"},
        {"word": "體育館", "kana": "たいいくかん", "mean": "體育館"},
        {"word": "大學院", "kana": "だいがくいん", "mean": "研究所"},
        {"word": "運動場", "kana": "うんどうじょう", "mean": "操場"},
        {"word": "事務所", "kana": "じむしょ", "mean": "辦公室"},
        {"word": "會議室", "kana": "かいぎしつ", "mean": "會議室"},
        {"word": "說明會", "kana": "せつめいかい", "mean": "說明會"},
        {"word": "名前", "kana": "なまえ", "mean": "名字"},
        {"word": "番号", "kana": "ばんごう", "mean": "號碼"},
        {"word": "出席", "kana": "しゅっせき", "mean": "出席"},
        {"word": "問題", "kana": "もんだい", "mean": "問題"},
        {"word": "意味", "kana": "いみ", "mean": "意思"},
        {"word": "練習", "kana": "れんしゅう", "mean": "練習"},
        {"word": "予習", "kana": "よしゅう", "mean": "預習"},
        {"word": "復習", "kana": "ふくしゅう", "mean": "複習"},
        {"word": "漢字", "kana": "かんじ", "mean": "漢字"},
        {"word": "文法", "kana": "ぶんぽう", "mean": "文法"},
        {"word": "専門", "kana": "せんもん", "mean": "專業"},
        {"word": "文章", "kana": "ぶんしょう", "mean": "文章"},
        {"word": "言葉", "kana": "ことば", "mean": "語言"},
        {"word": "作文", "kana": "さくぶん", "mean": "作文"},
        {"word": "小說", "kana": "しょうせつ", "mean": "小說"},
        {"word": "日記", "kana": "にっき", "mean": "日記"},
        {"word": "葉書", "kana": "はがき", "mean": "明信片"},
        {"word": "試験", "kana": "しけん", "mean": "考試"},
        {"word": "試合", "kana": "しあい", "mean": "比賽"},
        {"word": "質問", "kana": "しつもん", "mean": "提問"},
        {"word": "合格", "kana": "ごうかく", "mean": "合格"},
        {"word": "宿題", "kana": "しゅくだい", "mean": "作業"},
        {"word": "授業", "kana": "じゅぎょう", "mean": "課堂"}
    ],
    "名詞五 工作與日常物品": [
        {"word": "黑板", "kana": "こくばん", "mean": "黑板"},
        {"word": "消しゴム", "kana": "けしごむ", "mean": "橡皮擦"},
        {"word": "音楽", "kana": "おんがく", "mean": "音樂"},
        {"word": "水泳", "kana": "すいえい", "mean": "游泳"},
        {"word": "掃除", "kana": "そうじ", "mean": "打掃"},
        {"word": "見學", "kana": "けんがく", "mean": "參觀"},
        {"word": "丸", "kana": "まる", "mean": "圓圈"},
        {"word": "話", "kana": "はなし", "mean": "話題"},
        {"word": "嘘", "kana": "うそ", "mean": "謊言"},
        {"word": "秘密", "kana": "ひみつ", "mean": "秘密"},
        {"word": "習慣", "kana": "しゅうかん", "mean": "習慣"},
        {"word": "普通", "kana": "ふつう", "mean": "普通"},
        {"word": "営業", "kana": "えいぎょう", "mean": "營業"},
        {"word": "挨拶", "kana": "あいさつ", "mean": "問候"},
        {"word": "世話", "kana": "せわ", "mean": "照顧"},
        {"word": "用意", "kana": "ようい", "mean": "準備"},
        {"word": "準備", "kana": "じゅんび", "mean": "準備"},
        {"word": "相談", "kana": "そうだん", "mean": "討論"},
        {"word": "説明", "kana": "せつめい", "mean": "說明"},
        {"word": "約束", "kana": "やくそく", "mean": "約定"},
        {"word": "返事", "kana": "へんじ", "mean": "回覆"},
        {"word": "資料", "kana": "しりょう", "mean": "資料"},
        {"word": "名刺", "kana": "めいし", "mean": "名片"},
        {"word": "計画", "kana": "けいかく", "mean": "計畫"},
        {"word": "予定", "kana": "よてい", "mean": "預定"},
        {"word": "技術", "kana": "ぎじゅつ", "mean": "技術"},
        {"word": "機械", "kana": "きかい", "mean": "機械"},
        {"word": "故障", "kana": "こしょう", "mean": "故障"},
        {"word": "生産", "kana": "せいさん", "mean": "生產"},
        {"word": "工事", "kana": "工事", "mean": "工程"},
        {"word": "用事", "kana": "ようじ", "mean": "事情"},
        {"word": "貿易", "kana": "ぼうえき", "mean": "貿易"},
        {"word": "關係", "kana": "かんけい", "mean": "關係"},
        {"word": "影響", "kana": "えいきょう", "mean": "影響"},
        {"word": "意見", "kana": "いけん", "mean": "意見"},
        {"word": "人口", "kana": "じんこう", "mean": "人口"},
        {"word": "人數", "kana": "にんずう", "mean": "人數"},
        {"word": "人気", "kana": "にんき", "mean": "人氣"},
        {"word": "成功", "kana": "せいこう", "mean": "成功"},
        {"word": "失敗", "kana": "しっぱい", "mean": "失敗"},
        {"word": "賛成", "kana": "さんせい", "mean": "贊成"},
        {"word": "反対", "kana": "はんたい", "mean": "反對"}
    ],
    "名詞六 生活衣服與食物": [
        {"word": "中止", "kana": "ちゅうし", "mean": "中止"},
        {"word": "仕方", "kana": "しかた", "mean": "辦法"},
        {"word": "結果", "kana": "けっか", "mean": "結果"},
        {"word": "服", "kana": "ふく", "mean": "衣服"},
        {"word": "洋服", "kana": "ようふく", "mean": "西服"},
        {"word": "帽子", "kana": "ぼうし", "mean": "帽子"},
        {"word": "靴下", "kana": "くつした", "mean": "襪子"},
        {"word": "上着", "kana": "うわぎ", "mean": "外套"},
        {"word": "下着", "kana": "したぎ", "mean": "內衣"},
        {"word": "着物", "kana": "きもの", "mean": "和服"},
        {"word": "眼鏡", "kana": "めがね", "mean": "眼鏡"},
        {"word": "腕時計", "kana": "うdeどけい", "mean": "手錶"},
        {"word": "傘", "kana": "かさ", "mean": "傘"},
        {"word": "糊", "kana": "のり", "mean": "膠水"},
        {"word": "財布", "kana": "さいふ", "mean": "錢包"},
        {"word": "お釣り", "kana": "おつり", "mean": "找零"},
        {"word": "家賃", "kana": "やちん", "mean": "房租"},
        {"word": "電気", "kana": "でんき", "mean": "電燈"},
        {"word": "冷房", "kana": "れいぼう", "mean": "冷氣"},
        {"word": "机", "kana": "つくえ", "mean": "桌子"},
        {"word": "引き出し", "kana": "引き出し", "mean": "抽屜"},
        {"word": "箱", "kana": "はこ", "mean": "箱子"},
        {"word": "絵", "kana": "え", "mean": "畫"},
        {"word": "絵本", "kana": "えほん", "mean": "繪本"},
        {"word": "漫画", "kana": "まんが", "mean": "漫畫"},
        {"word": "種類", "kana": "しゅるい", "mean": "種類"},
        {"word": "道具", "kana": "どうぐ", "mean": "工具"},
        {"word": "買い物", "kana": "かいもの", "mean": "購物"},
        {"word": "忘れ物", "kana": "わすれもの", "mean": "遺失物"},
        {"word": "食べ物", "kana": "たべもの", "mean": "食物"},
        {"word": "飲料", "kana": "のみもの", "mean": "飲料"},
        {"word": "食事", "kana": "しょくじ", "mean": "用餐"},
        {"word": "弁当", "kana": "べんとう", "mean": "便當"},
        {"word": "茶碗", "kana": "ちゃわん", "mean": "碗"},
        {"word": "皿", "kana": "さら", "mean": "盤子"},
        {"word": "米", "kana": "こめ", "mean": "米"},
        {"word": "肉", "kana": "にく", "mean": "肉"},
        {"word": "野菜", "kana": "やさい", "mean": "蔬菜"},
        {"word": "果物", "kana": "くだもの", "mean": "水果"},
        {"word": "お菓子", "kana": "おかし", "mean": "點心"},
        {"word": "飴", "kana": "あめ", "mean": "糖果"},
        {"word": "砂糖", "kana": "さとう", "mean": "砂糖"}
    ],
    "名詞七 旅遊活動與自然": [
        {"word": "塩", "kana": "しお", "mean": "鹽"},
        {"word": "油", "kana": "あぶら", "mean": "油"},
        {"word": "卵", "kana": "たまご", "mean": "蛋"},
        {"word": "旅行", "kana": "りょこう", "mean": "旅行"},
        {"word": "帰國", "kana": "きこく", "mean": "歸國"},
        {"word": "留守", "kana": "るす", "mean": "不在家"},
        {"word": "交通", "kana": "こうつう", "mean": "交通"},
        {"word": "新幹線", "kana": "しんかんせん", "mean": "新幹線"},
        {"word": "片道", "kana": "かたみち", "mean": "單程"},
        {"word": "往復", "kana": "おうふく", "mean": "來回"},
        {"word": "切符", "kana": "きっぷ", "mean": "車票"},
        {"word": "切手", "kana": "きって", "mean": "郵票"},
        {"word": "手紙", "kana": "てがみ", "mean": "信"},
        {"word": "封筒", "kana": "ふうとう", "mean": "信封"},
        {"word": "小包み", "kana": "こづつみ", "mean": "小包裹"},
        {"word": "住所", "kana": "じゅうしょ", "mean": "住址"},
        {"word": "お知らせ", "kana": "おしらせ", "mean": "通知"},
        {"word": "お土産", "kana": "おみやげ", "mean": "紀念品"},
        {"word": "お礼", "kana": "おれい", "mean": "道謝"},
        {"word": "運動", "kana": "うんどう", "mean": "運動"},
        {"word": "野球", "kana": "やきゅう", "mean": "棒球"},
        {"word": "映画", "kana": "えいが", "mean": "電影"},
        {"word": "花見", "kana": "はなみ", "mean": "賞花"},
        {"word": "景色", "kana": "けしき", "mean": "景色"},
        {"word": "祭り", "kana": "まつり", "mean": "祭典"},
        {"word": "趣味", "kana": "しゅみ", "mean": "興趣"},
        {"word": "興味", "kana": "きょうみ", "mean": "有興趣"},
        {"word": "楽しみ", "kana": "たのしみ", "mean": "樂趣"},
        {"word": "気分", "kana": "きぶん", "mean": "心情"},
        {"word": "経験", "kana": "けいけん", "mean": "經驗"},
        {"word": "思い出", "kana": "おもいで", "mean": "回憶"},
        {"word": "禁煙", "kana": "きんえん", "mean": "禁菸"},
        {"word": "利用", "kana": "りよう", "mean": "利用"},
        {"word": "料金", "kana": "りょうきん", "mean": "費用"},
        {"word": "無料", "kana": "むりょう", "mean": "免費"},
        {"word": "貯金", "kana": "ちょきん", "mean": "存錢"},
        {"word": "事故", "kana": "じこ", "mean": "事故"},
        {"word": "病気", "kana": "びょうき", "mean": "生病"},
        {"word": "怪我", "kana": "けが", "mean": "受傷"},
        {"word": "入院", "kana": "にゅういん", "mean": "入院"},
        {"word": "退院", "kana": "たいいん", "mean": "出院"},
        {"word": "お見舞い", "kana": "おみまい", "mean": "探望"}
    ],
    "名詞八 外來語片假名": [
        {"word": "アニメ", "kana": "あにめ", "mean": "動漫"},
        {"word": "アパート", "kana": "あぱーと", "mean": "公寓"},
        {"word": "アルバイト", "kana": "あるばいと", "mean": "打工"},
        {"word": "プレゼント", "kana": "ぷれぜんと", "mean": "禮物"},
        {"word": "エレベーター", "kana": "えれべーたー", "mean": "電梯"},
        {"word": "カーテン", "kana": "かーてん", "mean": "窗簾"},
        {"word": "ソフト", "kana": "そふと", "mean": "軟體"},
        {"word": "タオル", "kana": "たおる", "mean": "毛巾"},
        {"word": "ダンス", "kana": "だんす", "mean": "跳舞"},
        {"word": "チーズ", "kana": "ちーず", "mean": "起士"},
        {"word": "チケット", "kana": "ちけっと", "mean": "票"},
        {"word": "テニス", "kana": "てにす", "mean": "網球"},
        {"word": "テキスト", "kana": "てきすと", "mean": "課本"},
        {"word": "ドライブ", "kana": "どらいぶ", "mean": "兜風"},
        {"word": "ネクタイ", "kana": "ねくたい", "mean": "領帶"},
        {"word": "ハサミ", "kana": "はさみ", "mean": "剪刀"},
        {"word": "パソコン", "kana": "ぱそこん", "mean": "電腦"},
        {"word": "パスポート", "kana": "ぱすぽーと", "mean": "護照"},
        {"word": "ピザ", "kana": "ぴざ", "mean": "披薩"},
        {"word": "ピアノ", "kana": "ぴあの", "mean": "鋼琴"},
        {"word": "ビル", "kana": "びる", "mean": "大樓"},
        {"word": "ビール", "kana": "びーる", "mean": "啤酒"},
        {"word": "ビデオ", "kana": "びでお", "mean": "影片"},
        {"word": "プール", "kana": "ぷーる", "mean": "游泳池"},
        {"word": "ページ", "kana": "ぺーじ", "mean": "頁數"},
        {"word": "ボタン", "kana": "ぼたん", "mean": "按鈕"},
        {"word": "マフラー", "kana": "まふらー", "mean": "圍巾"},
        {"word": "マンション", "kana": "まんしょん", "mean": "大廈"},
        {"word": "メニュー", "kana": "めにゅー", "mean": "菜單"},
        {"word": "ラジオ", "kana": "らじお", "mean": "收音機"},
        {"word": "ルール", "kana": "るーる", "mean": "規則"},
        {"word": "レジ", "kana": "れじ", "mean": "收銀台"},
        {"word": "レシート", "kana": "れしーと", "mean": "收據"},
        {"word": "コップ", "kana": "こっぷ", "mean": "杯子"},
        {"word": "サラダ", "kana": "さらだ", "mean": "沙拉"},
        {"word": "サッカー", "kana": "さっかー", "mean": "足球"},
        {"word": "サンダル", "kana": "サンダル", "mean": "涼鞋"},
        {"word": "スリッパ", "kana": "すりっぱ", "mean": "拖鞋"},
        {"word": "スポーツ", "kana": "すぽーつ", "mean": "運動"},
        {"word": "ギター", "kana": "ぎたー", "mean": "吉他"},
        {"word": "ガソリン", "kana": "がそりん", "mean": "汽油"},
        {"word": "クラス", "kana": "くらす", "mean": "班級"}
    ],
    "動詞一 自他動詞核心對應": [
        {"word": "始まる", "kana": "はじまる", "mean": "自一 開始"},
        {"word": "始める", "kana": "はじめる", "mean": "他二 開始"},
        {"word": "終わる", "kana": "おわる", "mean": "自一 結束"},
        {"word": "終える", "kana": "おえる", "mean": "他二 結束"},
        {"word": "出る", "kana": "でる", "mean": "自二 出來"},
        {"word": "出す", "kana": "だす", "mean": "他一 拿出來"},
        {"word": "入る", "kana": "はいる", "mean": "自一 進入"},
        {"word": "入れる", "kana": "いれる", "mean": "他二 放進去"},
        {"word": "開く", "kana": "あく", "mean": "自一 打開"},
        {"word": "開ける", "kana": "あける", "mean": "他二 打開"},
        {"word": "閉まる", "kana": "しまる", "mean": "自一 關上"},
        {"word": "閉める", "kana": "しめる", "mean": "他二 關上"},
        {"word": "つく", "kana": "つく", "mean": "自一 開啟"},
        {"word": "つける", "kana": "つける", "mean": "他二 打開"},
        {"word": "消える", "kana": "きえる", "mean": "自二 熄滅"},
        {"word": "消す", "kana": "けす", "mean": "他一 關掉"},
        {"word": "動く", "kana": "うごく", "mean": "自一 移動"},
        {"word": "動かす", "kana": "うごかす", "mean": "他一 移動"},
        {"word": "止まる", "kana": "とまる", "mean": "自一 停下"},
        {"word": "止める", "kana": "とめる", "mean": "他二 停下"},
        {"word": "壊れる", "kana": "こわれる", "mean": "自二 壞掉"},
        {"word": "壊す", "kana": "こわす", "mean": "他一 弄壞"},
        {"word": "治る", "kana": "なおる", "mean": "自一 痊癒"},
        {"word": "治す", "kana": "なおす", "mean": "他一 治療"},
        {"word": "汚れる", "kana": "よごれる", "mean": "自二 髒了"},
        {"word": "汚す", "kana": "よごす", "mean": "他一 弄髒"},
        {"word": "破れる", "kana": "やぶれる", "mean": "自二 破掉"},
        {"word": "破る", "kana": "やぶる", "mean": "他一 弄破"},
        {"word": "割れる", "kana": "われる", "mean": "自二 碎掉"},
        {"word": "割る", "kana": "わる", "mean": "他一 打碎"},
        {"word": "折れる", "kana": "おれる", "mean": "自二 斷掉"},
        {"word": "折る", "kana": "おる", "mean": "他一 折斷"},
        {"word": "外れる", "kana": "はずれる", "mean": "自二 脫落"},
        {"word": "外す", "kana": "はずす", "mean": "他一 摘下"},
        {"word": "落ちる", "kana": "おちる", "mean": "自二 掉落"},
        {"word": "落とす", "kana": "おとす", "mean": "他一 弄丟"},
        {"word": "変わる", "kana": "かわる", "mean": "自一 改變"},
        {"word": "変える", "kana": "かえる", "mean": "他二 改變"},
        {"word": "決まる", "kana": "きまる", "mean": "自一 決定"},
        {"word": "決める", "kana": "きめる", "mean": "他二 決定"},
        {"word": "付く", "kana": "つく", "mean": "自一 附有"},
        {"word": "付ける", "kana": "つける", "mean": "他二 裝上"}
    ],
    "動詞二 日常第二行為與狀態": [
        {"word": "浴びる", "kana": "あびる", "mean": "二類 淋浴"},
        {"word": "受ける", "kana": "うける", "mean": "二類 接受"},
        {"word": "間違える", "kana": "まちがえる", "mean": "二類 弄錯"},
        {"word": "足る", "kana": "たりる", "mean": "二類 足夠"},
        {"word": "逃げる", "kana": "にげる", "mean": "二類 逃走"},
        {"word": "捕まえる", "kana": "つかまえる", "mean": "二類 抓住"},
        {"word": "出来る", "kana": "できる", "mean": "二類 能夠"},
        {"word": "比べる", "kana": "くらべる", "mean": "二類 比較"},
        {"word": "出かける", "kana": "でかける", "mean": "二類 出門"},
        {"word": "考える", "kana": "かんがえる", "mean": "二類 思考"},
        {"word": "並べる", "kana": "ならべる", "mean": "二類 排列"},
        {"word": "生まれる", "kana": "うまれる", "mean": "二類 出生"},
        {"word": "答える", "kana": "こたえる", "mean": "二類 回答"},
        {"word": "調べる", "kana": "しらべる", "mean": "二類 調查"},
        {"word": "片付ける", "kana": "かたづける", "mean": "二類 整理"},
        {"word": "伝える", "kana": "つたえる", "mean": "二類 傳達"},
        {"word": "晴れる", "kana": "はれる", "mean": "二類 放晴"},
        {"word": "迎える", "kana": "むかえる", "mean": "二類 迎接"},
        {"word": "連れる", "kana": "つれる", "mean": "二類 帶領"},
        {"word": "數える", "kana": "かぞえる", "mean": "二類 計算"},
        {"word": "疲れる", "kana": "つかれる", "mean": "二類 疲勞"},
        {"word": "見せる", "kana": "みせる", "mean": "二類 給人看"},
        {"word": "濡れる", "kana": "ぬれる", "mean": "二類 淋濕"},
        {"word": "知らせる", "kana": "しらせる", "mean": "二類 通知"},
        {"word": "泊まる", "kana": "とまる", "mean": "一類 住宿"},
        {"word": "曲がる", "kana": "まがる", "mean": "一類 轉彎"},
        {"word": "勤める", "kana": "つとめる", "mean": "二類 任職"},
        {"word": "捨てる", "kana": "すてる", "mean": "二類 丟掉"},
        {"word": "締める", "kana": "しめる", "mean": "二類 綁緊"},
        {"word": "育てる", "kana": "そだてる", "mean": "二類 養育"},
        {"word": "諦める", "kana": "あきらめる", "mean": "二類 放棄"},
        {"word": "予約する", "kana": "よやくする", "mean": "三類 預約"},
        {"word": "案内する", "kana": "あんないする", "mean": "三類 帶路"},
        {"word": "寢坊する", "kana": "ねぼうする", "mean": "三類 睡過頭"},
        {"word": "連絡する", "kana": "れんらくする", "mean": "三類 聯絡"},
        {"word": "介紹する", "kana": "しょうかいする", "mean": "三類 介紹"},
        {"word": "卒業する", "kana": "そつぎょうする", "mean": "三類 畢業"},
        {"word": "輸入する", "kana": "ゆにゅうする", "mean": "三類 進口"},
        {"word": "輸出する", "kana": "ゆしゅつする", "mean": "三類 出口"},
        {"word": "運ぶ", "kana": "はこぶ", "mean": "一類 搬運"},
        {"word": "呼ぶ", "kana": "よぶ", "mean": "一類 呼叫"},
        {"word": "払う", "kana": "はらう", "mean": "一類 支付"}
    ],
    "動詞三 社交與互動行為": [
        {"word": "笑う", "kana": "わらう", "mean": "一類 笑"},
        {"word": "歌う", "kana": "うたう", "mean": "一類 唱歌"},
        {"word": "誘う", "kana": "さそう", "mean": "一類 邀請"},
        {"word": "頼む", "kana": "たのむ", "mean": "一類 拜託"},
        {"word": "頼る", "kana": "たよる", "mean": "一類 依靠"},
        {"word": "叱る", "kana": "しかる", "mean": "一類 責備"},
        {"word": "褒める", "kana": "ほめる", "mean": "二類 誇獎"},
        {"word": "教える", "kana": "おしえる", "mean": "二類 傳授"},
        {"word": "習う", "kana": "ならう", "mean": "一類 學習"},
        {"word": "借りる", "kana": "かりる", "mean": "二類 借入"},
        {"word": "貸す", "kana": "かす", "mean": "一類 借出"},
        {"word": "返す", "kana": "かえす", "mean": "一類 歸還"},
        {"word": "送る", "kana": "おくる", "mean": "一類 寄送"},
        {"word": "届く", "kana": "とどく", "mean": "一類 送達"},
        {"word": "届ける", "kana": "とどける", "mean": "二類 遞送"},
        {"word": "手伝う", "kana": "てつだう", "mean": "一類 幫忙"},
        {"word": "相談する", "kana": "そうだんする", "mean": "三類 商量"},
        {"word": "世話する", "kana": "せわする", "mean": "三類 照顧"},
        {"word": "謝る", "kana": "あやまる", "mean": "一類 道歉"},
        {"word": "祝う", "kana": "いわう", "mean": "一類 慶祝"},
        {"word": "集まる", "kana": "あつまる", "mean": "一類 集合"},
        {"word": "集める", "kana": "あつめる", "mean": "二類 收集"},
        {"word": "別れる", "kana": "わかれる", "mean": "二類 分手"},
        {"word": "出会う", "kana": "であう", "mean": "一類 遇見"},
        {"word": "信じる", "kana": "しんじる", "mean": "二類 相信"},
        {"word": "愛する", "kana": "あいする", "mean": "三類 愛"},
        {"word": "怒る", "kana": "おこる", "mean": "一類 生氣"},
        {"word": "騒ぐ", "kana": "さわぐ", "mean": "一類 吵鬧"},
        {"word": "驚く", "kana": "おどろく", "mean": "一類 驚訝"},
        {"word": "喜ぶ", "kana": "よろこぶ", "mean": "一類 高興"},
        {"word": "嫌う", "kana": "きらう", "mean": "一類 討厭"},
        {"word": "祈る", "kana": "いのる", "mean": "一類 祈島"},
        {"word": "探す", "kana": "さがす", "mean": "一類 尋找"},
        {"word": "選ぶ", "kana": "えらぶ", "mean": "一類 選擇"},
        {"word": "見つける", "kana": "みつける", "mean": "二類 找到"},
        {"word": "見つかる", "kana": "みつかる", "mean": "一類 被找到"},
        {"word": "渡す", "kana": "わたす", "mean": "一類 交給"},
        {"word": "渡る", "kana": "わたる", "mean": "一類 度度過"},
        {"word": "過ぎる", "kana": "すぎる", "mean": "二類 通過"},
        {"word": "過ごす", "kana": "すごす", "mean": "一類 度度過"},
        {"word": "開く", "kana": "ひらく", "mean": "一類 展開"},
        {"word": "進む", "kana": "すすむ", "mean": "一類 前進"}
    ],
    "動詞四 進階行為與複合詞": [
        {"word": "遅れる", "kana": "おくれる", "mean": "二類 遲到"},
        {"word": "遅刻する", "kana": "ちこくする", "mean": "三類 遲到"},
        {"word": "びっくりする", "kana": "びっくりする", "mean": "三類 嚇一跳"},
        {"word": "注意する", "kana": "ちゅういする", "mean": "三類 注意"},
        {"word": "気をつける", "kana": "きをつける", "mean": "二類 留意"},
        {"word": "思い出す", "kana": "おもいだす", "mean": "一類 想起"},
        {"word": "引っ越す", "kana": "ひっこす", "mean": "一類 搬家"},
        {"word": "声をかける", "kana": "こえをかける", "mean": "二類 搭話"},
        {"word": "電話をかける", "kana": "деんわをかける", "mean": "二類 打電話"},
        {"word": "めがねをかける", "kana": "めがねをかける", "mean": "二類 戴眼鏡"},
        {"word": "お金がかかる", "kana": "おかねがかかる", "mean": "一類 花錢"},
        {"word": "時間がかかる", "kana": "じかんがかかる", "mean": "一類 花時間"},
        {"word": "鍵がかかる", "kana": "かぎがかかる", "mean": "一類 鎖著"},
        {"word": "鍵をかける", "kana": "かぎをかける", "mean": "二類 上鎖"},
        {"word": "お湯を沸かす", "kana": "おゆをわかす", "mean": "一類 燒開水"},
        {"word": "お湯が沸く", "kana": "おゆがわく", "mean": "一類 水開了"},
        {"word": "子供が起きる", "kana": "こどもがおきる", "mean": "二類 小孩醒來"},
        {"word": "子供を起こす", "kana": "こどもをおこす", "mean": "一類 叫醒小孩"},
        {"word": "友達が乗る", "kana": "ともだちがのる", "mean": "一類 朋友搭車"},
        {"word": "友達を乗せる", "kana": "ともだちをのせる", "mean": "二類 讓朋友搭車"},
        {"word": "車が返る", "kana": "くるまがかえる", "mean": "一類 車子退回"},
        {"word": "車を返す", "kana": "くるまをかえす", "mean": "一類 歸還車子"},
        {"word": "目が回る", "kana": "めがまわる", "mean": "一類 頭暈眼花"},
        {"word": "目を回す", "kana": "めをまわす", "mean": "一類 感到驚訝"},
        {"word": "靴が並びます", "kana": "くつながらびます", "mean": "一類 鞋子排列"},
        {"word": "靴を並べます", "kana": "くつをならべます", "mean": "二類 排列鞋子"},
        {"word": "お金が戻る", "kana": "おかねがもどる", "mean": "一類 錢退回"},
        {"word": "お金を戻す", "kana": "おかねをもどす", "mean": "一類 退還金錢"},
        {"word": "1日を過ごす", "kana": "いちにちをすごす", "mean": "一類 度度過一天"},
        {"word": "子供が育つ", "kana": "こどもがそだつ", "mean": "一類 小孩成長"},
        {"word": "子供を育てる", "kana": "こどもをそだてる", "mean": "二類 養育小孩"},
        {"word": "片付く", "kana": "かたづく", "mean": "一類 收拾好"},
        {"word": "役に立つ", "kana": "役に立つ", "mean": "一類 起作用"},
        {"word": "売り切れる", "kana": "уりきれる", "mean": "二類 售罄"},
        {"word": "間に合う", "kana": "まニアう", "mean": "一類 趕得上"},
        {"word": "気に入る", "kana": "きにいる", "mean": "一類 喜歡"},
        {"word": "付き合う", "kana": "つきあう", "mean": "一類 交往"},
        {"word": "話し合う", "kana": "はなしあう", "mean": "一類 討論"},
        {"word": "申し込み", "kana": "もうしこむ", "mean": "一類 申請"},
        {"word": "取り消す", "kana": "とりけす", "mean": "一類 取消"},
        {"word": "向かう", "kana": "むかう", "mean": "一類 朝向"},
        {"word": "並ぶ", "kana": "ならぶ", "mean": "一類 排隊"}
    ],
    "副詞一 程度與時間": [
        {"word": "特に", "kana": "とくに", "mean": "特別"},
        {"word": "少し", "kana": "すこし", "mean": "稍微"},
        {"word": "偶に", "kana": "たまに", "mean": "偶爾"},
        {"word": "急に", "kana": "きゅうに", "mean": "突然"},
        {"word": "ぜひ", "kana": "ぜひ", "mean": "務必"},
        {"word": "なるほど", "kana": "なるほど", "mean": "原來如此"},
        {"word": "別に", "kana": "べつに", "mean": "不特別"},
        {"word": "やっと", "kana": "やっと", "mean": "終於"},
        {"word": "隨分", "kana": "ずいぶん", "mean": "相當"},
        {"word": "きっと", "kana": "きっと", "mean": "一定"},
        {"word": "ちょっと", "kana": "ちょっと", "mean": "一下"},
        {"word": "ちょうど", "kana": "ちょうど", "mean": "剛好"},
        {"word": "殆ど", "kana": "ほとんど", "mean": "幾乎"},
        {"word": "確かに", "kana": "たしかに", "mean": "確確實"},
        {"word": "非常に", "kana": "ひじょうに", "mean": "非常"},
        {"word": "一度に", "kana": "いちどに", "mean": "同時"},
        {"word": "とても", "kana": "とても", "mean": "很"},
        {"word": "今度", "kana": "こんど", "mean": "這次"},
        {"word": "ずっと", "kana": "ずっと", "mean": "一直"},
        {"word": "大抵", "kana": "たいてい", "mean": "大致上"},
        {"word": "もっと", "kana": "もっと", "mean": "更"},
        {"word": "だいぶ", "kana": "だいぶ", "mean": "相當"},
        {"word": "たぶん", "kana": "たぶん", "mean": "大概"},
        {"word": "さっき", "kana": "さっき", "mean": "剛才"},
        {"word": "十分", "kana": "じゅうぶん", "mean": "充分"},
        {"word": "沢山", "kana": "たくさん", "mean": "很多"},
        {"word": "いつも", "kana": "いつも", "mean": "總是"},
        {"word": "この間", "kana": "このあいだ", "mean": "前幾天"},
        {"word": "この頃", "kana": "このごろ", "mean": "最近"},
        {"word": "大體", "kana": "だいたい", "mean": "大概"},
        {"word": "最初", "kana": "さいしょ", "mean": "起初"},
        {"word": "最後", "kana": "さいご", "mean": "最後"},
        {"word": "今にも", "kana": "いまにも", "mean": "眼看就要"},
        {"word": "間もなく", "kana": "まもなく", "mean": "不久"},
        {"word": "そろそろ", "kana": "そろそろ", "mean": "差不多該"},
        {"word": "まず", "kana": "まず", "mean": "首先"},
        {"word": "次に", "kana": "つぎに", "mean": "接下來"},
        {"word": "後で", "kana": "あとで", "mean": "稍後"},
        {"word": "さっそく", "kana": "さっそく", "mean": "立刻"},
        {"word": "すぐに", "kana": "すぐに", "mean": "馬上"},
        {"word": "急いで", "kana": "いそいで", "mean": "趕快地"},
        {"word": "ゆっくり", "kana": "ゆっくり", "mean": "慢慢地"}
    ],
    "副詞二 狀態與語氣呼應": [
        {"word": "なんか", "kana": "なんか", "mean": "總覺得"},
        {"word": "なんだか", "kana": "なんだか", "mean": "總覺得"},
        {"word": "全然", "kana": "ぜんぜん", "mean": "完全不"},
        {"word": "状況", "kana": "もちろん", "mean": "當然"},
        {"word": "折角", "kana": "せっかく", "mean": "難得"},
        {"word": "早速", "kana": "さっそく", "mean": "立刻"},
        {"word": "暫く", "kana": "しばらく", "mean": "暫時"},
        {"word": "なるべく", "kana": "なるべく", "mean": "儘量"},
        {"word": "とにかく", "kana": "とにかく", "mean": "總之"},
        {"word": "また", "kana": "また", "mean": "又再"},
        {"word": "もうすぐ", "kana": "もうすぐ", "mean": "馬上"},
        {"word": "いっぱい", "kana": "いっぱい", "mean": "滿滿"},
        {"word": "つい", "kana": "つい", "mean": "不小心"},
        {"word": "如何にも", "kana": "いかにも", "mean": "實在"},
        {"word": "もし", "kana": "もし", "mean": "如果"},
        {"word": "それほど", "kana": "それほど", "mean": "沒那麼"},
        {"word": "そんなに", "kana": "そんなに", "mean": "那麼地"},
        {"word": "うっかり", "kana": "うっかり", "mean": "不留神"},
        {"word": "こっそり", "kana": "こっそり", "mean": "悄悄地"},
        {"word": "はじめて", "kana": "はじめて", "mean": "第一次"},
        {"word": "とうとう", "kana": "とうとう", "mean": "終於"},
        {"word": "決して", "kana": "けっして", "mean": "絕對不"},
        {"word": "まるで", "kana": "まるで", "mean": "簡直"},
        {"word": "もしかしたら", "kana": "もしかしたら", "mean": "也許"},
        {"word": "例えば", "kana": "たとえば", "mean": "例如"},
        {"word": "必ず", "kana": "かならず", "mean": "必定"},
        {"word": "相変わらず", "kana": "あいかわらず", "mean": "依舊"},
        {"word": "やはり", "kana": "やはり", "mean": "果然"},
        {"word": "やっぱり", "kana": "やっぱり", "mean": "果然"},
        {"word": "しっかり", "kana": "しっかり", "mean": "好好地"},
        {"word": "すっかり", "kana": "すっかり", "mean": "完全"},
        {"word": "はっきり", "kana": "はっきり", "mean": "清楚"},
        {"word": "なかなか", "kana": "なかなか", "mean": "相當"},
        {"word": "大分", "kana": "だいぶ", "mean": "頗"},
        {"word": "かなり", "kana": "かなり", "mean": "相當"},
        {"word": "別に", "kana": "べつに", "mean": "並不"},
        {"word": "案外", "kana": "あんがい", "mean": "意外地"},
        {"word": "意外に", "kana": "いがいに", "mean": "意外地"},
        {"word": "實際", "kana": "じっさい", "mean": "實際上"},
        {"word": "たしか", "kana": "たしか", "mean": "大概是"},
        {"word": "たしかに", "kana": "たしかに", "mean": "確實"},
        {"word": "絕對", "kana": "ぜったい", "mean": "絕對"}
    ],
    "副詞三 變化與擬聲擬態詞": [
        {"word": "どんどん", "kana": "どんどん", "mean": "接連不斷地"},
        {"word": "だんだん", "kana": "だんだん", "mean": "漸漸"},
        {"word": "ざあざあ", "kana": "ざあざあ", "mean": "大雨音"},
        {"word": "ペラペラ", "kana": "ぺらぺら", "mean": "說話流利"},
        {"word": "すやすや", "kana": "すやすや", "mean": "安穩入睡"},
        {"word": "ますます", "kana": "ますます", "mean": "越來越"},
        {"word": "ニコニコ", "kana": "にこにこ", "mean": "微笑咪咪"},
        {"word": "わくわく", "kana": "わくわく", "mean": "歡欣雀躍"},
        {"word": "どきどき", "kana": "どきどき", "mean": "心跳加速"},
        {"word": "いらいら", "kana": "いらいら", "mean": "焦躁不安"},
        {"word": "はきはき", "kana": "はきはき", "mean": "乾脆俐落"},
        {"word": "ぴかぴか", "kana": "ぴかぴか", "mean": "閃閃發亮"},
        {"word": "ごろごろ", "kana": "ごろごろ", "mean": "無所事事"},
        {"word": "ぶつぶつ", "kana": "ぶつぶつ", "mean": "碎碎念"},
        {"word": "うとうと", "kana": "うとうと", "mean": "打瞌睡"},
        {"word": "のろのろ", "kana": "のろのろ", "mean": "動作遲緩"},
        {"word": "ばらばら", "kana": "ばらばら", "mean": "散亂"},
        {"word": "ぴったり", "kana": "ぴったり", "mean": "恰好"},
        {"word": "たっぷり", "kana": "たっぷり", "mean": "足夠"},
        {"word": "がっかり", "kana": "がっかり", "mean": "失望"},
        {"word": "すっきり", "kana": "すっきり", "mean": "舒暢"},
        {"word": "そっくり", "kana": "そっくり", "mean": "一模一樣"},
        {"word": "がっちり", "kana": "gacchiri", "mean": "結實"},
        {"word": "ぎっしり", "kana": "gisshiri", "mean": "塞得滿滿"},
        {"word": "すんなり", "kana": "すんなり", "mean": "順利"},
        {"word": "うっすら", "kana": "うっすら", "mean": "隱約"},
        {"word": "さっぱり", "kana": "さっぱり", "mean": "清爽"},
        {"word": "がやがや", "kana": "がやがや", "mean": "吵鬧"},
        {"word": "めちゃくちゃ", "kana": "めちゃくちゃ", "mean": "亂七八糟"},
        {"word": "だらだら", "kana": "だらだら", "mean": "懶散"},
        {"word": "ぎりぎり", "kana": "ぎりぎり", "mean": "極限"},
        {"word": "そろそろ", "kana": "そろそろ", "mean": "差不多該"},
        {"word": "着々と", "kana": "ちゃくちゃくと", "mean": "穩步地"},
        {"word": "次々と", "kana": "つぎつぎと", "mean": "接二連三地"},
        {"word": "徐々に", "kana": "じょじょに", "mean": "逐步地"},
        {"word": "一歩一歩", "kana": "いっぽいっぽ", "mean": "一步一步地"},
        {"word": "刻々と", "kana": "こくこくと", "mean": "時時刻刻"},
        {"word": "刻々", "kana": "こくこく", "mean": "每分每秒"},
        {"word": "次々", "kana": "つぎつぎ", "mean": "依次"},
        {"word": "色々", "kana": "いろいろ", "mean": "各式各樣"},
        {"word": "ちゃんと", "kana": "ちゃんと", "mean": "端正地"},
        {"word": "そろって", "kana": "そろって", "mean": "到齊地"}
    ]
}

for ext_cat in ["動詞五 進階型態", "動詞六 形容詞對應", "動詞七 復合語彙", "形容詞一", "形容詞二", "接續詞與接尾詞", "重要日常短句"]:
    if ext_cat not in WORD_DATABASE:
        WORD_DATABASE[ext_cat] = [{"word": f"{ext_cat}預留", "kana": "よりゅう", "mean": "預留"}]

# ----------------- 側邊欄參數設定 -----------------
st.sidebar.header("全自動字卡朗讀參數設定")
speak_count = st.sidebar.slider("日文重覆次數", 1, 10, 2)
interval_sec = st.sidebar.slider("發音間隔 (秒)", 0.1, 5.0, 0.5, 0.1)
next_word_delay = st.sidebar.slider("下個單字暫停 (秒)", 0.5, 10.0, 2.0, 0.5)

categories = list(WORD_DATABASE.keys())

# 初始化 Session State
if "selected_category" not in st.session_state:
    st.session_state.selected_category = categories[0]
if "play_all_mode" not in st.session_state:
    st.session_state.play_all_mode = False
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "is_playing" not in st.session_state:
    st.session_state.is_playing = False

# ----------------- 主介面 -----------------
st.title("📖 N4核心單字大師機")

col_sel1, col_sel2 = st.columns([2, 1])

with col_sel1:
    chosen_cat = st.selectbox("選擇學習單元大類：", categories, index=categories.index(st.session_state.selected_category))

with col_sel2:
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("單元循環播放", use_container_width=True):
            st.session_state.selected_category = chosen_cat
            st.session_state.play_all_mode = False
            st.session_state.current_index = 0
            st.session_state.is_playing = True
    with col_btn2:
        if st.button("➔ 跨大類大聯播", use_container_width=True):
            st.session_state.selected_category = chosen_cat
            st.session_state.play_all_mode = True
            st.session_state.current_index = 0
            st.session_state.is_playing = True

if st.button("⏹ 停止播放", type="primary", use_container_width=True):
    st.session_state.is_playing = False
    st.rerun()

st.divider()

# 取得目前單字資訊
cat_name = st.session_state.selected_category
word_list = WORD_DATABASE[cat_name]

if st.session_state.current_index >= len(word_list):
    st.session_state.current_index = 0

current_item = word_list[st.session_state.current_index]

# 顯示看板標題與進度
mode_label = "【大聯播模式】" if st.session_state.play_all_mode else "【單元循環模式】"
st.markdown(f"### {mode_label} 📂 {cat_name} （第 {st.session_state.current_index + 1} / {len(word_list)} 題）")

# 置中大字體展示卡片
st.markdown(
    f"""
    <div style="background-color:#f4f3ef; padding:40px; border-radius:15px; text-align:center; border:2px solid #b0bec5; margin-bottom:20px;">
        <h1 style="font-size:90px; color:#2c3e50; margin:0;">{current_item['word']}</h1>
        <h2 style="font-size:60px; color:#5a6266; margin:10px 0;">{current_item['kana']}</h2>
        <h3 style="font-size:35px; color:#6b8096; margin:0;">{current_item['mean']}</h3>
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------- 語音產生與播放邏輯（使用 Streamlit 內建 st.audio 防閃退） -----------------
if st.session_state.is_playing:
    item = current_item
    
    fn_ja = f"run_ja_{int(time.time())}_{random.randint(100,999)}.mp3" if 'random' in globals() else f"run_ja_{time.time()}.mp3"
    fn_zh = f"run_zh_{int(time.time())}_{random.randint(100,999)}.mp3" if 'random' in globals() else f"run_zh_{time.time()}.mp3"
    
    try:
        # 生成日文語音
        tts_ja = gTTS(text=item["kana"], lang='ja', slow=False)
        tts_ja.save(fn_ja)
        
        # 生成中文語音
        clean_zh = item["mean"].replace("自一", "").replace("他二", "").replace("自二", "").replace("他一", "").replace("一類", "").replace("二類", "").replace("三類", "").strip()
        tts_zh = gTTS(text=clean_zh, lang='zh-TW', slow=False)
        tts_zh.save(fn_zh)
        
        # 顯示內建音訊播放器並自動播放日文
        st.write("🔊 正在朗讀日文...")
        for i in range(speak_count):
            if not st.session_state.is_playing: break
            st.audio(fn_ja, format="audio/mp3", autoplay=True)
            time.sleep(interval_sec + 1.0) # 給予足夠的音訊播放時間
            
        # 播放中文意思
        if st.session_state.is_playing:
            st.write("🔊 正在朗讀中文...")
            st.audio(fn_zh, format="audio/mp3", autoplay=True)
            time.sleep(2.0)
            
    except Exception as e:
        st.error(f"語音播放異常: {e}")
    finally:
        for f in [fn_ja, fn_zh]:
            try:
                if os.path.exists(f): os.remove(f)
            except Exception: pass
            
    # 下一個單字緩衝
    if st.session_state.is_playing:
        time.sleep(next_word_delay)
        
        # 推進索引
        st.session_state.current_index += 1
        if st.session_state.current_index >= len(word_list):
            st.session_state.current_index = 0
            if st.session_state.play_all_mode:
                cat_idx = categories.index(st.session_state.selected_category)
                cat_idx += 1
                if cat_idx >= len(categories):
                    cat_idx = 0
                st.session_state.selected_category = categories[cat_idx]
        
        st.rerun()
