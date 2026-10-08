-- SwipeSense schema: customer + credit_card tables
-- Lives in the same `dynamic_sql` database db_helper.py already connects to.
-- Run this once before the import script (import_swipesense.py also creates
-- these tables defensively via CREATE TABLE IF NOT EXISTS, so running it
-- twice is safe).

USE dynamic_sql;

CREATE TABLE IF NOT EXISTS customer (
    Client_Num               BIGINT UNSIGNED NOT NULL PRIMARY KEY,
    Customer_Age             TINYINT UNSIGNED,
    Gender                   VARCHAR(10),
    Dependent_Count          TINYINT UNSIGNED,
    Education_Level          VARCHAR(50),
    Marital_Status           VARCHAR(20),
    state_cd                 VARCHAR(10),
    Zipcode                  VARCHAR(10),   -- text, not int: preserves leading zeros
    Car_Owner                VARCHAR(5),
    House_Owner              VARCHAR(5),
    Personal_loan            VARCHAR(5),
    contact                  VARCHAR(20),
    Customer_Job             VARCHAR(50),
    Income                   DECIMAL(12, 2),
    Cust_Satisfaction_Score  TINYINT UNSIGNED
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS credit_card (
    Client_Num              BIGINT UNSIGNED NOT NULL PRIMARY KEY,
    Card_Category            VARCHAR(20),
    Annual_Fees              DECIMAL(10, 2),
    Activation_30_Days       TINYINT UNSIGNED,
    Customer_Acq_Cost        DECIMAL(10, 2),
    Week_Start_Date          DATE,
    Week_Num                 VARCHAR(20),   -- text: source data may use "Week-1" style labels
    Qtr                      VARCHAR(10),
    current_year             SMALLINT UNSIGNED,
    Credit_Limit             DECIMAL(12, 2),
    Total_Revolving_Bal      DECIMAL(12, 2),
    Total_Trans_Amt          DECIMAL(12, 2),
    Total_Trans_Vol          INT UNSIGNED,
    Avg_Utilization_Ratio    DECIMAL(6, 4),
    Use_Chip                 VARCHAR(20),   -- source CSV header is "Use Chip" (with a space)
    Exp_Type                 VARCHAR(30),   -- source CSV header is "Exp Type" (with a space)
    Interest_Earned          DECIMAL(10, 2),
    Delinquent_Acc           TINYINT UNSIGNED,
    CONSTRAINT fk_creditcard_client
        FOREIGN KEY (Client_Num) REFERENCES customer(Client_Num)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE INDEX idx_customer_state_cd ON customer(state_cd);
CREATE INDEX idx_creditcard_card_category ON credit_card(Card_Category);
