import streamlit as st
import random
import time

# キャラクターデータの定義
characters = [
    {
        "name": "ハローキティ",
        "birthday": "11月1日",
        "dream": "ピアニスト",
        "hobby": "クッキーを作ること",
        "like" : "ママが作ったアップルパイ",
        "personality" : "明るくてやさしい",
        "skill" : "音楽",
        "img" : "hellokitty.png"
    },
    {
        "name": "シナモロール",
        "birthday": "3月6日",
        "dream": "レストランのシェフ",
        "hobby": "カフェのテラスでお昼寝",
        "like" : "シナモンロール",
        "personality" : "おとなしいけれど、とても人なつっこい",
        "skill" : "空を飛ぶこと",
        "img" : "cinnamon.png"
    },
    {
        "name": "マイメロディ",
        "birthday": "1月18日",
        "dream": "お菓子屋さん",
        "hobby": "クッキーを焼くこと",
        "like" : "アーモンドパウンドケーキ",
        "personality" : "すなおで明るい",
        "skill" : "お菓子をつくること",
        "img" : "mymelody.png"
    },
    {
        "name": "ポムポムプリン",
        "birthday": "4月16日",
        "dream": "もっともっとおっきくなること",
        "hobby": "くつ集め",
        "like" : "ママが作ったプリン",
        "personality" : "のんびりマイペース",
        "skill" : "だれとでもなかよくなれちゃうこと",
        "img" : "pompompurin.png"
    }
]

# クイズの項目と日本語名のマッピング
QUIZ_ITEMS = {
    "birthday": "誕生日",
    "dream": "夢",
    "hobby": "趣味",
    "like": "好きなもの",
    "personality": "性格",
    "skill": "特技"
}

st.markdown("""
<style>

.main {
    background: linear-gradient(
        180deg,
        #fff0f6 0%,
        #ffe4f2 50%,
        #fff8dc 100%
    );
}

/* タイトル */
h1 {
    text-align: center;
    color: #ff4fa3;
    font-size: 3rem !important;
    font-weight: bold;
}

/* サブタイトル */
h2, h3 {
    color: #ff69b4;
}

/* カード */
.card {
    background-color: white;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0 4px 15px rgba(255,105,180,0.2);
    margin-bottom: 20px;
}

/* ボタン */
.stButton button {
    width: 100%;
    background: linear-gradient(90deg,#ff7eb3,#ff758c);
    color: white;
    border-radius: 15px;
    border: none;
    padding: 12px;
    font-size: 18px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg,#ff5caa,#ff5c7c);
}

/* ラジオボタン */
div[role="radiogroup"] {
    background: white;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.1);
}

/* 成功メッセージ */
.stSuccess {
    border-radius: 15px;
}

/* エラーメッセージ */
.stError {
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

st.title("サンリオキャラクタークイズ")

# セッション状態の初期化
if "stage" not in st.session_state:
    st.session_state.stage = "start"
if "char_index" not in st.session_state:
    st.session_state.char_index = 0  # 0～3
if "quiz_count" not in st.session_state:
    st.session_state.quiz_count = 0  # 0～1
if "current_quiz" not in st.session_state:
    st.session_state.current_quiz = None

# 【修正ポイント】インデックスが範囲内のときだけ安全にキャラクターを取得する
if st.session_state.char_index < len(characters):
    current_char = characters[st.session_state.char_index]
else:
    current_char = None


# --- 1. スタート画面 ---
if st.session_state.stage == "start":
    st.write("キャラクター情報を覚えてね！！")
    if st.button("ゲーム開始！！"):
        st.session_state.stage = "memorize"
        st.rerun()

# --- 2. 記憶画面 ---
elif st.session_state.stage == "memorize" and current_char:
    st.subheader(f"{st.session_state.char_index + 1}人目: {current_char['name']}")
    
    try:
        st.image(current_char["img"], width=300)
    except:
        st.warning(f"画像 '{current_char['img']}' が見つかりません。")
    
    st.write(f"**誕生日:** {current_char['birthday']}")
    st.write(f"**夢:** {current_char['dream']}")
    st.write(f"**趣味:** {current_char['hobby']}")
    st.write(f"**好きなもの:** {current_char['like']}")
    st.write(f"**性格:** {current_char['personality']}")
    st.write(f"**特技:** {current_char['skill']}")

    st.write("---")
    st.write("5秒後にクイズ開始!!")
    
    time.sleep(5)
    st.session_state.stage = "quiz"
    st.session_state.quiz_count = 0
    st.session_state.current_quiz = None
    st.rerun()

# --- 3. クイズ画面 ---
elif st.session_state.stage == "quiz" and current_char:
    st.subheader(f"クイズ（{current_char['name']} からの出題）")
    st.write(f"第 {st.session_state.quiz_count + 1} 問 / 全2問")

    # クイズの生成
    if st.session_state.current_quiz is None:
        quiz_key = random.choice(list(QUIZ_ITEMS.keys()))
        correct_answer = current_char[quiz_key]
        
        dummies = [c[quiz_key] for c in characters if c[quiz_key] != correct_answer]
        dummies = list(set(dummies))
        
        while len(dummies) < 3:
            dummies.append("???")
            
        options = random.sample(dummies, 3) + [correct_answer]
        random.shuffle(options)
        
        st.session_state.current_quiz = {
            "key": quiz_key,
            "question": f"このキャラクターの **{QUIZ_ITEMS[quiz_key]}** はどれ？",
            "correct": correct_answer,
            "options": options
        }

    quiz = st.session_state.current_quiz
    answer = st.radio(quiz["question"], quiz["options"])

    if st.button("回答する"):
        if answer == quiz["correct"]:
            st.success("正解！")
        else:
            st.error(f"不正解！ 正解は「{quiz['correct']}」でした。")
        
        time.sleep(2)
        
        # カウントを進める処理
        st.session_state.quiz_count += 1
        st.session_state.current_quiz = None
        
        if st.session_state.quiz_count >= 2:
            st.session_state.char_index += 1
            # ここで次のキャラがいるかチェック
            if st.session_state.char_index < len(characters):
                st.session_state.stage = "memorize"
            else:
                st.session_state.stage = "end"
        else:
            st.session_state.stage = "quiz"
            
        st.rerun()

# --- 4. 終了画面 ---
elif st.session_state.stage == "end":
    st.subheader("ゲーム終了") 
    st.balloons()
    st.success("みんなについて詳しくなれたかな？また遊ぼうね！！")
    
    if st.button("もう一度遊ぶ"):
        st.session_state.stage = "start"
        st.session_state.char_index = 0
        st.session_state.quiz_count = 0
        st.session_state.current_quiz = None
        st.rerun()
