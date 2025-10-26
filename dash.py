import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
import warnings

warnings.filterwarnings('ignore')

# تنظیمات فونت فارسی برای matplotlib
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# -------------------------------------------------
# 0. تنظیمات صفحه
# -------------------------------------------------
st.set_page_config(
    page_title="داشبورد ارزیابی هلدینگ مالی",
    page_icon="📊",
    layout="wide"
)

st.title("📊 داشبورد ارزیابی عملکرد و بهره‌وری هلدینگ مالی")
st.caption("مدل تمرکز: سودآوری و بهره‌وری عملیاتی")

# -------------------------------------------------
# 1. داده اولیه
# -------------------------------------------------

default_data = [
    {
        "شرکت": "سبدگردان الف",
        "ROE": 18,
        "ROI": 15,
        "EVA": 12,
        "رشد سود خالص": 10,
        "نسبت سود به درآمد": 25,
        "Cost/Income": 45,
        "درآمد به ازای کارمند": 200,
        "AUM/تحلیلگر": 30,
        "زمان تصمیم سرمایه‌گذاری": 5,
        "رشد AUM": 12,
        "نوآوری مالی": 3,
        "درآمد پایدار": 70,
        "رضایت مشتری (NPS)": 85,
        "Compliance": 90,
        "Debt/Equity": 0.5,
        "کنترل داخلی": 85,
        "شفافیت گزارش": 90,
        "هم‌افزایی": 60,
        "پروژه‌های مشترک": 2,
        "سهم بازار": 5,
    },
    {
        "شرکت": "کارگزاری ب",
        "ROE": 20,
        "ROI": 18,
        "EVA": 14,
        "رشد سود خالص": 12,
        "نسبت سود به درآمد": 28,
        "Cost/Income": 40,
        "درآمد به ازای کارمند": 250,
        "AUM/تحلیلگر": 35,
        "زمان تصمیم سرمایه‌گذاری": 4,
        "رشد AUM": 10,
        "نوآوری مالی": 5,
        "درآمد پایدار": 65,
        "رضایت مشتری (NPS)": 90,
        "Compliance": 88,
        "Debt/Equity": 0.6,
        "کنترل داخلی": 80,
        "شفافیت گزارش": 88,
        "هم‌افزایی": 55,
        "پروژه‌های مشترک": 3,
        "سهم بازار": 6,
    },
    {
        "شرکت": "مدیریت دارایی ج",
        "ROE": 15,
        "ROI": 12,
        "EVA": 10,
        "رشد سود خالص": 8,
        "نسبت سود به درآمد": 22,
        "Cost/Income": 50,
        "درآمد به ازای کارمند": 180,
        "AUM/تحلیلگر": 28,
        "زمان تصمیم سرمایه‌گذاری": 6,
        "رشد AUM": 14,
        "نوآوری مالی": 2,
        "درآمد پایدار": 60,
        "رضایت مشتری (NPS)": 80,
        "Compliance": 85,
        "Debt/Equity": 0.7,
        "کنترل داخلی": 82,
        "شفافیت گزارش": 85,
        "هم‌افزایی": 70,
        "پروژه‌های مشترک": 2,
        "سهم بازار": 4,
    },
    {
        "شرکت": "تأمین سرمایه د",
        "ROE": 22,
        "ROI": 20,
        "EVA": 16,
        "رشد سود خالص": 15,
        "نسبت سود به درآمد": 30,
        "Cost/Income": 38,
        "درآمد به ازای کارمند": 300,
        "AUM/تحلیلگر": 40,
        "زمان تصمیم سرمایه‌گذاری": 3,
        "رشد AUM": 18,
        "نوآوری مالی": 6,
        "درآمد پایدار": 75,
        "رضایت مشتری (NPS)": 92,
        "Compliance": 90,
        "Debt/Equity": 0.4,
        "کنترل داخلی": 90,
        "شفافیت گزارش": 92,
        "هم‌افزایی": 65,
        "پروژه‌های مشترک": 4,
        "سهم بازار": 8,
    },
]

raw_df = pd.DataFrame(default_data)

