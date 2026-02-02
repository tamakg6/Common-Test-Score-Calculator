import streamlit as st
import pandas as pd

def main():
    st.set_page_config(page_title="共テ配点シミュレーターPro", layout="wide")
    st.title("🎓 共通テスト 傾斜配点シミュレーター")

    # --- 1. 素点（自己採点）入力 ---
    st.header("1. 素点を入力")
    col_k, col_e, col_m, col_s, col_g, col_j = st.columns(6)
    
    with col_k:
        st.subheader("国語")
        raw_kokugo = st.number_input("国語 (200)", 0, 200, 0, key="raw_k")
    with col_e:
        st.subheader("英語")
        raw_re = st.number_input("R (100)", 0, 100, 0, key="raw_re")
        raw_li = st.number_input("L (100)", 0, 100, 0, key="raw_li")
    with col_m:
        st.subheader("数学")
        raw_m1a = st.number_input("ⅠA (100)", 0, 100, 0, key="raw_m1")
        raw_m2bc = st.number_input("ⅡBC (100)", 0, 100, 0, key="raw_m2")
    with col_s:
        st.subheader("理科")
        raw_sci1 = st.number_input("理科① (100)", 0, 100, 0, key="raw_s1")
        raw_sci2 = st.number_input("理科② (100)", 0, 100, 0, key="raw_s2")
    with col_g:
        st.subheader("地歴公民")
        raw_geo1 = st.number_input("1科目目 (100)", 0, 100, 0, key="raw_g1")
        raw_geo2 = st.number_input("2科目目 (100)", 0, 100, 0, key="raw_g2")
    with col_j:
        st.subheader("情報")
        raw_joho = st.number_input("情報Ⅰ (100)", 0, 100, 0, key="raw_j1")

    st.divider()

    # --- 2. 大学別設定 ---
    st.header("2. 志望校の設定")
    set_col1, set_col2 = st.columns([1, 2])
    
    with set_col1:
        st.markdown("### 🔍 英語の比率設定")
        
        # 【修正点】文字列で定義してマッピングする（これでエラー回避）
        ratio_map = {
            "Rのみ (100:0)": (100, 0),
            "4:1 (80:20)": (80, 20),
            "3:1 (75:25)": (75, 25),
            "7:3 (70:30)": (70, 30),
            "3:2 (60:40)": (60, 40),
            "1:1 (50:50)": (50, 50)
        }
        
        selected_label = st.select_slider(
            "リーディング : リスニング",
            options=list(ratio_map.keys()), # 選択肢は文字列のリスト
            value="1:1 (50:50)"           # 初期値も文字列で指定
        )
        
        # 選択された文字列から数値（例: 50, 50）を取り出す
        r_val, l_val = ratio_map[selected_label]
        
        st.markdown("### 🔗 合算設定")
        is_math_sum = st.checkbox("数学を2科目合算する", value=True)
        is_sci_sum = st.checkbox("理科を2科目合算する", value=True)
        is_geo_sum = st.checkbox("地歴公民を2科目合算する", value=True)

    with set_col2:
        st.markdown("### ⚙️ 換算後の満点")
        w_col1, w_col2, w_col3 = st.columns(3)
        with w_col1:
            w_eigo = st.number_input("英語の満点", 0, 400, 200)
            w_kokugo = st.number_input("国語の満点", 0, 400, 200)
        with w_col2:
            w_math = st.number_input("数学の満点", 0, 400, 200)
            w_sci = st.number_input("理科の満点", 0, 400, 200)
        with w_col3:
            w_geo = st.number_input("地歴公民の満点", 0, 400, 200)
            w_joho = st.number_input("情報の満点", 0, 200, 100)

    # --- 3. 計算 ---
    # 英語計算ロジック
    # (R素点 * R比率 + L素点 * L比率) / 100 で「共通テストとしての得点率」を出し、大学満点を掛ける
    eigo_score_base = (raw_re * r_val + raw_li * l_val) / 100
    calc_eigo = (eigo_score_base / 100) * w_eigo
    
    calc_kokugo = (raw_kokugo / 200) * w_kokugo
    calc_joho = (raw_joho / 100) * w_joho

    # 合算計算関数
    def calc_weighted(raw1, raw2, is_sum, weight):
        if weight <= 0: return 0.0
        # 合算なら単純足し算、そうでなければ1科目目のみ使用
        score = (raw1 + raw2) if
