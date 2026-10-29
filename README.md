# Freelancer Expense Tracker

A simple, single-owner web app that helps freelancers and solo builders track business expenses, see where money is going, and never miss a deductible at tax time.

## The customer problem (the "why")

Freelancers and independent contractors wear every hat — sales, delivery, invoicing, *and* bookkeeping. Expense tracking usually gets deferred until tax season, when they scramble through bank statements and WhatsApp chats to reconstruct what they spent. The cost:

- **Missed deductions** → overpaying tax
- **No visibility into true net income** → can't price work or know if the business is viable
- **Month-end panic** instead of a five-minute habit

Existing tools (heavy accounting suites) are overkill and expensive for a solo builder. This is a purpose-built, dead-simple expense tracker: add an expense in ~10 seconds, see category totals instantly, export-ready data for your CA/accountant.

## What it does

- Add an expense: amount, category, description, date
- View all expenses, newest first
- Delete a mistake
- See a live summary: total spent, count, and per-category breakdown
- Zero setup: runs locally with SQLite, no external accounts

## The product-builder angle

This project was chosen because it solves a problem I've felt firsthand, not because it was assigned. It's small enough for one person to own end-to-end (problem → design → code → deploy → support), which is exactly the kind of ownership this role rewards.

**Business value story:** For a freelancer billing ₹1–3 lakh/month, catching even a few missed deductions (hosting, software subscriptions, coworking, internet) can save thousands in tax per year — and give them real-time clarity on whether their pricing is actually profitable. That's worth paying for.

## Stack (chosen for speed + simplicity, not dogma)

- **Backend:** Flask (Python) — one file, easy to reason about, trivial to deploy
- **Database:** SQLite — file-based, zero config, perfect for a single-user tool
- **Frontend:** vanilla HTML/CSS/JS — no build step, no framework churn, loads instantly
- **AI use:** AI helped generate boilerplate, write tests, and explore edge cases; I framed the problem, reviewed every line, and made the product calls. AI is the tool, not the decision-maker.

This mirrors the role's philosophy: strong CS fundamentals (proper data modeling, validation, separation of concerns) let me learn/ship any stack the problem demands.

## How to run

```bash
# 1. Clone / open this folder
cd freelancer-expense-tracker

# 2. (Optional but recommended) create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py

# 5. Open http://127.0.0.1:5000
```

The first run creates `expenses.db` automatically. Data persists on your machine.

What I'd build next (if this were a real product)

- CSV export for your accountant
- Monthly/quarterly views and trends
- Receipt photo upload (OCR to pre-fill fields)
- Multi-currency support for international clients
- Reminder: "log this week's expenses" every Friday