st.sidebar.header("تنظیمات ورودی 📥")
st.sidebar.write("اگر می‌خوای داده واقعی وارد کنی، می‌تونی از این جدول ادیت‌پذیر استفاده کنی:")

edited_df = st.sidebar.data_editor(raw_df, num_rows="dynamic", key="editor_table")

st.sidebar.info("پس از تغییر جدول سمت چپ، داشبورد پایین بر اساس همین داده محاسبه می‌شود.")

# -------------------------------------------------
# تنظیمات وزن‌ها
# -------------------------------------------------
st.sidebar.divider()
st.sidebar.subheader("⚖️ تنظیم وزن محورها")
st.sidebar.caption("مجموع وزن‌ها باید 100% باشد")

weight_financial = st.sidebar.slider("وزن مالی (%)", 0, 100, 40)
weight_efficiency = st.sidebar.slider("وزن بهره‌وری (%)", 0, 100, 30)
weight_growth = st.sidebar.slider("وزن رشد پایدار (%)", 0, 100, 15)
weight_risk = st.sidebar.slider("وزن ریسک و حاکمیت (%)", 0, 100, 10)
weight_synergy = st.sidebar.slider("وزن هم‌افزایی (%)", 0, 100, 5)

total_weight = weight_financial + weight_efficiency + weight_growth + weight_risk + weight_synergy
if total_weight != 100:
    st.sidebar.warning(f"⚠️ مجموع وزن‌ها {total_weight}% است. لطفاً آن را به 100% تنظیم کنید.")

# -------------------------------------------------
# 2. توابع محاسبه KPI محوری
# -------------------------------------------------

def محور_مالی(row):
    return (
        row["ROE"]
        + row["ROI"]
        + row["EVA"]
        + row["رشد سود خالص"]
        + row["نسبت سود به درآمد"]
    ) / 5.0


def محور_بهره_وری(row):
    return (
        (100 - row["Cost/Income"]) +
        (row["درآمد به ازای کارمند"] / 3) +
        row["AUM/تحلیلگر"] +
        ((10 - row["زمان تصمیم سرمایه‌گذاری"]) * 10)
    ) / 4.0


def محور_رشد_پایدار(row):
    return (
        row["رشد AUM"] +
        row["نوآوری مالی"] * 10 +
        row["درآمد پایدار"] +
        row["رضایت مشتری (NPS)"]
    ) / 4.0


def محور_ریسک_و_حاکمیت(row):
    سلامت_اهرم = (1 - min(row["Debt/Equity"] / 2, 1)) * 100
    return (
        row["Compliance"] +
        سلامت_اهرم +
        row["کنترل داخلی"] +
        row["شفافیت گزارش"]
    ) / 4.0


def محور_هم_افزایی(row):
    return (
        row["هم‌افزایی"] +
        row["پروژه‌های مشترک"] * 15 +
        row["سهم بازار"] * 10
    ) / 3.0


def محاسبه_امتیازها(df, w_fin, w_eff, w_grow, w_risk, w_syn):
    df = df.copy()

    df["امتیاز مالی"] = df.apply(محور_مالی, axis=1)
    df["امتیاز بهره‌وری"] = df.apply(محور_بهره_وری, axis=1)
    df["امتیاز رشد پایدار"] = df.apply(محور_رشد_پایدار, axis=1)
    df["امتیاز ریسک و حاکمیت"] = df.apply(محور_ریسک_و_حاکمیت, axis=1)
    df["امتیاز هم‌افزایی"] = df.apply(محور_هم_افزایی, axis=1)

    df["امتیاز کل"] = (
        (w_fin/100) * df["امتیاز مالی"] +
        (w_eff/100) * df["امتیاز بهره‌وری"] +
        (w_grow/100) * df["امتیاز رشد پایدار"] +
        (w_risk/100) * df["امتیاز ریسک و حاکمیت"] +
        (w_syn/100) * df["امتیاز هم‌افزایی"]
    )

    df["رتبه"] = df["امتیاز کل"].rank(ascending=False, method="min").astype(int)
    return df


