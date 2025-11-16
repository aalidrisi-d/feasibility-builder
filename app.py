# Feasibility Builder – Powered by The Three Group (2025)

import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime
import requests

# بيانات بوت التليجرام
TELEGRAM_BOT_TOKEN = "8356517277:AAHaqq_-5oUZlWkC7X5G_MXVRcv1HjcdpXQ"
TELEGRAM_CHAT_ID = "8336591767"

def send_telegram_message(message):
    print("Telegram message was sent:")
    print(message)  # ← لاحظ أنك استخدمت telegram_msg بالخطأ، والصحيح هو message
    url = "https://api.telegram.org/bot8356517277:AAHaqq_-5oUZlWkC7X5G_MXVRcv1HjcdpXQ/sendMessage"
    payload = {
        "chat_id": "8336591767",
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        print("Telegram API Response:", response.text)  # طباعة النتيجة
        response.raise_for_status()
    except Exception as e:
        print(f"Telegram Error: {e}")

# القطاعات وتفاصيلها
sectors = {
    "Tech": {"avg_margin": 0.45, "avg_roi": 0.22, "fixed_costs": 120000, "variable_cost_pct": 0.35},
    "Health": {"avg_margin": 0.5, "avg_roi": 0.27, "fixed_costs": 150000, "variable_cost_pct": 0.30},
    "Fitness": {"avg_margin": 0.4, "avg_roi": 0.18, "fixed_costs": 100000, "variable_cost_pct": 0.4},
    "Hospitality": {"avg_margin": 0.35, "avg_roi": 0.2, "fixed_costs": 130000, "variable_cost_pct": 0.45},
    "Tourism": {"avg_margin": 0.42, "avg_roi": 0.25, "fixed_costs": 125000, "variable_cost_pct": 0.38},
    "Restaurants": {"avg_margin": 0.28, "avg_roi": 0.15, "fixed_costs": 80000, "variable_cost_pct": 0.55},
    "Cafes": {"avg_margin": 0.32, "avg_roi": 0.18, "fixed_costs": 90000, "variable_cost_pct": 0.5},
    "Finance": {"avg_margin": 0.48, "avg_roi": 0.3, "fixed_costs": 200000, "variable_cost_pct": 0.25},
    "Fashion": {"avg_margin": 0.38, "avg_roi": 0.2, "fixed_costs": 95000, "variable_cost_pct": 0.42},
    "Agriculture": {"avg_margin": 0.25, "avg_roi": 0.12, "fixed_costs": 85000, "variable_cost_pct": 0.6},
    "Perfumes": {"avg_margin": 0.55, "avg_roi": 0.3, "fixed_costs": 70000, "variable_cost_pct": 0.28},
    "Cosmetics": {"avg_margin": 0.5, "avg_roi": 0.26, "fixed_costs": 90000, "variable_cost_pct": 0.32}
}

def run_feasibility(name, email, phone, sector, capital, revenue):
    data = sectors.get(sector)
    if not data:
        return "Invalid sector.", None

    fixed = data["fixed_costs"] / 12
    variable = revenue * data["variable_cost_pct"]
    total_costs = fixed + variable
    profit = revenue - total_costs
    margin = profit / revenue if revenue else 0
    roi = (profit * 12) / capital if capital else 0
    breakeven = fixed / (revenue - variable) if revenue > variable else float('inf')
    required_revenue = fixed / (1 - data["variable_cost_pct"])
    capital_regain = capital / (profit * 12) if profit > 0 else float('inf')

    now = datetime.datetime.now().strftime("%Y-%m-%d")
    df = pd.DataFrame([{
        "Date": now,
        "Name": name,
        "Email": email,
        "Phone": phone,
        "Sector": sector,
        "StartupCapital": capital,
        "ExpectedRevenue": revenue,
        "FixedCosts": fixed,
        "VariableCosts": variable,
        "Profit": profit,
        "Margin": margin,
        "ROI": roi,
        "BreakevenMonths": breakeven,
        "CapitalRegainMonths": capital_regain
    }])

    file_path = "feasibility_clients.csv"
    df.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)

    # رسالة التليجرام
    telegram_msg = f"""
📩 New Feasibility Request:
👤 {name}
📱 {phone}
📧 {email}
📊 Sector: {sector}
💰 Capital: {capital:,.0f} SAR
📈 Monthly Revenue: {revenue:,.0f} SAR
    """
    send_telegram_message(telegram_msg)

    # رسم بياني
    fig, ax = plt.subplots()
    ax.bar(["Revenue", "Total Costs", "Profit"], [revenue, total_costs, profit],
           color=['#0066cc', '#ff6600', '#33cc33'])
    ax.set_title("Financial Snapshot")
    ax.set_ylabel("SAR")
    plt.tight_layout()

    summary_ar = f"""
 الاسم: {name}
 الجوال: {phone}
 البريد الإلكتروني: {email}
 القطاع: {sector}
 رأس المال: {capital:,.0f} ريال
 الإيرادات الشهرية المتوقعة: {revenue:,.0f} ريال
 التكاليف الإجمالية الشهرية: {total_costs:,.0f} ريال
 الربح الشهري المقدر: {profit:,.0f} ريال
 هامش الربح: {margin*100:.1f}% | العائد السنوي: {roi*100:.1f}%
 نقطة التعادل: {breakeven:.1f} شهر
 الإيراد اللازم لنقطة التعادل: {required_revenue:,.0f} ريال
 مدة استعادة رأس المال: {capital_regain:.1f} شهر
 للحصول على دراسة تفصيلية دقيقة احجز استشارة معنا
"""

    summary_en = f"""
Name: {name}
Phone: {phone}
Email: {email}
Sector: {sector}
Startup Capital: {capital:,.0f} SAR
Expected Monthly Revenue: {revenue:,.0f} SAR
Total Monthly Costs: {total_costs:,.0f} SAR
Estimated Monthly Profit: {profit:,.0f} SAR
Margin: {margin*100:.1f}% | Annual ROI: {roi*100:.1f}%
Breakeven Point: {breakeven:.1f} months
Required Monthly Revenue for Break-even: {required_revenue:,.0f} SAR
Capital Regain Point: {capital_regain:.1f} months
For a detailed feasibility report, book a consultation with us.
"""

    return summary_ar + "\n\n" + summary_en, fig

# واجهة Gradio
with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Image(value="header.png", show_label=False)

    with gr.Row():
        with gr.Column():
            name = gr.Textbox(label="الاسم الكامل / Full Name", placeholder="مثال: عبدالرحمن")
            email = gr.Textbox(label="البريد الإلكتروني / Email", placeholder="example@the3g.com")
            phone = gr.Textbox(label="رقم الجوال / Phone", placeholder="0500000000")
            sector = gr.Dropdown(choices=list(sectors.keys()), label="Select Business Sector (اختر القطاع)")
            capital = gr.Number(label="Startup Capital (رأس المال المبدئي المتوقع)", precision=0)
            revenue = gr.Number(label="Expected Monthly Revenue (الإيرادات الشهرية المتوقعة)", precision=0)
            submit = gr.Button("احسب الجدوى / Generate Feasibility")

        with gr.Column():
            result = gr.Textbox(label="Summary / ملخص", lines=20)
            chart = gr.Plot(label="Financial Snapshot")

    submit.click(run_feasibility,
                 inputs=[name, email, phone, sector, capital, revenue],
                 outputs=[result, chart])

app.launch()

