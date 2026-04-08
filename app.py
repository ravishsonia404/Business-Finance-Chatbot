from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get('file')

    if not file:
        return "❌ No file uploaded"

    try:
        df = pd.read_csv(file)

        # ✅ Clean column names (important fix)
        df.columns = df.columns.str.strip().str.lower()

        # ✅ Check required columns
        if 'revenue' not in df.columns or 'expenses' not in df.columns:
            return "❌ CSV must contain 'Revenue' and 'Expenses' columns"

        # ✅ Convert to numeric (handle text values)
        df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
        df['expenses'] = pd.to_numeric(df['expenses'], errors='coerce')

        # ✅ Calculate values
        revenue = df['revenue'].sum()
        expenses = df['expenses'].sum()
        profit = revenue - expenses

        # ✅ AI Insight
        if profit > 0:
            insight = "✅ Your business is profitable. Keep growing!"
        elif profit < 0:
            insight = "⚠️ You are in loss. Try reducing expenses."
        else:
            insight = "😐 Break-even point. No profit, no loss."

        return render_template("index.html",
                               revenue=round(revenue, 2),
                               expenses=round(expenses, 2),
                               profit=round(profit, 2),
                               insight=insight)

    except Exception as e:
        return f"❌ Error processing file: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)