scored_df = محاسبه_امتیازها(edited_df, weight_financial, weight_efficiency, weight_growth, weight_risk, weight_synergy)

# -------------------------------------------------
# 3. خلاصه مدیریتی بالا
# -------------------------------------------------
st.subheader("📈 خلاصه عملکرد مدیریت (Consolidated View)")

col1, col2, col3, col4 = st.columns(4)

top_company_row = scored_df.loc[scored_df["امتیاز کل"].idxmax()]
worst_cost_row = scored_df.loc[scored_df["Cost/Income"].idxmax()]
best_eff_row = scored_df.loc[scored_df["امتیاز بهره‌وری"].idxmax()]
best_fin_row = scored_df.loc[scored_df["امتیاز مالی"].idxmax()]

col1.metric(
    "بهترین شرکت از نظر امتیاز کل",
    f"{top_company_row['شرکت']}",
    f"امتیاز: {round(top_company_row['امتیاز کل'],1)}"
)

col2.metric(
    "بالاترین هزینه/درآمد (نیاز به اصلاح)",
    f"{worst_cost_row['شرکت']}",
    f"{round(worst_cost_row['Cost/Income'],1)}%",
    delta_color="inverse"
)

col3.metric(
    "بهره‌ورترین شرکت",
    f"{best_eff_row['شرکت']}",
    f"امتیاز: {round(best_eff_row['امتیاز بهره‌وری'],1)}"
)

col4.metric(
    "قوی‌ترین وضعیت مالی",
    f"{best_fin_row['شرکت']}",
    f"امتیاز: {round(best_fin_row['امتیاز مالی'],1)}"
)

st.divider()

# -------------------------------------------------
# 4. جدول امتیاز نهایی و رتبه
# -------------------------------------------------
st.subheader("🏆 رتبه و امتیاز کل شرکت‌ها")

display_cols = [
    "رتبه",
    "شرکت",
    "امتیاز مالی",
    "امتیاز بهره‌وری",
    "امتیاز رشد پایدار",
    "امتیاز ریسک و حاکمیت",
    "امتیاز هم‌افزایی",
    "امتیاز کل",
]

styled_df = scored_df[display_cols].sort_values("رتبه").copy()
styled_df = styled_df.round(2)

st.dataframe(
    styled_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# -------------------------------------------------
# 5. نمودارهای مقایسه‌ای
# -------------------------------------------------
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📊 امتیاز کل شرکت‌ها")
    
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    bars = ax1.barh(scored_df["شرکت"], scored_df["امتیاز کل"], color=colors[:len(scored_df)])
    ax1.set_xlabel("Total Score")
    ax1.set_title("Company Total Score Comparison")
    ax1.grid(axis='x', alpha=0.3)
    
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax1.text(width, bar.get_y() + bar.get_height()/2, 
                f'{width:.1f}', ha='left', va='center', fontsize=9)
    
    plt.tight_layout()
    st.pyplot(fig1)

with col_chart2:
    st.subheader("💰 شاخص‌های مالی کلیدی")
    
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    x = np.arange(len(scored_df["شرکت"]))
    width = 0.25
    
    ax2.bar(x - width, scored_df["ROE"], width, label='ROE', alpha=0.8)
    ax2.bar(x, scored_df["ROI"], width, label='ROI', alpha=0.8)
    ax2.bar(x + width, scored_df["EVA"], width, label='EVA', alpha=0.8)
    
    ax2.set_ylabel('Value')
    ax2.set_title('Key Financial Metrics')
    ax2.set_xticks(x)
    ax2.set_xticklabels(scored_df["شرکت"], rotation=20, ha='right')
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig2)

st.divider()

# -------------------------------------------------
# 6. نمودار رادار (Spider Chart)
# -------------------------------------------------
st.subheader("🕸️ نمودار مقایسه چندبعدی محورها (Radar Chart)")

metric_cols = [
    "امتیاز مالی",
    "امتیاز بهره‌وری",
    "امتیاز رشد پایدار",
    "امتیاز ریسک و حاکمیت",
    "امتیاز هم‌افزایی",
]

fig3, ax3 = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))

