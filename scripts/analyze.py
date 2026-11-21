"""Funnel Fix analysis on the Olist public data. Run from the repo root after scripts/0-download.sh.
Finds the weakest funnel step, what predicts a second order, and the baseline for the experiment.
Writes data/funnel.json and prints every number used on the page."""
import json
import numpy as np, pandas as pd
W = "work"
o = pd.read_csv(f"{W}/olist_orders_dataset.csv", parse_dates=["order_purchase_timestamp", "order_delivered_customer_date", "order_estimated_delivery_date"])
c = pd.read_csv(f"{W}/olist_customers_dataset.csv"); r = pd.read_csv(f"{W}/olist_order_reviews_dataset.csv").drop_duplicates("order_id")
it = pd.read_csv(f"{W}/olist_order_items_dataset.csv"); p = pd.read_csv(f"{W}/olist_products_dataset.csv"); tr = pd.read_csv(f"{W}/product_category_name_translation.csv")
o = o.merge(c[["customer_id", "customer_unique_id"]], on="customer_id").merge(r[["order_id", "review_score"]], on="order_id", how="left")
END = pd.Timestamp("2018-09-01")  # orders after August 2018 are a handful of stragglers
o = o[o.order_purchase_timestamp < END].sort_values("order_purchase_timestamp")
o["n"] = o.groupby("customer_unique_id").cumcount() + 1
first = o[o.n == 1].copy()
# next order on a later day (same-day second orders are split baskets, not a return visit)
later = o.merge(first[["customer_unique_id", "order_purchase_timestamp"]].rename(columns={"order_purchase_timestamp": "t0"}), on="customer_unique_id")
later = later[later.order_purchase_timestamp.dt.normalize() > later.t0.dt.normalize()]
nxt = later.groupby("customer_unique_id").order_purchase_timestamp.min().rename("next_at")
first = first.join(nxt, on="customer_unique_id")
first["gap"] = (first.next_at - first.order_purchase_timestamp).dt.days
same_day = o[o.n == 2].merge(first[["customer_unique_id", "order_purchase_timestamp"]].rename(columns={"order_purchase_timestamp": "t0"}), on="customer_unique_id")
same_day_share = float((same_day.order_purchase_timestamp.dt.normalize() == same_day.t0.dt.normalize()).mean())
out = {}
# Funnel: customers -> first order delivered -> reviewed -> reviewed 4 or 5 -> second order within 180 days (customers with 180 days of history)
f = first[first.order_purchase_timestamp <= END - pd.Timedelta(days=180)].copy()
f["delivered"] = f.order_status == "delivered"; f["reviewed"] = f.review_score.notna(); f["happy"] = f.review_score >= 4
f["rep180"] = f.gap.between(1, 180); f["rep90"] = f.gap.between(1, 90)
n = len(f)
steps = [("Placed a first order", n), ("First order delivered", int(f.delivered.sum())), ("Left a review", int((f.delivered & f.reviewed).sum())),
         ("Rated it 4 or 5 stars", int((f.delivered & f.happy).sum())), ("Ordered again within 180 days", int((f.delivered & f.happy & f.rep180).sum()))]
out["funnel"] = [{"step": s, "customers": v, "pct_of_start": round(v / n * 100, 1), "pct_of_previous": round(v / steps[i - 1][1] * 100, 1) if i else 100.0} for i, (s, v) in enumerate(steps)]
out["customers_total"] = int(o.customer_unique_id.nunique()); out["customers_180d"] = n
out["any_repeat_pct"] = round(float((o.groupby("customer_unique_id").size() > 1).mean() * 100), 2)
out["same_day_share_of_second_orders"] = round(same_day_share * 100, 1)
out["rep180_pct"] = round(float(f.rep180.mean() * 100), 2); out["rep90_pct"] = round(float(f.rep90.mean() * 100), 2)
# What predicts coming back
f["late"] = f.order_delivered_customer_date > f.order_estimated_delivery_date
seg = []
for name, mask in [("Delivered on time", f.delivered & ~f.late), ("Delivered late", f.delivered & f.late), ("Rated 4 or 5", f.review_score >= 4), ("Rated 3", f.review_score == 3), ("Rated 1 or 2", f.review_score <= 2)]:
    seg.append({"segment": name, "customers": int(mask.sum()), "rep180_pct": round(float(f[mask].rep180.mean() * 100), 2)})
out["segments"] = seg
# Category of the first order
cat = it.drop_duplicates("order_id")[["order_id", "product_id"]].merge(p[["product_id", "product_category_name"]], on="product_id").merge(tr, on="product_category_name", how="left")
f = f.merge(cat[["order_id", "product_category_name_english"]], on="order_id", how="left")
g = f.groupby("product_category_name_english").agg(customers=("rep180", "size"), rep180=("rep180", "mean")).query("customers >= 1500").sort_values("rep180", ascending=False)
out["categories"] = [{"category": k.replace("_", " "), "customers": int(v.customers), "rep180_pct": round(float(v.rep180 * 100), 2)} for k, v in g.iterrows()]
# When people come back (days to second order, among those who do, within 365 days)
gaps = first.gap.dropna(); gaps = gaps[(gaps >= 1) & (gaps <= 365)]
out["gap_median_days"] = float(gaps.median()); out["gap_p25"] = float(gaps.quantile(.25)); out["gap_p75"] = float(gaps.quantile(.75))
bins = [0, 30, 60, 90, 120, 180, 270, 365]
h = pd.cut(gaps, bins).value_counts().sort_index()
out["gap_hist"] = [{"days": f"{int(i.left) + 1} to {int(i.right)}", "customers": int(v)} for i, v in h.items()]
# Experiment population and traffic: happy, on-time first orders per month in 2018
f2 = first.copy(); f2["late"] = f2.order_delivered_customer_date > f2.order_estimated_delivery_date
elig = f2[(f2.order_status == "delivered") & ~f2.late & (f2.review_score >= 4)]
m = elig[(elig.order_purchase_timestamp >= "2018-01-01")].groupby(elig.order_purchase_timestamp.dt.to_period("M")).size()
out["eligible_per_month_2018"] = int(round(m.mean())); out["new_customers_per_month_2018"] = int(round(first[first.order_purchase_timestamp >= "2018-01-01"].groupby(first.order_purchase_timestamp.dt.to_period("M")).size().mean()))
ef = elig[elig.order_purchase_timestamp <= END - pd.Timedelta(days=180)]
out["baseline_rep90_eligible_pct"] = round(float(ef.gap.between(1, 90).mean() * 100), 2)
out["baseline_rep180_eligible_pct"] = round(float(ef.gap.between(1, 180).mean() * 100), 2)
v = it.groupby("order_id").agg(value=("price", "sum"), freight=("freight_value", "sum")).reset_index().merge(o[["order_id", "order_status"]], on="order_id")
v = v[v.order_status == "delivered"]
out["order_value_median_brl"] = round(float(v.value.median()), 2); out["freight_median_brl"] = round(float(v.freight.median()), 2)
json.dump(out, open("data/funnel.json", "w"), indent=1)
print(json.dumps(out, indent=1))
