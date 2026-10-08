import mysql.connector as connector
import logging

logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# Allow-list mapping "friendly label shown in the dropdown" -> "actual
# table.column SQL identifier". This is the single source of truth for
# the /query builder: app.py renders the dropdown from these keys, and
# DBHelper.run_dynamic_query() re-validates every submitted column
# against these same keys before it ever touches SQL. Column/table
# identifiers can't be sent as %s parameters (placeholders are for
# VALUES only), so this whitelist -- not parameter binding -- is what
# keeps the dynamic WHERE clause injection-safe. NEVER build a query by
# dropping a raw client-submitted string in here.
QUERYABLE_COLUMNS = {
    # customer table
    "Client_Num": "customer.Client_Num",
    "Customer_Age": "customer.Customer_Age",
    "Gender": "customer.Gender",
    "Dependent_Count": "customer.Dependent_Count",
    "Education_Level": "customer.Education_Level",
    "Marital_Status": "customer.Marital_Status",
    "State_Cd": "customer.state_cd",
    "Zipcode": "customer.Zipcode",
    "Car_Owner": "customer.Car_Owner",
    "House_Owner": "customer.House_Owner",
    "Personal_Loan": "customer.Personal_loan",
    "Contact": "customer.contact",
    "Customer_Job": "customer.Customer_Job",
    "Income": "customer.Income",
    "Cust_Satisfaction_Score": "customer.Cust_Satisfaction_Score",
    # credit_card table
    "Card_Category": "credit_card.Card_Category",
    "Annual_Fees": "credit_card.Annual_Fees",
    "Activation_30_Days": "credit_card.Activation_30_Days",
    "Customer_Acq_Cost": "credit_card.Customer_Acq_Cost",
    "Week_Start_Date": "credit_card.Week_Start_Date",
    "Week_Num": "credit_card.Week_Num",
    "Qtr": "credit_card.Qtr",
    "Current_Year": "credit_card.current_year",
    "Credit_Limit": "credit_card.Credit_Limit",
    "Total_Revolving_Bal": "credit_card.Total_Revolving_Bal",
    "Total_Trans_Amt": "credit_card.Total_Trans_Amt",
    "Total_Trans_Vol": "credit_card.Total_Trans_Vol",
    "Avg_Utilization_Ratio": "credit_card.Avg_Utilization_Ratio",
    "Use_Chip": "credit_card.Use_Chip",
    "Exp_Type": "credit_card.Exp_Type",
    "Interest_Earned": "credit_card.Interest_Earned",
    "Delinquent_Acc": "credit_card.Delinquent_Acc",
}

# Fixed operator whitelist -- also re-validated server-side for the same
# reason as QUERYABLE_COLUMNS above (a client could POST directly to
# /query and skip the HTML <select> entirely).
OPERATOR_OPTIONS = ["=", ">", "<", ">=", "<=", "LIKE"]