angles = np.linspace(0, 2 * np.pi, len(metric_cols), endpoint=False).tolist()
angles += angles[:1]

colors_radar = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']

for idx, row in scored_df.iterrows():
    values = [row[col] for col in metric_cols]
    values += values[:1]
    ax3.plot(angles, values, 'o-', linewidth=2, label=row["شرکت"], color=colors_radar[idx % len(colors_radar)])
    ax3.fill(angles, values, alpha=0.15, color=colors_radar[idx % len(colors_radar)])

ax3.set_xticks(angles[:-1])
ax3.set_xticklabels(['Financial', 'Efficiency', 'Growth', 'Risk Gov', 'Synergy'], fontsize=10)
ax3.set_ylim(0, max(scored_df[metric_cols].max()) * 1.1)
ax3.set_title("Multi-dimensional Performance Comparison", size=14, pad=20)
ax3.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
ax3.grid(True)

plt.tight_layout()
st.pyplot(fig3)

st.divider()

# -------------------------------------------------
# 7. نمودار مقایسه محورها (Grouped Bar)
# -------------------------------------------------
st.subheader("📊 مقایسه تفصیلی محورها بین شرکت‌ها")

fig4, ax4 = plt.subplots(figsize=(12, 6))
x = np.arange(len(scored_df["شرکت"]))
width = 0.15

for i, col in enumerate(metric_cols):
    ax4.bar(
        x + i*width - (len(metric_cols)*width/2 - width/2),
        scored_df[col],
        width=width,
        label=col.replace("امتیاز ", "")
    )

ax4.set_xticks(x)
ax4.set_xticklabels(scored_df["شرکت"], rotation=15, ha='right')
ax4.set_ylabel('Score')
ax4.set_title('Detailed Axis Comparison Between Companies')
ax4.legend(loc="best", fontsize=9, ncol=2)
ax4.grid(axis='y', alpha=0.3)

plt.tight_layout()
st.pyplot(fig4)

st.divider()

# -------------------------------------------------
# 8. تحلیل هزینه و بهره‌وری
# -------------------------------------------------
st.subheader("💼 تحلیل هزینه و بهره‌وری")

col_eff1, col_eff2 = st.columns(2)

with col_eff1:
    st.subheader("هزینه/درآمد (Cost to Income)")
    fig5, ax5 = plt.subplots(figsize=(8, 5))
    bars = ax5.barh(scored_df["شرکت"], scored_df["Cost/Income"], 
                    color=['green' if x < 45 else 'orange' if x < 50 else 'red' 
                           for x in scored_df["Cost/Income"]])
    ax5.set_xlabel('Cost/Income (%)')
    ax5.set_title('Cost Efficiency (Lower is Better)')
    ax5.axvline(x=45, color='green', linestyle='--', alpha=0.5, label='Excellent (<45%)')
    ax5.axvline(x=50, color='orange', linestyle='--', alpha=0.5, label='Warning (>50%)')
    ax5.legend()
    ax5.grid(axis='x', alpha=0.3)
    
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax5.text(width, bar.get_y() + bar.get_height()/2, 
                f'{width:.1f}%', ha='left', va='center', fontsize=9)
    
    plt.tight_layout()
    st.pyplot(fig5)

with col_eff2:
    st.subheader("درآمد به ازای کارمند")
    fig6, ax6 = plt.subplots(figsize=(8, 5))
    bars = ax6.barh(scored_df["شرکت"], scored_df["درآمد به ازای کارمند"], color='#2ecc71')
    ax6.set_xlabel('Revenue per Employee')
    ax6.set_title('Employee Productivity')
    ax6.grid(axis='x', alpha=0.3)
    
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax6.text(width, bar.get_y() + bar.get_height()/2, 
                f'{int(width)}', ha='left', va='center', fontsize=9)
    
    plt.tight_layout()
    st.pyplot(fig6)

st.divider()

# -------------------------------------------------
# 9. تحلیل ریسک
# -------------------------------------------------
st.subheader("⚠️ تحلیل ریسک و حاکمیت")

