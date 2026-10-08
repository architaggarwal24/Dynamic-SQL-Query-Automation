"""
Imports customer.csv and credit_card.csv into the `dynamic_sql` MySQL
database (customer / credit_card tables). Run schema_swipesense.sql once
first, or just run this script directly -- it also creates the tables
defensively via CREATE TABLE IF NOT EXISTS.

Usage:
    python import_swipesense.py
    python import_swipesense.py --customer path/to/customer.csv --credit-card path/to/credit_card.csv

customer.csv must load before credit_card.csv, since credit_card.Client_Num
has a foreign key back to customer.Client_Num.
"""

import argparse
import logging
import sys

import pandas as pd
import mysql.connector as connector

logging.basicConfig(
    filename='logs/import.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "archit",
    "database": "dynamic_sql",
}

BATCH_SIZE = 500

CUSTOMER_COLUMNS = [
    "Client_Num", "Customer_Age", "Gender", "Dependent_Count",
    "Education_Level", "Marital_Status", "state_cd", "Zipcode",
    "Car_Owner", "House_Owner", "Personal_loan", "contact",
    "Customer_Job", "Income", "Cust_Satisfaction_Score",
]

CREDIT_CARD_COLUMNS = [
    "Client_Num", "Card_Category", "Annual_Fees", "Activation_30_Days",
    "Customer_Acq_Cost", "Week_Start_Date", "Week_Num", "Qtr",
    "current_year", "Credit_Limit", "Total_Revolving_Bal",
    "Total_Trans_Amt", "Total_Trans_Vol", "Avg_Utilization_Ratio",
    "Use_Chip", "Exp_Type", "Interest_Earned", "Delinquent_Acc",
]

CREATE_CUSTOMER_TABLE = """
CREATE TABLE IF NOT EXISTS customer (
    Client_Num               BIGINT UNSIGNED NOT NULL PRIMARY KEY,
    Customer_Age             TINYINT UNSIGNED,
    Gender                   VARCHAR(10),
    Dependent_Count          TINYINT UNSIGNED,
    Education_Level          VARCHAR(50),
    Marital_Status           VARCHAR(20),
    state_cd                 VARCHAR(10),
    Zipcode                  VARCHAR(10),
    Car_Owner                VARCHAR(5),
    House_Owner              VARCHAR(5),
    Personal_loan            VARCHAR(5),
    contact                  VARCHAR(20),
    Customer_Job             VARCHAR(50),
    Income                   DECIMAL(12, 2),
    Cust_Satisfaction_Score  TINYINT UNSIGNED
) ENGINE=InnoDB
"""

CREATE_CREDIT_CARD_TABLE = """
CREATE TABLE IF NOT EXISTS credit_card (
    Client_Num              BIGINT UNSIGNED NOT NULL PRIMARY KEY,
    Card_Category            VARCHAR(20),
    Annual_Fees              DECIMAL(10, 2),
    Activation_30_Days       TINYINT UNSIGNED,
    Customer_Acq_Cost        DECIMAL(10, 2),
    Week_Start_Date          DATE,
    Week_Num                 VARCHAR(20),
    Qtr                      VARCHAR(10),
    current_year             SMALLINT UNSIGNED,
    Credit_Limit             DECIMAL(12, 2),
    Total_Revolving_Bal      DECIMAL(12, 2),
    Total_Trans_Amt          DECIMAL(12, 2),
    Total_Trans_Vol          INT UNSIGNED,
    Avg_Utilization_Ratio    DECIMAL(6, 4),
    Use_Chip                 VARCHAR(20),
    Exp_Type                 VARCHAR(30),
    Interest_Earned          DECIMAL(10, 2),
    Delinquent_Acc           TINYINT UNSIGNED,
    CONSTRAINT fk_creditcard_client
        FOREIGN KEY (Client_Num) REFERENCES customer(Client_Num)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB
"""


def ensure_tables(cur):
    cur.execute(CREATE_CUSTOMER_TABLE)
    cur.execute(CREATE_CREDIT_CARD_TABLE)


