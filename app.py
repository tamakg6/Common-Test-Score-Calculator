import streamlit as st
import pandas as pd

def main():
    st.set_page_config(page_title="共テ配点シミュレーターPro", layout="wide")
    st.title("🎓 共通テスト 傾斜配点シミュレーター")
    st.write("素点を入力し、大学ごとの合算ルールと配点を設定してください。")

    # --- 1. 素点入力セクション ---
    st.header("1. 素点（自己採点）を入力")
    
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

    # --- 2. 大学別配点設定セクション ---
    st.header("2. 志望校の配点・比率を設定")
    
    set_col1, set_col2 = st.columns([1, 2])
    
    with set_col1:
        st.markdown("### 🔍 英語の比率設定")
        r_ratio = st.select_slider(
            "リーディング : リスニング の比率",
            options=[(100, 0), (80, 20), (75, 25), (70, 30), (60, 40), (50, 50)],
            value=(50, 50),
            format_func=lambda x: f"{x[0]} : {x[1]}",
            key="ratio_slider"
        )
        
        st.markdown("### 🔗 合算設定")
        is_math_sum = st.checkbox("数学を2科目合算する", value=True)
        is_sci_sum = st.checkbox("理科を2科目合算する", value=True)
        is_geo_sum = st.checkbox("地歴公民を2科目合算する", value=True)
        st.caption("チェックを外すと、1科目目のみが換算対象になります。")

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

    # --- 3. 計算ロジック ---
    # 英語
    eigo_base = (raw_re * r_ratio[0] + raw_li * r_ratio[1]) / 50
    calc_eigo = (eigo_base / 200) * w_eigo
    
    # 国語・情報
    calc_kokugo = (raw_kokugo / 200) * w_kokugo
    calc_joho = (raw_joho / 100) * w_joho

    # 合算or単独の判定と計算
    def calc_weighted(raw1, raw2, is_sum, weight):
        base_score = (raw1 + raw2) if is_sum else raw1
        max_raw = 200 if is_sum else 100
        return (base_score / max_raw) * weight if weight > 0 else 0

    calc_math = calc_weighted(raw_m1a, raw_m2bc, is_math_sum, w_math)
    calc_sci = calc_weighted(raw_sci1, raw_sci2, is_sci_sum, w_sci)
    calc_geo = calc_weighted(raw_geo1, raw_geo2, is_geo_sum, w_geo)

    total_score = calc_eigo + calc_kokugo + calc_math + calc_sci + calc_geo + calc_joho
    max_total = w_eigo + w_kokugo + w_math + w_sci + w_geo + w_joho

    # --- 4. 結果表示 ---
    st.divider()
    st.header("📊 計算結果")
    
    res_c1, res_c2 = st.columns([1, 2])
    
    with res_c1:
        st.metric(label="合計得点", value=f"{total_score:.1f} / {max_total}")
        if max_total > 0:
            percent = (total_score / max_total) * 100
            st.write(f"## 得点率: {percent:.2f}%")
            st.progress(percent / 100)
        
        # 記録保存ボタン
        if st.button("💾 結果を記録する"):
            record = {
                "合計": f"{total_score:.1f}",
                "率": f"{percent:.1f}%",
                "英": f"{calc_eigo:.1f}",
                "数": f"{calc_math:.1f}",
                "理": f"{calc_sci:.1f}",
                "社": f"{calc_geo:.1f}"
            }
            st.success("結果を記録しました（セッション中のみ保持）")
            st.write(record)

    with res_c2:
        # 結果の表
        results_list = [
            ["英語", f"{raw_re + raw_li}", f"{calc_eigo:.1f}", w_eigo],
            ["国語", f"{raw_kokugo}", f"{calc_kokugo:.1f}", w_kokugo],
            ["数学", f"{raw_m1a + raw_m2bc if is_math_sum else raw_m1a}", f"{calc_math:.1f}", w_math],
            ["理科", f"{raw_sci1 + raw_sci2 if is_sci_sum else raw_sci1}", f"{calc_sci:.1f}", w_sci],
            ["地歴公民", f"{raw_geo1 + raw_geo2 if is_geo_sum else raw_geo1}", f"{calc_geo:.1f}", w_geo],
            ["情報", f"{raw_joho}", f"{calc_joho:.1f}", w_joho],
        ]
        df = pd.DataFrame(results_list, columns=["科目", "計算対象素点", "換算点", "満点設定"])
        st.table(df)

if __name__ == "__main__":
    main()