col_risk1, col_risk2 = st.columns(2)

with col_risk1:
    st.subheader("نسبت بدهی به حقوق صاحبان سهام")
    fig7, ax7 = plt.subplots(figsize=(8, 5))
    colors_debt = ['green' if x < 0.5 else 'orange' if x < 0.7 else 'red' 
                   for x in scored_df["Debt/Equity"]]
    bars = ax7.barh(scored_df["شرکت"], scored_df["Debt/Equity"], color=colors_debt)
    ax7.set_xlabel('Debt/Equity Ratio')
    ax7.set_title('Leverage Risk Assessment')
    ax7.axvline(x=0.5, color='green', linestyle='--', alpha=0.5, label='Safe (<0.5)')
    ax7.axvline(x=0.7, color='red', linestyle='--', alpha=0.5, label='Risky (>0.7)')
    ax7.legend()
    ax7.grid(axis='x', alpha=0.3)
    
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax7.text(width, bar.get_y() + bar.get_height()/2, 
                f'{width:.2f}', ha='left', va='center', fontsize=9)
    
    plt.tight_layout()
    st.pyplot(fig7)

with col_risk2:
    st.subheader("Compliance و کنترل داخلی")
    fig8, ax8 = plt.subplots(figsize=(8, 5))
    x = np.arange(len(scored_df["شرکت"]))
    width = 0.35
    
    ax8.bar(x - width/2, scored_df["Compliance"], width, label='Compliance', alpha=0.8)
    ax8.bar(x + width/2, scored_df["کنترل داخلی"], width, label='Internal Control', alpha=0.8)
    
    ax8.set_ylabel('Score')
    ax8.set_title('Governance Quality')
    ax8.set_xticks(x)
    ax8.set_xticklabels(scored_df["شرکت"], rotation=20, ha='right')
    ax8.legend()
    ax8.grid(axis='y', alpha=0.3)
    ax8.set_ylim(0, 100)
    
    plt.tight_layout()
    st.pyplot(fig8)

st.divider()

# -------------------------------------------------
# 10. جزئیات یک شرکت انتخابی (Drilldown)
# -------------------------------------------------
st.subheader("🔍 تحلیل Drilldown یک شرکت")

selected_company = st.selectbox(
    "شرکت مورد بررسی:",
    scored_df["شرکت"].tolist()
)

row = scored_df[scored_df["شرکت"] == selected_company].iloc[0]

# نمایش امتیازها
st.markdown(f"### 🏅 امتیازهای {selected_company}")
col_score1, col_score2, col_score3, col_score4, col_score5 = st.columns(5)
col_score1.metric("امتیاز مالی", f"{round(row['امتیاز مالی'], 1)}")
col_score2.metric("امتیاز بهره‌وری", f"{round(row['امتیاز بهره‌وری'], 1)}")
col_score3.metric("امتیاز رشد", f"{round(row['امتیاز رشد پایدار'], 1)}")
col_score4.metric("امتیاز ریسک", f"{round(row['امتیاز ریسک و حاکمیت'], 1)}")
col_score5.metric("امتیاز کل", f"{round(row['امتیاز کل'], 1)}", delta=f"رتبه {int(row['رتبه'])}")

st.markdown(f"### 📊 شاخص‌های کلیدی {selected_company}")
col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5, col_kpi6 = st.columns(6)
col_kpi1.metric("ROE", f"{row['ROE']}%")
col_kpi2.metric("ROI", f"{row['ROI']}%")
col_kpi3.metric("EVA", f"{row['EVA']}")
col_kpi4.metric("Cost/Income", f"{row['Cost/Income']}%")
col_kpi5.metric("D/E Ratio", f"{row['Debt/Equity']}")
col_kpi6.metric("NPS", f"{row['رضایت مشتری (NPS)']}")

# جدول جزئیات کامل
st.markdown(f"### 📋 جزئیات کامل شاخص‌های {selected_company}")
company_detail = edited_df[edited_df["شرکت"] == selected_company].T
company_detail.columns = ['مقدار']
st.dataframe(company_detail, use_container_width=True)

