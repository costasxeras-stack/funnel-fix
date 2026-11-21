#!/bin/sh
# Downloads the Olist public e-commerce CSVs (MIT licence) into work/.
set -e
mkdir -p work
B=https://raw.githubusercontent.com/olist/work-at-olist-data/master/datasets
for f in olist_orders_dataset olist_customers_dataset olist_order_reviews_dataset olist_order_items_dataset olist_products_dataset product_category_name_translation; do
  curl -sSfL -o "work/$f.csv" "$B/$f.csv"
done
echo "Downloaded to work/"
