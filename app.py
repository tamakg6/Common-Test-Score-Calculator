import streamlit as st

def main():
    st.set_page_config(page_title="共テ配点シミュレーター", layout="wide")
    st.title("🎓 共通テスト 傾斜配点シミュレーター")
    st.caption("科目まとめ換算・英語比率調整対応版")

    # --- 1. 素点の入力セクション ---
    st.header("1. 各科目の素点を入力")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.subheader("📝 国語・情報")
        raw_kokugo = st.number_input("国語 (200)", 0, 200, 0)
        raw_joho = st.number_input("情報Ⅰ (100)", 0, 100, 0)

    with col2:
        st.subheader("🔢 数学")
        raw_math1a = st.number_input("数学ⅠA (100)", 0, 100, 0)
        raw_math2bc = st.number_input("数学ⅡBC (100)", 0, 100, 0)

    with col3:
        st.subheader("🧪 理科")
        raw_sci1 = st.number_input("理科① (100)", 0, 100, 0)
        raw_sci2 = st.number_input("理科② (100)", 0, 100, 0)

    with col4:
        st.subheader("🌍 社会")
        raw_soc1 = st.number_input("社会① (100)", 0, 100, 0)
        raw_soc2 = st.number_input("社会② (100)", 0, 100, 0)

    st.divider()

    # --- 2. 英語の特殊計算設定 (サイドバー) ---
    st.sidebar.header("📢 英語の配点設定")
    raw_re = st.sidebar.number_input("リーディング素点 (100)", 0, 100, 0)
    raw_li = st.sidebar.number_input("リスニング素点 (100)", 0, 100, 0)
    
    st.sidebar.subheader("比率設定")
    r_ratio = st.sidebar.slider("リーディングの比率", 0, 100, 50, step=5)
    l_ratio = 100 - r_ratio
    st.sidebar.write(f"比率 R {r_ratio} : L {l_ratio}")
    
    # 英語の「共通テストベース(200点満点)」での持ち点
    base_eigo = (raw_re * r_ratio + raw_li * l_ratio) / 50 

    # --- 3. 傾斜配点の設定セクション ---
    st.header("2. 大学の配点（満点）を設定")
    st.info("使わない科目の満点は「0」にしてください")

    w_col1, w_col2, w_col3 = st.columns(3)

    with w_col1:
        w_eigo = st.number_input("英語の満点", 0, 400, 200)
        w_kokugo = st.number_input("国語の満点", 0, 400, 200)
        w_joho = st.number_input("情報の満点", 0, 400, 100)

    with w_col2:
        # 数学をまとめて計算
        w_math_total = st.number_input("数学（2科目合計）の満点", 0, 400, 200)
        # 理科をまとめて計算
        w_sci_total = st.number_input("理科（2科目合計）の満点", 0, 400, 200)

    with w_col3:
        # 社会をまとめて計算
        w_soc_total = st.number_input("社会（2科目合計）の満点", 0, 400, 200)

    # --- 4. 計算ロジック ---
    # 英語
    calc_eigo = (base_eigo / 200) * w_eigo
    # 国語・情報
    calc_kokugo = (raw_kokugo / 200) * w_kokugo
    calc_joho = (raw_joho / 100) * w_joho
    # 数学（200点満点を大学配点に換算）
    calc_math = ((raw_math1a + raw_math2bc) / 200) * w_math_total
    # 理科
    calc_sci = ((raw_sci1 + raw_sci2) / 200) * w_sci_total
    # 社会
    calc_soc = ((raw_soc1 + raw_soc2) / 200) * w_soc_total

    total_score = calc_eigo + calc_kokugo + calc_joho + calc_math + calc_sci + calc_soc
    max_total = w_eigo + w_kokugo + w_joho + w_math_total + w_sci_total + w_soc_total

    # --- 5. 結果表示 ---
    st.divider()
    st.header("📊 計算結果")
    
    res_left, res_right = st.columns([1, 1])

    with res_left:
        st.metric(label="合計得点", value=f"{total_score:.1f} / {max_total}")
        if max_total > 0:
            percent = (total_score / max_total) * 100
            st.subheader(f"得点率: {percent:.2f}%")
            st.progress(percent / 100)

    with res_right:
        # 内訳の表示
        st.write("📌 科目別換算点")
        breakdown = {
            "英語": f"{calc_eigo:.1f} / {w_eigo}",
            "国語": f"{calc_kokugo:.1f} / {w_kokugo}",
            "数学(合計)": f"{calc_math:.1f} / {w_math_total}",
            "理科(合計)": f"{calc_sci:.1f} / {w_sci_total}",
            "社会(合計)": f"{calc_soc:.1f} / {w_soc_total}",
            "情報": f"{calc_joho:.1f} / {w_joho}",
        }
        st.json(breakdown)

if __name__ == "__main__":
    main()