# توصیه‌های بهبود
st.markdown(f"### 💡 توصیه‌های بهبود برای {selected_company}")

recommendations = []

if row["Cost/Income"] > 45:
    recommendations.append("🔴 نسبت هزینه به درآمد بالاست. کاهش هزینه‌های عملیاتی توصیه می‌شود.")
if row["Debt/Equity"] > 0.6:
    recommendations.append("🔴 نسبت بدهی به حقوق صاحبان سهام بالاست. کاهش اهرم مالی ضروری است.")
if row["رضایت مشتری (NPS)"] < 85:
    recommendations.append("🟡 رضایت مشتری قابل بهبود است. تمرکز بر کیفیت خدمات توصیه می‌شود.")
if row["نوآوری مالی"] < 4:
    recommendations.append("🟡 سرمایه‌گذاری بیشتر در نوآوری و فناوری پیشنهاد می‌شود.")
if row["ROE"] > 20:
    recommendations.append("🟢 عملکرد مالی عالی! حفظ این روند ضروری است.")
if row["امتیاز بهره‌وری"] > 80:
    recommendations.append("🟢 بهره‌وری بالا! این مزیت رقابتی را حفظ کنید.")

if recommendations:
    for rec in recommendations:
        st.write(rec)
else:
    st.success("✅ عملکرد شرکت در سطح مطلوبی است.")

st.divider()

# -------------------------------------------------
# 11. خلاصه نهایی و توصیه‌های کلی
# -------------------------------------------------
st.subheader("📝 خلاصه تحلیل و توصیه‌های کلی هلدینگ")

col_summary1, col_summary2 = st.columns(2)

with col_summary1:
    st.markdown("#### نقاط قوت هلدینگ")
    avg_financial = scored_df["امتیاز مالی"].mean()
    avg_efficiency = scored_df["امتیاز بهره‌وری"].mean()
    avg_nps = scored_df["رضایت مشتری (NPS)"].mean()
    
    st.write(f"✅ **میانگین امتیاز مالی:** {avg_financial:.1f}")
    st.write(f"✅ **میانگین بهره‌وری:** {avg_efficiency:.1f}")
    st.write(f"✅ **میانگین رضایت مشتری:** {avg_nps:.1f}")
    
    if avg_financial > 18:
        st.success("سودآوری کلی هلدینگ در سطح عالی است")
    if avg_efficiency > 75:
        st.success("بهره‌وری عملیاتی در سطح مطلوب است")
    if avg_nps > 85:
        st.success("رضایت مشتریان در سطح بالایی است")

with col_summary2:
    st.markdown("#### نقاط نیازمند بهبود")
    avg_cost_income = scored_df["Cost/Income"].mean()
    avg_debt = scored_df["Debt/Equity"].mean()
    avg_innovation = scored_df["نوآوری مالی"].mean()
    
    st.write(f"⚠️ **میانگین Cost/Income:** {avg_cost_income:.1f}%")
    st.write(f"⚠️ **میانگین D/E Ratio:** {avg_debt:.2f}")
    st.write(f"⚠️ **میانگین نوآوری:** {avg_innovation:.1f}/10")
    
    if avg_cost_income > 45:
        st.warning("بهینه‌سازی هزینه‌های عملیاتی در سطح هلدینگ ضروری است")
    if avg_debt > 0.6:
        st.warning("کاهش اهرم مالی در برخی شرکت‌ها توصیه می‌شود")
    if avg_innovation < 4:
        st.warning("سرمایه‌گذاری بیشتر در نوآوری و دیجیتال ضروری است")

st.divider()

# -------------------------------------------------
# 12. ماتریس عملکرد (Performance Matrix)
# -------------------------------------------------
st.subheader("🎯 ماتریس عملکرد: سودآوری vs بهره‌وری")

fig9, ax9 = plt.subplots(figsize=(10, 7))

# رسم نقاط
for idx, row in scored_df.iterrows():
    ax9.scatter(row["امتیاز بهره‌وری"], row["امتیاز مالی"], 
               s=row["سهم بازار"]*50, alpha=0.6, 
               label=row["شرکت"])
    ax9.annotate(row["شرکت"], 
                (row["امتیاز بهره‌وری"], row["امتیاز مالی"]),
                xytext=(5, 5), textcoords='offset points', fontsize=9)

