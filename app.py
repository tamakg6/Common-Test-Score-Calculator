import streamlit as st

def main():
    st.set_page_config(page_title="共テ配点シミュレーターPro", layout="wide")
    st.title("🎓 共通テスト 傾斜配点シミュレーター")
    st.caption("全科目対応・英語比率調整機能付き")

    # --- データ構造定義 ---
    # (科目名, デフォルト満点)
    subjects = {
        "国語": {"max": 200},
        "数学ⅠA": {"max": 100},
        "数学ⅡB/C": {"max": 100},
        "理科①(基礎2科目)": {"max": 100},
        "理科②": {"max": 100},
        "地歴B/探究": {"max": 100},
        "公民": {"max": 100},
        "情報Ⅰ": {"max": 100},
    }

    # --- サイドバー：英語の特殊計算 ---
    st.sidebar.header("📢 英語の配点比率設定")
    r_weight = st.sidebar.slider("リーディングの比率", 0, 100, 50, step=10)
    l_weight = 100 - r_weight
    st.sidebar.write(f"比率 R:{r_weight} : L:{l_weight}")
    
    st.sidebar.divider()
    st.sidebar.info("大学の募集要項に合わせて比率を変えてください。")

    # --- メインエリア ---
    col_score, col_weight = st.columns(2)

    with col_score:
        st.subheader("1. 素点を入力 (点)")
        
        # 英語は特殊なので個別入力
        st.markdown("**【英語】**")
        c_r, c_l = st.columns(2)
        raw_r = c_r.number_input("リーディング(100)", 0, 100, 80)
        raw_l = c_l.number_input("リスニング(100)", 0, 100, 80)
        
        # その他の科目
        st.markdown("**【他科目】**")
        scores = {}
        for sub, info in subjects.items():
            scores[sub] = st.number_input(f"{sub} ({info['max']})", 0, info['max'], 0)

    with col_weight:
        st.subheader("2. 大学の配点設定 (満点)")
        
        # 英語の換算
        target_eigo = st.number_input("英語の合計満点", 0, 400, 200)
        
        # その他の科目
        weights = {}
        for sub, info in subjects.items():
            weights[sub] = st.number_input(f"{sub} の換算満点", 0, 400, info['max'])

    # --- 計算処理 ---
    # 英語の計算（比率考慮）
    # 換算点 = (R素点 * R比率 + L素点 * L比率) / 100 * (大学満点 / 200)
    calc_eigo = ((raw_r * r_weight + raw_l * l_weight) / 100) * (target_eigo / 200)
    
    # 他科目の計算
    results = {}
    for sub, score in scores.items():
        results[sub] = (score / subjects[sub]['max']) * weights[sub]

    total_score = calc_eigo + sum(results.values())
    max_total = target_eigo + sum(weights.values())

    # --- 結果表示 ---
    st.divider()
    st.header("📊 判定結果")
    
    res_c1, res_c2 = st.columns([1, 2])
    
    with res_c1:
        st.metric(label="合計得点", value=f"{total_score:.1f} / {max_total}")
        if max_total > 0:
            percentage = (total_score / max_total) * 100
            st.write(f"### 得点率: **{percentage:.2f}%**")

    with res_c2:
        # 内訳をテーブルで表示
        display_data = {"科目": ["英語（換算後）"], "得点": [f"{calc_eigo:.1f}"]}
        for sub, val in results.items():
            display_data["科目"].append(sub)
            display_data["得点"].append(f"{val:.1f}")
        
        st.table(display_data)

if __name__ == "__main__":
    main()