def clean_dataframe(df):
    """Convert pandas NaN/NaT to None so MySQL stores NULL, not the string 'nan',
    and strip stray whitespace from text columns (credit_card.csv's "Use Chip"
    column ships with trailing spaces, e.g. "Chip " / "Swipe ")."""
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].str.strip()
    return df.where(pd.notnull(df), None)


def rows_for_insert(df, columns):
    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise ValueError(f"CSV is missing expected columns: {missing}")
    return [tuple(row) for row in df[columns].itertuples(index=False, name=None)]


def load_customer(cur, con, csv_path):
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    df = clean_dataframe(df)
    rows = rows_for_insert(df, CUSTOMER_COLUMNS)

    col_list = ", ".join(CUSTOMER_COLUMNS)
    placeholders = ", ".join(["%s"] * len(CUSTOMER_COLUMNS))
    query = f"INSERT INTO customer ({col_list}) VALUES ({placeholders})"

    for i in range(0, len(rows), BATCH_SIZE):
        batch = rows[i:i + BATCH_SIZE]
        cur.executemany(query, batch)
        con.commit()
        logging.info(f"customer: inserted rows {i} to {i + len(batch)}")

    print(f"customer: inserted {len(rows)} rows")
    logging.info(f"customer.csv import complete: {len(rows)} rows")


def load_credit_card(cur, con, csv_path):
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    df = df.rename(columns={"Use Chip": "Use_Chip", "Exp Type": "Exp_Type"})

    if "Week_Start_Date" in df.columns:
        # Source format is day-first (dd-mm-yyyy), e.g. "29-01-2023".
        # Without an explicit format, pandas guesses month-first and either
        # silently swaps day/month or turns any day>12 into NaT.
        df["Week_Start_Date"] = pd.to_datetime(
            df["Week_Start_Date"], format="%d-%m-%Y", errors="coerce"
        )

    df = clean_dataframe(df)

    # Convert remaining Timestamp objects to plain python dates for the connector
    if "Week_Start_Date" in df.columns:
        df["Week_Start_Date"] = df["Week_Start_Date"].apply(
            lambda v: v.date() if isinstance(v, pd.Timestamp) else v
        )

    rows = rows_for_insert(df, CREDIT_CARD_COLUMNS)

    col_list = ", ".join(CREDIT_CARD_COLUMNS)
    placeholders = ", ".join(["%s"] * len(CREDIT_CARD_COLUMNS))
    query = f"INSERT INTO credit_card ({col_list}) VALUES ({placeholders})"

    for i in range(0, len(rows), BATCH_SIZE):
        batch = rows[i:i + BATCH_SIZE]
        cur.executemany(query, batch)
        con.commit()
        logging.info(f"credit_card: inserted rows {i} to {i + len(batch)}")

    print(f"credit_card: inserted {len(rows)} rows")
    logging.info(f"credit_card.csv import complete: {len(rows)} rows")


def main():
    parser = argparse.ArgumentParser(description="Import SwipeSense CSVs into MySQL")
    parser.add_argument("--customer", default="customer.csv", help="Path to customer.csv")
    parser.add_argument("--credit-card", default="credit_card.csv", help="Path to credit_card.csv")
    args = parser.parse_args()

    con = connector.connect(**DB_CONFIG)
    cur = con.cursor()

    try:
        ensure_tables(cur)
        con.commit()
        load_customer(cur, con, args.customer)       # parent table first (FK dependency)
        load_credit_card(cur, con, args.credit_card)  # child table second
    except connector.Error as err:
        logging.error(f"Database Error during import: {err}")
        print(f"Database Error: {err}")
        con.rollback()
        sys.exit(1)
    except Exception as err:
        logging.error(f"Import Error: {err}")
        print(f"Error: {err}")
        sys.exit(1)
    finally:
        cur.close()
        con.close()


if __name__ == "__main__":
    main()