# خطوط میانگین
avg_eff = scored_df["امتیاز بهره‌وری"].mean()
avg_fin = scored_df["امتیاز مالی"].mean()

ax9.axhline(y=avg_fin, color='red', linestyle='--', alpha=0.5, label='Avg Financial')
ax9.axvline(x=avg_eff, color='blue', linestyle='--', alpha=0.5, label='Avg Efficiency')

# برچسب‌های چهار ربع
ax9.text(ax9.get_xlim()[1]*0.95, ax9.get_ylim()[1]*0.95, 'Stars', 
        ha='right', va='top', fontsize=12, weight='bold', 
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
ax9.text(ax9.get_xlim()[0]*1.05, ax9.get_ylim()[1]*0.95, 'Cash Cows', 
        ha='left', va='top', fontsize=12, weight='bold',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
ax9.text(ax9.get_xlim()[1]*0.95, ax9.get_ylim()[0]*1.05, 'Question Marks', 
        ha='right', va='bottom', fontsize=12, weight='bold',
        bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5))
ax9.text(ax9.get_xlim()[0]*1.05, ax9.get_ylim()[0]*1.05, 'Dogs', 
        ha='left', va='bottom', fontsize=12, weight='bold',
        bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5))

ax9.set_xlabel('Efficiency Score', fontsize=11)
ax9.set_ylabel('Financial Score', fontsize=11)
ax9.set_title('Performance Matrix (Bubble size = Market Share)', fontsize=13)
ax9.grid(True, alpha=0.3)
ax9.legend(loc='upper left', fontsize=9)

plt.tight_layout()
st.pyplot(fig9)

st.info("""
**راهنمای ماتریس:**
- **Stars (ستاره‌ها):** سودآوری و بهره‌وری بالا - حفظ و سرمایه‌گذاری
- **Cash Cows (گاوهای شیرده):** سودآوری بالا، بهره‌وری متوسط - بهینه‌سازی عملیات
- **Question Marks (علامت سوال):** بهره‌وری بالا، سودآوری پایین - بررسی استراتژی
- **Dogs (سگ‌ها):** هر دو پایین - نیاز به بازسازی یا خروج
""")

st.divider()

# -------------------------------------------------
# 13. تحلیل همبستگی
# -------------------------------------------------
st.subheader("🔗 تحلیل همبستگی شاخص‌ها")

correlation_metrics = [
    "ROE", "ROI", "EVA", "Cost/Income", "درآمد به ازای کارمند",
    "رضایت مشتری (NPS)", "Compliance", "Debt/Equity"
]

corr_df = edited_df[correlation_metrics].corr()

fig10, ax10 = plt.subplots(figsize=(10, 8))
im = ax10.imshow(corr_df, cmap='RdYlGn', aspect='auto', vmin=-1, vmax=1)

ax10.set_xticks(np.arange(len(correlation_metrics)))
ax10.set_yticks(np.arange(len(correlation_metrics)))
ax10.set_xticklabels(correlation_metrics, rotation=45, ha='right', fontsize=9)
ax10.set_yticklabels(correlation_metrics, fontsize=9)

# افزودن مقادیر
for i in range(len(correlation_metrics)):
    for j in range(len(correlation_metrics)):
        text = ax10.text(j, i, f'{corr_df.iloc[i, j]:.2f}',
                        ha="center", va="center", color="black", fontsize=8)

ax10.set_title("Correlation Matrix of Key Metrics", fontsize=13, pad=20)
plt.colorbar(im, ax=ax10)
plt.tight_layout()
st.pyplot(fig10)

st.divider()

# -------------------------------------------------
# 14. مقایسه با بنچمارک
# -------------------------------------------------
st.subheader("📏 مقایسه با بنچمارک صنعت")

benchmark_data = {
    "ROE": 18,
    "ROI": 15,
    "Cost/Income": 42,
    "رضایت مشتری (NPS)": 85,
    "Compliance": 88,
    "Debt/Equity": 0.55
}

