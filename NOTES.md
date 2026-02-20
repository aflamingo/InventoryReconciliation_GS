1. `reconcile.py` (or similar) - your reconciliation script
2. `tests/` - test coverage for your logic
3. `output/` - your reconciliation results
4. `NOTES.md` - brief write-up (~half page):
   - Key decisions or assumptions you made
   - Any data quality issues you found
   - How you approached the problem
  
**Identifies**:
   - Items present in both snapshots (and whether quantities changed) --> common.csv
   - Items only in snapshot 1 (removed/sold out)  --> removed.csv
   - Items only in snapshot 2 (newly added)  --> added.csv

   - 
   - Any data quality issues worth flagging

## DATA SNANPSHOT 1 75
 # 0   sku           75 non-null     str
 # 1   name          75 non-null     str
 # 2   quantity      75 non-null     int64
 # 3   location      75 non-null     str
 # 4   last_counted  75 non-null     str
 
## DATA SNANPSHOT 2
 # 0   sku           79 non-null     str
 # 1   product_name  79 non-null     str      -- make col names match
 # 2   qty           79 non-null     float64  -- standardize name data type
 # 3   warehouse     79 non-null     str      -- make col names match
 # 4   updated_at    79 non-null     str      -- change type
