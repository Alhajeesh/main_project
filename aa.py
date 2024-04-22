re=[{'product_id': 5, 'orderdetails_id': 3, 'ordermaster_id': 1, 'quantity': '2', 'amount': '30', 'orderstatus': 'pending', 'stock_id': 4, 'stock_quantity': '3', 'date_time': '2023-10-31'}, {'product_id': 8, 'orderdetails_id': 1, 'ordermaster_id': 1, 'quantity': '2', 'amount': '200', 'orderstatus': 'pending', 'stock_id': 7, 'stock_quantity': '15', 'date_time': '2023-11-03'}, {'product_id': 9, 'orderdetails_id': 2, 'ordermaster_id': 1, 'quantity': '2', 'amount': '240', 'orderstatus': 'pending', 'stock_id': 8, 'stock_quantity': '15', 'date_time': '2023-11-03'}]

for item in re:
    # item is a dictionary, and you can access its key-value pairs
    for key, value in item.items():
        print(f'{key}: {value}')