st.write("**بنچمارک‌های استاندارد صنعت مالی:**")

col_bench1, col_bench2, col_bench3 = st.columns(3)

for idx, (key, benchmark_value) in enumerate(benchmark_data.items()):
    avg_value = scored_df[key].mean()
    
    if idx % 3 == 0:
        col = col_bench1
    elif idx % 3 == 1:
        col = col_bench2
    else:
        col = col_bench3
    
    # محاسبه انحراف از بنچمارک
    if key in ["Cost/Income", "Debt/Equity"]:
        # برای این‌ها کمتر بودن بهتر است
        deviation = benchmark_value - avg_value
        status = "✅" if deviation >= 0 else "⚠️"
    else:
        # برای بقیه بیشتر بودن بهتر است
        deviation = avg_value - benchmark_value
        status = "✅" if deviation >= 0 else "⚠️"
    
    col.metric(
        label=key,
        value=f"{avg_value:.1f}",
        delta=f"{deviation:+.1f} vs benchmark ({benchmark_value})",
        delta_color="normal" if deviation >= 0 else "inverse"
    )

st.divider()

# -------------------------------------------------
# 15. گزارش PDF/Excel Export
# -------------------------------------------------
st.subheader("📥 دانلود داده‌ها")

col_export1, col_export2 = st.columns(2)

with col_export1:
    # تبدیل به CSV
    csv = scored_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📊 دانلود گزارش کامل (CSV)",
        data=csv,
        file_name="financial_holding_report.csv",
        mime="text/csv"
    )

with col_export2:
    # تبدیل به JSON
    json_data = scored_df.to_json(orient='records', force_ascii=False).encode('utf-8')
    st.download_button(
        label="📋 دانلود داده‌ها (JSON)",
        data=json_data,
        file_name="financial_holding_data.json",
        mime="application/json"
    )

st.divider()

# -------------------------------------------------
# 16. Footer و اطلاعات تکمیلی
# -------------------------------------------------
st.markdown("---")
st.markdown("""
### 📌 درباره این داشبورد

این داشبورد یک سیستم جامع ارزیابی عملکرد برای هلدینگ‌های مالی است که شامل:

**محورهای ارزیابی:**
- 💰 **محور مالی:** ROE, ROI, EVA, رشد سود، نسبت سودآوری
- ⚡ **محور بهره‌وری:** Cost/Income، درآمد هر کارمند، AUM/تحلیلگر، سرعت تصمیم‌گیری
- 📈 **محور رشد پایدار:** رشد AUM، نوآوری، درآمد پایدار، رضایت مشتری
- 🛡️ **محور ریسک و حاکمیت:** Compliance، D/E Ratio، کنترل داخلی، شفافیت
- 🤝 **محور هم‌افزایی:** همکاری بین واحدها، پروژه‌های مشترک، سهم بازار

**ویژگی‌های کلیدی:**
- ✅ ورود و ویرایش آسان داده‌ها
- ✅ تنظیم وزن‌های محورها به صورت داینامیک
- ✅ نمودارهای تعاملی و چندبعدی
- ✅ تحلیل Drilldown برای هر شرکت
- ✅ مقایسه با بنچمارک صنعت
- ✅ توصیه‌های هوشمند بهبود
- ✅ امکان دانلود گزارش‌ها

**نحوه استفاده:**
1. داده‌های شرکت‌ها را در سایدبار وارد کنید
2. وزن محورها را مطابق اولویت‌های خود تنظیم کنید
3. نمودارها و تحلیل‌ها را بررسی کنید
4. برای هر شرکت، تحلیل جزئی و توصیه‌ها را مطالعه کنید
5. گزارش نهایی را دانلود کنید

---
*این داشبورد به‌صورت کاملاً آفلاین و on-premise قابل استفاده است.*  
*نسخه 2.0 - آخرین بروزرسانی: 2025*
""")

st.caption("💡 برای سوالات یا پشتیبانی، با تیم توسعه تماس بگیرید.")

# پایان کد
