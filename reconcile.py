
# Two snapshots were taken a week apart, and you 
# need to reconcile them to understand what changed.


############
###SETUP & DATA LOAD
############

## install packages if needed
#pip install pandas numpy datetime

## import packages, run every time 
import pandas as pd, numpy as np, datetime 

### Load data snapshots
df1 = pd.read_csv("snapshot_1.csv")
df2 = pd.read_csv("snapshot_2.csv")


## Put data frames into a list for easier handling and to make code flexible
dflist = [df1, df2] 

## General column name, remove extra spaces, make lower
for df in dflist:
    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_") 


############
### INSPECT & CLEAN
############

## Return structure (num of rows, col names, data types)
for df in dflist:
    df.info()

### Findings:
    # mismatch in num of records
    # mismatch on col names
    # mismatch of data types
    # mismatch of sku - removed "-" and 
 
 
## Check if headers match, show mismatches
set(df1.columns) - set(df2.columns), set(df2.columns) - set(df1.columns)

## Standardize column names -- make snapshot_2 match snapshot_1 
df2.rename(columns={"product_name": "name", "qty": "quantity", "warehouse": "location", "updated_at": "last_counted"}, inplace=True)

##Confirm headers match exactly
df1.columns.equals(df2.columns)  

  
##Understand data inputs, look at first and last 5 rows 
for df in dflist:
    df.head(), df.tail()

#count missing values for all columns
for df in dflist:
    df.isna().sum()
    ## none found
    
#count duplicated records
for df in dflist:
    df.duplicated().sum()
    ## none found



#check for quality issues in data entry


#general clean
for df in dflist:
    for col in df.select_dtypes(include="string"):
        df[col] = df[col].apply(
            lambda x: x.lower().strip() if isinstance(x, str) else x
        )
        
##Standardize data types (only one mismatch found)
for df in dflist:
    df["quantity"] = df["quantity"].astype(int)

for df in dflist:
    df["last_counted"] = pd.to_datetime(
        df["last_counted"],
        format="mixed",
        errors="coerce"
    )

#fix sku format remove "-" for easier handling
for df in dflist:
    df["sku"] = df["sku"].str.upper().str.replace("-", "") 

#loop through all cols in all dfs to force na to 0
for df in dflist:
    for col in df.columns:
        df[col].fillna(0)

#confirm changes were successful
for df in dflist:
    df.info()
    

############
### RECONCILE
############

##Identify:
   # 1 - Items present in both snapshots (and whether quantities changed)
   # 2 - Items only in snapshot 1 (removed/sold out)
   # 3 - Items only in snapshot 2 (newly added)
   # 4 - Any data quality issues worth flagging

merged = df1.merge(
    df2,
    on="sku",
    how="outer",
    suffixes=("_1", "_2"),
    indicator=True
)

# Changed
common = merged[merged["_merge"] == "both"]
common["qty_diff"] = (
     common["quantity_1"]-common["quantity_2"]
)

# Added
added = merged[merged["_merge"] == "right_only"]

# Removed
removed = merged[merged["_merge"] == "left_only"]


common.to_csv("common.csv", index=False)
added.to_csv("added.csv", index=False)
removed.to_csv("removed.csv", index=False)



    
    
### ---------------- ASSUMPTIONS ---------------- ###
### Assume key is sku
### 
### 
### --------------------------------------------- ###



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