class DBHelper:
    def __init__(self):
        self.con = connector.connect(host="localhost",user ="root",password="archit",database="dynamic_sql")
        query = 'create table if not exists user(userId int primary key AUTO_INCREMENT,userName varchar(200), phone varchar(12))'
        cur = self.con.cursor()
        cur.execute(query)
        logging.info("User table creation checked/created successfully.")

        # SwipeSense tables (schema also lives in schema_swipesense.sql;
        # kept here too, mirroring the existing bootstrap pattern above,
        # so a fresh checkout works without a manual schema step).
        customer_query = '''
            create table if not exists customer (
                Client_Num              bigint unsigned not null primary key,
                Customer_Age            tinyint unsigned,
                Gender                  varchar(10),
                Dependent_Count         tinyint unsigned,
                Education_Level         varchar(50),
                Marital_Status          varchar(20),
                state_cd                varchar(10),
                Zipcode                 varchar(10),
                Car_Owner               varchar(5),
                House_Owner             varchar(5),
                Personal_loan           varchar(5),
                contact                 varchar(20),
                Customer_Job            varchar(50),
                Income                  decimal(12,2),
                Cust_Satisfaction_Score tinyint unsigned
            ) ENGINE=InnoDB
        '''
        cur.execute(customer_query)

        credit_card_query = '''
            create table if not exists credit_card (
                Client_Num             bigint unsigned not null primary key,
                Card_Category           varchar(20),
                Annual_Fees              decimal(10,2),
                Activation_30_Days        tinyint unsigned,
                Customer_Acq_Cost          decimal(10,2),
                Week_Start_Date              date,
                Week_Num                      varchar(20),
                Qtr                            varchar(10),
                current_year                    smallint unsigned,
                Credit_Limit                     decimal(12,2),
                Total_Revolving_Bal               decimal(12,2),
                Total_Trans_Amt                    decimal(12,2),
                Total_Trans_Vol                     int unsigned,
                Avg_Utilization_Ratio                 decimal(6,4),
                Use_Chip                               varchar(20),
                Exp_Type                                varchar(30),
                Interest_Earned                          decimal(10,2),
                Delinquent_Acc                            tinyint unsigned,
                constraint fk_creditcard_client
                    foreign key (Client_Num) references customer(Client_Num)
                    on delete cascade on update cascade
            ) ENGINE=InnoDB
        '''
        cur.execute(credit_card_query)
        self.con.commit()
        logging.info("SwipeSense table creation checked/created successfully.")


    
    def insert_user(self, username, phone):
        try:
            query = "INSERT INTO user (userName, phone) VALUES (%s, %s)"
            cur = self.con.cursor()
            cur.execute(query, (username, phone))
            self.con.commit()
            logging.info("User inserted successfully")

        except connector.Error as err:
            logging.error(f"Database Error: {err}")
            raise err
    
    
    def fetch_all(self):
        try:
            query = "select * from user"
            cur = self.con.cursor()
            cur.execute(query)
            result = cur.fetchall()
            logging.info("Fetched all users successfully")
            return result
        except connector.Error as err:
            logging.error(f"Database Error: {err}")
            return []

    
    

    def delete_user(self,userId):
        try:
            query = "delete from user where userId=%s"
            c= self.con.cursor()
            c.execute(query, (userId,))
            self.con.commit()
            logging.info("User deleted successfully")

        except connector.Error as err:
            print(f"Database Error: {err}")
    


    def update_user(self,userId,newName,newPhone):
        try:
            query ="update user set userName=%s, phone=%s where userId=%s"
            cur =self.con.cursor()
            cur.execute(query, (newName, newPhone, userId))
            self.con.commit()
            logging.info("User updated successfully")
        except connector.Error as err:
            print(f"Database Error: {err}")


    # ---- SwipeSense: customer / credit_card fetch methods ----

    def fetch_all_customers(self):
        try:
            query = "select * from customer"
            cur = self.con.cursor()
            cur.execute(query)
            result = cur.fetchall()
            logging.info("Fetched all customers successfully")
            return result
        except connector.Error as err:
            logging.error(f"Database Error: {err}")
            return []

    def fetch_customer_by_id(self, client_num):
        try:
            query = "select * from customer where Client_Num=%s"
            cur = self.con.cursor()
            cur.execute(query, (client_num,))
            result = cur.fetchone()
            logging.info(f"Fetched customer {client_num} successfully")
            return result
        except connector.Error as err:
            logging.error(f"Database Error: {err}")
            return None

    def fetch_customers_by_state(self, state_cd):
        try:
            query = "select * from customer where state_cd=%s"
            cur = self.con.cursor()
            cur.execute(query, (state_cd,))
            result = cur.fetchall()
            logging.info(f"Fetched customers for state {state_cd} successfully")
            return result
        except connector.Error as err:
            logging.error(f"Database Error: {err}")
            return []

    def fetch_all_credit_cards(self):
        try:
            query = "select * from credit_card"
            cur = self.con.cursor()
            cur.execute(query)
            result = cur.fetchall()
            logging.info("Fetched all credit cards successfully")
            return result
        except connector.Error as err:
            logging.error(f"Database Error: {err}")
            return []

    def fetch_credit_card_by_id(self, client_num):
        try:
            query = "select * from credit_card where Client_Num=%s"
            cur = self.con.cursor()
            cur.execute(query, (client_num,))
            result = cur.fetchone()
            logging.info(f"Fetched credit card {client_num} successfully")
            return result
        except connector.Error as err:
            logging.error(f"Database Error: {err}")
            return None

    def fetch_customer_with_card(self, client_num):
        try:
            query = '''
                select c.*, cc.*
                from customer c
                join credit_card cc on c.Client_Num = cc.Client_Num
                where c.Client_Num = %s
            '''
            cur = self.con.cursor()
            cur.execute(query, (client_num,))
            result = cur.fetchone()
            logging.info(f"Fetched joined customer+credit_card for {client_num} successfully")
            return result
        except connector.Error as err:
            logging.error(f"Database Error: {err}")
            return None

    def count_rows(self, table_name):
        # Table/column identifiers can't be passed as %s parameters (that
        # placeholder syntax is for VALUES, not identifiers), so table_name
        # is checked against a fixed allow-list here rather than ever being
        # interpolated directly -- keeps this injection-safe like the rest
        # of the file.
        allowed_tables = ("user", "customer", "credit_card")
        if table_name not in allowed_tables:
            raise ValueError(f"Unsupported table: {table_name}")
        try:
            query = f"select count(*) from {table_name}"
            cur = self.con.cursor()
            cur.execute(query)
            result = cur.fetchone()[0]
            logging.info(f"Counted rows in {table_name}: {result}")
            return result
        except connector.Error as err:
            logging.error(f"Database Error: {err}")
            return None

    # ---- Dynamic query builder (the feature the project is named for) ----

    RESULT_ROW_LIMIT = 200

    def run_dynamic_query(self, conditions):
        """
        conditions: list of (column_label, operator, value) tuples from the
        /query form. column_label must be a key in QUERYABLE_COLUMNS and
        operator must be in OPERATOR_OPTIONS -- both are re-checked here
        against the fixed allow-lists, never trusted from the request.
        Only the user-typed `value` is ever placed in the query, and only
        via a %s placeholder bound through cursor.execute(); it is never
        concatenated or f-string'd into the SQL text.

        Returns (column_names, rows, capped) where capped is True if more
        than RESULT_ROW_LIMIT rows matched (results are truncated to that
        limit for display).
        Raises ValueError if a condition fails validation or the query
        itself fails.
        """
        where_clauses = []
        params = []

        for column_label, operator, value in conditions:
            if column_label not in QUERYABLE_COLUMNS:
                raise ValueError(f"Unknown column: {column_label}")
            if operator not in OPERATOR_OPTIONS:
                raise ValueError(f"Unsupported operator: {operator}")

            sql_column = QUERYABLE_COLUMNS[column_label]  # from the allow-list only
            where_clauses.append(f"{sql_column} {operator} %s")
            params.append(value)

        where_sql = " AND ".join(where_clauses)

        # RESULT_ROW_LIMIT is a hardcoded int constant, not user input, so
        # embedding it directly is safe -- it never carries request data.
        query = f'''
            SELECT customer.*, credit_card.*
            FROM customer
            JOIN credit_card ON customer.Client_Num = credit_card.Client_Num
            WHERE {where_sql}
            LIMIT {self.RESULT_ROW_LIMIT + 1}
        '''

        try:
            cur = self.con.cursor()
            cur.execute(query, tuple(params))
            rows = cur.fetchall()

            capped = len(rows) > self.RESULT_ROW_LIMIT
            if capped:
                rows = rows[:self.RESULT_ROW_LIMIT]

            # customer.* and credit_card.* both include Client_Num (the
            # join key), so de-duplicate the header labels for display.
            raw_names = [desc[0] for desc in cur.description]
            seen = {}
            col_names = []
            for name in raw_names:
                seen[name] = seen.get(name, 0) + 1
                col_names.append(name if seen[name] == 1 else f"{name}_{seen[name]}")

            logging.info(
                f"Dynamic query executed: {len(conditions)} condition(s), {len(rows)} row(s) returned"
            )
            return col_names, rows, capped
        except connector.Error as err:
            logging.error(f"Database Error in dynamic query: {err}")
            raise ValueError(f"Database error: {err}")


    # ---- /stats: aggregate queries ----
    # "Revenue" has no literal column in either CSV -- it's defined here as
    # Interest_Earned + Total_Trans_Amt + Annual_Fees, the standard measure
    # for this dataset. None of the four queries below take user input, so
    # none need %s placeholders -- GROUP BY runs over fixed column names,
    # not request data. stats_top_states_by_revenue() is the one exception
    # (top_n is caller-influenced), so that one validates top_n against a
    # bounded range and binds it with %s in the LIMIT clause.

    def stats_income_revenue_by_education(self):
        try:
            query = '''
                SELECT
                    c.Education_Level,
                    ROUND(AVG(c.Income), 2) AS avg_income,
                    ROUND(AVG(cc.Interest_Earned + cc.Total_Trans_Amt + cc.Annual_Fees), 2) AS avg_revenue,
                    COUNT(*) AS customer_count
                FROM customer c
                JOIN credit_card cc ON c.Client_Num = cc.Client_Num
                GROUP BY c.Education_Level
                ORDER BY avg_income DESC
            '''
            cur = self.con.cursor()
            cur.execute(query)
            result = cur.fetchall()
            logging.info("Fetched income/revenue by education stats successfully")
            return result
        except connector.Error as err:
            logging.error(f"Database Error: {err}")
            return []

    def stats_transaction_amount_by_card_category(self):
        try:
            query = '''
                SELECT
                    Card_Category,
                    ROUND(SUM(Total_Trans_Amt), 2) AS total_trans_amt,
                    COUNT(*) AS card_count
                FROM credit_card
                GROUP BY Card_Category
                ORDER BY total_trans_amt DESC
            '''
            cur = self.con.cursor()
            cur.execute(query)
            result = cur.fetchall()
            logging.info("Fetched transaction amount by card category stats successfully")
            return result
        except connector.Error as err:
            logging.error(f"Database Error: {err}")
            return []

    def stats_customer_count_satisfaction_by_job(self):
        try:
            query = '''
                SELECT
                    Customer_Job,
                    COUNT(*) AS customer_count,
                    ROUND(AVG(Cust_Satisfaction_Score), 2) AS avg_satisfaction
                FROM customer
                GROUP BY Customer_Job
                ORDER BY customer_count DESC
            '''
            cur = self.con.cursor()
            cur.execute(query)
            result = cur.fetchall()
            logging.info("Fetched customer count/satisfaction by job stats successfully")
            return result
        except connector.Error as err:
            logging.error(f"Database Error: {err}")
            return []

    def stats_top_states_by_revenue(self, top_n=5):
        # top_n is caller-influenced (comes from a query string in app.py),
        # so it's bounds-checked here and bound via %s in LIMIT -- never
        # f-string'd into the query, even though it's "just a number".
        try:
            top_n = int(top_n)
        except (TypeError, ValueError):
            raise ValueError("top_n must be a whole number")
        if not (1 <= top_n <= 50):
            raise ValueError("top_n must be between 1 and 50")

        try:
            query = '''
                SELECT
                    c.state_cd,
                    ROUND(SUM(cc.Interest_Earned + cc.Total_Trans_Amt + cc.Annual_Fees), 2) AS total_revenue
                FROM customer c
                JOIN credit_card cc ON c.Client_Num = cc.Client_Num
                GROUP BY c.state_cd
                ORDER BY total_revenue DESC
                LIMIT %s
            '''
            cur = self.con.cursor()
            cur.execute(query, (top_n,))
            result = cur.fetchall()
            logging.info(f"Fetched top {top_n} states by revenue successfully")
            return result
        except connector.Error as err:
            logging.error(f"Database Error: {err}")
            return []

if __name__ == '__main__':
    db = DBHelper()
    db.fetch_all()