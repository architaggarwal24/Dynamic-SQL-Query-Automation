import csv
import io

from flask import Flask, render_template, request, redirect, url_for, session, Response
from db_helper import DBHelper, QUERYABLE_COLUMNS, OPERATOR_OPTIONS

app = Flask(__name__)
app.secret_key = "super-secret-key-change-this"
db = DBHelper()


def csv_response(filename, rows_writer):
    """Build a Flask Response streaming a CSV file, written via Python's
    csv module (never string-concatenated). rows_writer is a callable that
    takes a csv.writer and writes whatever rows/sections it needs to it --
    keeps this helper reusable for both a single flat table (/query export)
    and the multi-section file (/stats export)."""
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    rows_writer(writer)
    return Response(
        buffer.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )

@app.route('/')
def home():
    users = db.fetch_all()
    return render_template('index.html', users=users)

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        userName = request.form.get('userName')
        phone = request.form.get('phone')

        try:
            db.insert_user(userName, phone)
            session['toast'] = ('success', 'User added successfully!')
        except Exception:
            session['toast'] = ('error', 'Database error occurred!')

        return redirect('/')

    return render_template('insert.html')



@app.route('/update/<int:userId>', methods=['GET', 'POST'])
def update(userId):
    if request.method == 'POST':
        newName = request.form['userName']
        newPhone = request.form['phone']
        db.update_user(userId, newName, newPhone)
        return redirect(url_for('home'))
    return render_template('update.html', userId=userId)

@app.route('/delete/<int:userId>')
def delete(userId):
    db.delete_user(userId)
    return redirect(url_for('home'))

@app.route('/query', methods=['GET', 'POST'])
def query():
    columns = request.form.getlist('column')
    operators = request.form.getlist('operator')
    values = request.form.getlist('value')

    result_columns = None
    results = None
    capped = False
    error = None
    ran_query = False

    if request.method == 'POST':
        ran_query = True
        # Only keep rows where the user actually filled in all three parts
        conditions = [c for c in zip(columns, operators, values) if c[0] and c[1] and c[2] != '']

        if not conditions:
            error = "Add at least one complete condition (column, operator, and value)."
        else:
            try:
                result_columns, results, capped = db.run_dynamic_query(conditions)
            except ValueError as err:
                error = str(err)

    return render_template(
        'query.html',
        column_options=list(QUERYABLE_COLUMNS.keys()),
        operator_options=OPERATOR_OPTIONS,
        submitted=list(zip(columns, operators, values)),
        result_columns=result_columns,
        results=results,
        capped=capped,
        error=error,
        ran_query=ran_query,
    )

@app.route('/query/export', methods=['POST'])
def query_export():
    columns = request.form.getlist('column')
    operators = request.form.getlist('operator')
    values = request.form.getlist('value')
    conditions = [c for c in zip(columns, operators, values) if c[0] and c[1] and c[2] != '']

    if not conditions:
        # Nothing to export -- bounce back to the builder rather than
        # downloading an empty/misleading file.
        return redirect(url_for('query'))

    try:
        # Same call /query itself uses, so the export is guaranteed to
        # match what's rendered on screen -- same rows, same 200-row cap.
        result_columns, results, _capped = db.run_dynamic_query(conditions)
    except ValueError:
        return redirect(url_for('query'))

    def write_rows(writer):
        writer.writerow(result_columns)
        writer.writerows(results)

    return csv_response('query_results.csv', write_rows)

@app.route('/stats')
def stats():
    education_stats = db.stats_income_revenue_by_education()
    card_category_stats = db.stats_transaction_amount_by_card_category()
    job_stats = db.stats_customer_count_satisfaction_by_job()

    top_n_raw = request.args.get('top_n', '5')
    error = None
    try:
        state_stats = db.stats_top_states_by_revenue(top_n_raw)
        top_n = int(top_n_raw)
    except ValueError as err:
        error = str(err)
        state_stats = db.stats_top_states_by_revenue(5)
        top_n = 5

    return render_template(
        'stats.html',
        education_stats=education_stats,
        card_category_stats=card_category_stats,
        job_stats=job_stats,
        state_stats=state_stats,
        top_n=top_n,
        error=error,
    )

@app.route('/stats/export')
def stats_export():
    # Same DB calls /stats itself uses -- guarantees the export matches
    # what's currently on screen, including the current top_n.
    education_stats = db.stats_income_revenue_by_education()
    card_category_stats = db.stats_transaction_amount_by_card_category()
    job_stats = db.stats_customer_count_satisfaction_by_job()

    top_n_raw = request.args.get('top_n', '5')
    try:
        state_stats = db.stats_top_states_by_revenue(top_n_raw)
        top_n = int(top_n_raw)
    except ValueError:
        state_stats = db.stats_top_states_by_revenue(5)
        top_n = 5

    def write_rows(writer):
        writer.writerow(['Average Income & Revenue by Education Level'])
        writer.writerow(['Education_Level', 'Avg_Income', 'Avg_Revenue', 'Customer_Count'])
        writer.writerows(education_stats)
        writer.writerow([])

        writer.writerow(['Total Transaction Amount by Card Category'])
        writer.writerow(['Card_Category', 'Total_Trans_Amt', 'Card_Count'])
        writer.writerows(card_category_stats)
        writer.writerow([])

        writer.writerow(['Customer Count & Avg Satisfaction by Job'])
        writer.writerow(['Customer_Job', 'Customer_Count', 'Avg_Satisfaction_Score'])
        writer.writerows(job_stats)
        writer.writerow([])

        writer.writerow([f'Top {top_n} States by Revenue'])
        writer.writerow(['State_Cd', 'Total_Revenue'])
        writer.writerows(state_stats)

    return csv_response('stats_export.csv', write_rows)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
