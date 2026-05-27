#!/usr/bin/env python3
"""
02_seed.sql を生成するスクリプト。
実行: python generate_seed.py > infrastructure/db/seed/02_seed.sql
"""
import random
from datetime import datetime, timedelta

# --- 設定 ---
SEED        = 42
ORDERS_COUNT = 400
DATE_FROM   = datetime(2025, 12, 1)
DATE_TO     = datetime(2026, 5, 31)

random.seed(SEED)

customers = [
    "株式会社東京商事",
    "大阪物産株式会社",
    "名古屋産業株式会社",
    "福岡商事株式会社",
    "株式会社札幌オフィス",
    "横浜トレーディング株式会社",
    "仙台ビジネス株式会社",
    "広島商工株式会社",
]

# (商品名, CategoryId, 単価)
# CategoryId: 1=事務用品, 2=家具, 3=消耗品
items = [
    ("高性能オフィスチェア",   1, 85000),
    ("デスクライト",           1, 12000),
    ("ホワイトボード",         1, 28000),
    ("シュレッダー",           1, 35000),
    ("スタンディングデスク",   2, 120000),
    ("会議用テーブル",         2, 95000),
    ("ロッカー",               2, 45000),
    ("パーテーション",         2, 38000),
    ("コピー用紙(500枚)",      3, 1500),
    ("ボールペン(10本セット)", 3, 800),
    ("クリアファイル(10枚)",   3, 600),
    ("トナーカートリッジ",     3, 8500),
]

total_days = (DATE_TO - DATE_FROM).days

print("-- サンプルデータ投入")
print()

# M_Stock 追加
print("-- 在庫マスタ追加")
for name, _, _ in items:
    stock = random.randint(20, 200)
    print(f"INSERT INTO M_Stock (ItemName, CurrentStock) VALUES ('{name}', {stock}) ON CONFLICT DO NOTHING;")
print()

# Orders 生成
print("-- 受注データ")
counter: dict[str, int] = {}

for _ in range(ORDERS_COUNT):
    delta      = random.randint(0, total_days)
    order_date = DATE_FROM + timedelta(days=delta)
    date_str   = order_date.strftime("%Y%m%d")
    counter[date_str] = counter.get(date_str, 0) + 1
    order_no   = f"{date_str}-{counter[date_str]:03d}"

    customer              = random.choice(customers)
    item_name, cat_id, price = random.choice(items)

    qty   = random.randint(5, 50) if cat_id == 3 else random.randint(1, 10)
    total = price * qty
    total_with_tax = total + int(total * 0.1)

    ts = order_date.strftime("%Y-%m-%d") + f" {random.randint(8,17):02d}:{random.randint(0,59):02d}:00"

    print(
        f"INSERT INTO Orders "
        f"(OrderNo, OrderDate, CustomerName, CategoryId, ItemName, Price, Qty, TotalAmount) "
        f"VALUES ('{order_no}', '{ts}', '{customer}', {cat_id}, '{item_name}', "
        f"{price}, {qty}, {total_with_tax}) ON CONFLICT DO NOTHING;"
    )

print()
print(f"-- 生成件数: {ORDERS_COUNT} 件")
