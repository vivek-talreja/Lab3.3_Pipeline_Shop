"""Validation rules for the shop pipeline - one line per rule.

Each rule is a Chapter 2 data-quality check, written once and run on every run.
If a rule here fails, the pipeline STOPS and writes nothing (see pipeline.validate).
Row-level problems (bad quantity, unknown customer, ...) are handled in
pipeline.split() and go to the quarantine file instead.
"""
import pandas as pd
import pandera.pandas as pa
from pandera.pandas import Column, Check

# Custom check: an order cannot be placed in the future.
def not_in_future(dates):
    return dates.isna() | (dates <= pd.Timestamp.today().normalize())


clean_orders_rules = pa.DataFrameSchema({
    "order_date":  Column("datetime64[ns]", nullable=True,
                          checks=Check(not_in_future, name="order_date_not_in_future",
                                       error="order_date lies in the future")),
    "order_id":    Column(str, unique=True, nullable=False,
                          checks=Check.str_matches(r"^[A-Z]\d{3}$")),
    "customer_id": Column(str, nullable=False),
    "category":    Column(str, Check.isin(["Accessories", "Electronics"])),
    "quantity":    Column(float, nullable=True),
    "unit_price":  Column(float, [Check.ge(0), Check.le(5000)], nullable=True),
})

clean_customers_rules = pa.DataFrameSchema({
    "customer_id":   Column(str, unique=True, nullable=False,
                            checks=Check.str_matches(r"^C\d{3}$")),
    "customer_name": Column(str, nullable=False),
    "city":          Column(str, nullable=False),
    "segment":       Column(str, Check.isin(["Private", "Business"])),
    # Lab 3.2 rules
    "email":         Column(str, Check.str_matches(r"^$|^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$")),
    "country":       Column(str, Check.isin(["Germany", "Austria", "Switzerland"])),
})
