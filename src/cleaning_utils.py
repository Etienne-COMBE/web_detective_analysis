import pandas as pd

def imports_csv(type, files):
    dfs = []
    for file in files:
        dfs.append(pd.read_csv(f'../data/{type}/{file}.csv'))
    return dfs

def check_columns(df):
    cols = []
    for col in df.columns:
        if df[col].count() < len(df):
            cols.append(col)
    if len(cols) == 0:
        print('No missing values in the dataframe')
        return
    print('Missing values in these columns:')
    for col in cols:
        print(col, 'with', len(df)-col.count(), 'missing values')
    return

def cleaning_global(clients, sales, products):
    trash_products = products[products['id_prod'] == 'T_0']
    cleaned_products = products.drop(trash_products.index)

    trash_sales = sales[sales['id_prod'] == 'T_0']
    cleaned_sales = sales.drop(trash_sales.index)

    trash_clients = clients[(clients['client_id'] == 'ct_0') | (clients['client_id'] == 'ct_1')]
    cleaned_clients = clients.drop(trash_clients.index)

    return  cleaned_clients, cleaned_sales, cleaned_products

def merging(clients, products, sales):
    fusion_by_clients_join = pd.merge(left = clients, right = sales, on = 'client_id')
    fusion_by_clients = pd.merge(left = fusion_by_clients_join, right = products, on = 'id_prod')
    
    fusion_by_products_join = pd.merge(left = products, right = sales, on = 'id_prod')
    fusion_by_products = pd.merge(left = fusion_by_products_join, right = clients, on = 'client_id')
    return fusion_by_clients, fusion_by_products

def export_csv(dfs, type, files):
    for i in range(len(dfs)):
        dfs[i].to_csv(f'../data/{type}/{files[i]}.csv', index = False)