from datetime import datetime

import mysql.connector

Connection = mysql.connector.connect(host="localhost", user="root", password="!password")
Cursor = Connection.cursor(buffered=True)
# print("No of Record Fetched:" + str(Cursor.rowcount))
# print("Results: " + str(returned_rows))


current_user_staff_id = 0
current_user_staff_name = ''


def db_cud_query(query, param):  # Create, Update, Delete: Connection.commit()
    Connection.connect()
    Cursor.execute("use project_v2")
    try:
        Cursor.execute(query, param)
        Connection.commit()

    except (mysql.connector.DatabaseError, mysql.connector.OperationalError) as e:  # catch the error
        print('***', e, '***')

def db_r_query(query, param):  # Read: Connection.commit()
    Connection.connect()
    Cursor.execute("use project_v2")
    try:
        Cursor.execute(query, param)
        returned_rows = Cursor.fetchall()
        Connection.close()
        return Cursor.rowcount, returned_rows

    except (mysql.connector.DatabaseError, mysql.connector.OperationalError) as e:  # catch the error
        print('***', e, '***')
        return 0, []


def sexy_customer_display(raw_list):
    customer_columns = ['Customer ID    ', 'Customer name  ', 'Address        ',
                        'Region         ', 'Unit no.       ', 'Postal code    ',
                        'Phone          ']
    for item in range(1, len(raw_list[0])):
        print(customer_columns[item], raw_list[0][item])


def sexy_product_display(raw_list):
    product_columns = ['Product ID   ', 'Category     ', 'Item         ', 'Product code ',
                       'Unit price   ', 'Stock level  ']
    for item in range(1, len(raw_list[0])):
        print(product_columns[item], raw_list[0][item])


def sexy_staff_display(raw_list):
    staff_columns = ['Staff ID   ', 'Staff name ', 'Role       ', 'NRIC       ',
                     'Username   ', 'Password   ']
    for item in range(1, len(raw_list[0])):
        print(staff_columns[item], raw_list[0][item])


def sexy_order_display(order_id, role):
    if role == 'merchandiser':
        returned_rows, customer_order = db_r_query('SELECT * FROM customer_order WHERE OrderID=%s', [order_id])
        returned_rows2, order_product = db_r_query('SELECT * FROM order_product WHERE OrderID=%s', [order_id])
        returned_rows3, order_deliver = db_r_query('SELECT * FROM order_deliver WHERE OrderID=%s', [order_id])
        returned_rows4, order_pack = db_r_query('SELECT * FROM order_pack WHERE OrderID=%s', [order_id])
        returned_rows5, order_merchandise = db_r_query('SELECT * FROM order_merchandise WHERE OrderID=%s', [order_id])

        if not customer_order or not order_product or not order_deliver or not order_pack or not order_merchandise:  # where data = []
            print('\n*** No matching order ***')
            merchandiser_order_menu()

        order_by_name = order_merchandise[0][2]
        order_date = customer_order[0][1]
        customer_id = customer_order[0][2]
        # order_product handled
        packing_status = order_pack[0][3]
        packer_name = order_pack[0][2]
        pack_date = order_pack[0][4]
        delivery_status = order_deliver[0][3]
        deliverer_name = order_deliver[0][2]
        delivery_date = order_deliver[0][4]

    else:  # if manager/packer/deliverer
        returned_rows, order_info = db_r_query('SELECT * FROM order_info WHERE OrderID=%s', [order_id])
        returned_rows2, order_product = db_r_query('SELECT * FROM order_product_info WHERE OrderID=%s', [order_id])

        if not order_product or not order_info:  # where data = []
            print('\n*** No matching order ***')
            if role == 'manager':
                manager_menu()
            elif role == 'packer':
                packer_menu()

        order_by_name = order_info[0][-4]
        order_date = order_info[0][1]
        customer_id = order_info[0][2]
        # order_product handled
        packing_status = order_info[0][3]
        packer_name = order_info[0][6]
        pack_date = order_info[0][7]
        delivery_status = order_info[0][4]
        deliverer_name = order_info[0][-7]
        delivery_date = order_info[0][-6]

    # merchandiser staff name
    print('\nOrder by             ' + str(order_by_name))

    # order date
    print('Order date           ' + str(order_date)[:10])

    # from customer id >get name + address + phone
    returned_rows, data = db_r_query("SELECT * FROM customer WHERE CustomerID=%s", [customer_id])
    print('Delivery customer    ' + str(data[0][1]) +
          '\nDelivery address     ' + str(data[0][2]) + ', ' + str(data[0][4]) + ', Singapore ' + str(data[0][5]) +
          '\nDelivery phone       ' + str(data[0][6]) +
          '\n-----------------------------------------------------------------------')

    total_cost = 0.00
    # from product id > get name + code + unit price
    print('Product          Product Code    Unit Psce      Quantity    Total'
          '\n-----------------------------------------------------------------------')
    for index in range(0, len(order_product)):
        total_cost += float(order_product[index][3])
        returned_rows2, data2 = db_r_query("SELECT * FROM product WHERE ProductID=%s", [order_product[index][1]])
        print('{0: <17}'.format(data2[0][2]) + '{0: <16}'.format(data2[0][3]) + '${0: <15}'.format(data2[0][4]) +
              '{0: <12}'.format(order_product[index][2]) + '${0: <10}'.format(order_product[index][3]))

    # order revenue
    print('-----------------------------------------------------------------------'
          '\n{0: >68}'.format('$' + "{:.2f}".format(total_cost)))

    # packing status(additional) + packer staff name
    if str(packing_status) == 'Pending':
        print('Packing status       Pending')
    else:
        print('Packing status       Fulfilled')
        print('Packed by            ' + str(packer_name))
        print('Pack date            ' + str(pack_date)[:10])

    # delivery status(additional) + deliverer staff name + delivery date
    if str(delivery_status) == 'Pending':
        print('Delivery status      Pending')
    else:
        print('Delivery status      Fulfilled')
        print('Delivered by         ' + str(deliverer_name))
        print('Delivery date        ' + str(delivery_date)[:10])


def admin_menu():
    print('\nAdmin Menu\n===================='  # Welcome Myles
          '\n1. Manager mode\n2. Merchandiser mode\n3. Packer mode\n4. Deliverer mode\n5. Log out'
          '\n====================')
    admin_action = input("Enter Selection:")
    if admin_action == '1':
        manager_menu()
    elif admin_action == '2':
        merchandiser_menu()
    elif admin_action == '3':
        packer_menu()
    elif admin_action == '4':
        deliverer_menu()
    elif admin_action == '5':
        login()
    else:
        admin_menu()


def manager_customer_menu():
    print('\nManager Menu - Manage Customer (Outlets)\n===================='
          '\n1. Add customer\n2. Update customer details\n3. Remove customer\n4. Retrieve customer details\n5. Back\n====================')

    manager_customer_action = input("Enter Selection:")

    if manager_customer_action == '1':
        customer_name_create = input('\nEnter customer name:')
        customer_address_create = input('Enter customer address:')
        customer_region_create = input('Enter customer region:')
        customer_unit_num_create = input('Enter customer unit no.:')
        customer_postal_code_create = input('Enter customer postal code:')
        customer_phone_create = input('Enter customer phone no.:')

        db_cud_query(
            "INSERT INTO customer(Customer_Name, Customer_Address, Region, Unit_Number, Postal_Code, Customer_Phone) VALUES (%s,%s,%s,%s,%s,%s)",
            [customer_name_create, customer_address_create, customer_region_create,
             customer_unit_num_create, customer_postal_code_create, customer_phone_create]
            )
        returned_rows, data = db_r_query("SELECT * FROM customer WHERE Customer_Phone=%s", [customer_phone_create])
        if not data:
            print('\n*** Failed to add customer ***')
        else:
            print('\n*** Customer added ***')
        input('\n*** Enter any key to go back ***')
        manager_customer_menu()

    elif manager_customer_action == '2':
        customer_id_update = input('\nEnter Customer ID:')

        returned_rows, data = db_r_query('SELECT * FROM customer WHERE CustomerID=%s', [customer_id_update])

        if not data:  # where data = []
            print('\n*** No matching customer ***')
            manager_customer_menu()

        customer_name_update = data[0][1]
        address_update = data[0][2]
        region_update = data[0][3]
        unit_num_update = data[0][4]
        postal_code_update = data[0][5]
        phone_update = data[0][6]

        def manager_update_customer_menu(new_customer_name, new_address, new_region, new_unit_num, new_postal_code, new_phone):
            print('\nManager Menu - Manage Customer - Update Customer Details\n============================'
                  '\n1. Update customer name  ', new_customer_name,
                  '\n2. Update address        ', new_address,
                  '\n3. Update region         ', new_region,
                  '\n4. Update unit no.       ', new_unit_num,
                  '\n5. Update postal code    ', new_postal_code,
                  '\n6. Update phone no.      ', new_phone,
                  '\n7. Confirm Update\n8. Back\n============================')

            manager_update_customer_action = input("Enter Selection:")

            if manager_update_customer_action == '1':
                new_customer_name = input('Enter new customer name:')
            elif manager_update_customer_action == '2':
                new_address = input('Enter new address:')
            elif manager_update_customer_action == '3':
                new_region = input('Enter new region:')
            elif manager_update_customer_action == '4':
                new_unit_num = input('Enter new unit no.:')
            elif manager_update_customer_action == '5':
                new_postal_code = input('Enter new postal code:')
            elif manager_update_customer_action == '6':
                new_phone = input('Enter new phone no.:')
            elif manager_update_customer_action == '7':
                db_cud_query(
                    "UPDATE customer SET Customer_Name=%s, Customer_Address=%s, Region=%s, Unit_number=%s, Postal_Code=%s, Customer_Phone=%s WHERE CustomerID=%s",
                    [new_customer_name, new_address, new_region, new_unit_num, new_postal_code, new_phone, int(customer_id_update)])

                print('\n*** Customer details updated ***')

                input('\n*** Enter any key to go back ***')
                manager_customer_menu()
            else:
                manager_customer_menu()
            manager_update_customer_menu(new_customer_name, new_address, new_region, new_unit_num, new_postal_code, new_phone)

        manager_update_customer_menu(customer_name_update, address_update, region_update,
                                     unit_num_update, postal_code_update, phone_update)

    elif manager_customer_action == '3':
        customer_id_delete = input('\nEnter Customer ID:')
        db_cud_query("DELETE FROM customer WHERE CustomerID=%s", [customer_id_delete])
        print('\n*** Customer removed ***')
        input('\n*** Enter any key to go back ***')
        manager_customer_menu()

    elif manager_customer_action == '4':
        customer_id_retrieve = input('\nEnter Customer ID:')
        returned_rows, data = db_r_query('SELECT * FROM customer WHERE CustomerID=%s', [customer_id_retrieve])
        if not data:  # where data = []
            print('\n*** No matching customer ***')
        else:
            print('')
            sexy_customer_display(data)
        input('\n*** Enter any key to go back ***')
        manager_customer_menu()

    elif manager_customer_action == '5':
        manager_menu()

    else:
        manager_customer_menu()


def manager_staff_menu():
    print('\nManager Menu - Manage staff\n===================='
          '\n1. Add staff\n2. Update staff details\n3. Remove staff\n4. Retrieve staff details\n5. Back\n====================')

    manager_staff_action = input("Enter Selection:")

    if manager_staff_action == '1':
        staff_name_create = input('\nEnter staff name:')
        role_create = input('Enter staff role:')
        nric_create = input('Enter staff NRIC:')
        username_create = input('Enter staff username:')
        password_create = input('Enter staff password:')
        db_cud_query("INSERT INTO staff(Staff_Name, Role, NRIC, Username, Password) VALUES (%s,%s,%s,%s,%s)",
                     [staff_name_create, role_create, nric_create, username_create, password_create])
        returned_rows, data = db_r_query("SELECT * FROM staff WHERE NRIC=%s", [nric_create])
        if not data:
            print('\n*** Failed to add staff ***')
        else:
            print('\n*** Staff added ***')
        input('\n*** Enter any key to go back ***')
        manager_staff_menu()

    elif manager_staff_action == '2':
        staff_id_update = input('\nEnter Staff ID:')

        returned_rows, data = db_r_query('SELECT * FROM staff WHERE StaffID=%s', [staff_id_update])

        if not data:  # where data = []
            print('\n*** No matching staff ***')
            manager_staff_menu()

        staff_name_update = data[0][1]
        role_update = data[0][2]
        nric_update = data[0][3]
        username_update = data[0][4]
        password_update = data[0][5]

        def manager_update_staff_menu(new_staff_name, new_role, new_nric, new_username, new_password):
            print('\nManager Menu - Manage Staff - Update Staff Details\n============================'
                  '\n1. Update staff name      ', new_staff_name,
                  '\n2. Update role            ', new_role,
                  '\n3. Update NRIC            ', new_nric,
                  '\n4. Update staff username  ', new_username,
                  '\n5. Update staff password  ', new_password,
                  '\n6. Confirm Update\n7. Back\n============================')

            manager_update_staff_action = input("Enter Selection:")

            if manager_update_staff_action == '1':
                new_staff_name = input('Enter new staff name:')
            elif manager_update_staff_action == '2':
                new_role = input('Enter new staff role:')
            elif manager_update_staff_action == '3':
                new_nric = input('Enter new staff NRIC:')
            elif manager_update_staff_action == '4':
                new_username = input('Enter new username:')
            elif manager_update_staff_action == '5':
                new_password = input('Enter new password:')
            elif manager_update_staff_action == '6':
                # staff
                db_cud_query(
                    "UPDATE staff SET Staff_Name=%s, Role=%s, NRIC=%s, Username=%s, Password=%s WHERE StaffID=%s",
                    [new_staff_name, new_role, new_nric, new_username, new_password, staff_id_update])

                # order_pack
                returned_rows2, data2 = db_r_query("SELECT * FROM order_pack WHERE Packer_StaffID=%s", [staff_id_update])
                if data2:
                    db_cud_query("UPDATE order_pack SET Packer_Name=%s WHERE Packer_StaffID=%s", [new_staff_name, staff_id_update])

                # order_deliver
                returned_rows3, data3 = db_r_query("SELECT * FROM order_deliver WHERE Deliverer_StaffID=%s", [staff_id_update])
                if data3:
                    db_cud_query("UPDATE order_deliver SET Deliverer_Name=%s WHERE Deliverer_StaffID=%s", [new_staff_name, staff_id_update])

                # order_merchandiser
                returned_rows4, data4 = db_r_query("SELECT * FROM order_merchandise WHERE Merchandiser_StaffID=%s", [staff_id_update])
                if data4:
                    db_cud_query("UPDATE order_merchandise SET Merchandiser_Name=%s WHERE Merchandiser_StaffID=%s", [new_staff_name, staff_id_update])

                print('\n*** Staff details updated ***')

                input('\n*** Enter any key to go back ***')
                manager_staff_menu()
            else:
                manager_staff_menu()

            manager_update_staff_menu(new_staff_name, new_role, new_nric, new_username, new_password)

        manager_update_staff_menu(staff_name_update, role_update, nric_update, username_update, password_update)

    elif manager_staff_action == '3':
        staff_id_delete = input('\nEnter Staff ID:')
        db_cud_query("DELETE FROM staff WHERE StaffID=%s", [staff_id_delete])
        print('\n*** Staff removed ***')
        input('\n*** Enter any key to go back ***')
        manager_staff_menu()

    elif manager_staff_action == '4':
        staff_id_retrieve = input('\nEnter Staff ID:')
        returned_rows, data = db_r_query('SELECT * FROM staff WHERE StaffID=%s', [staff_id_retrieve])
        if not data:  # where data = []
            print('\n*** No matching staff ***')
        else:
            print('')
            sexy_staff_display(data)
        input('\n*** Enter any key to go back ***')
        manager_staff_menu()

    elif manager_staff_action == '5':
        manager_menu()

    else:
        manager_staff_menu()


def manager_product_menu():
    print('\nManager Menu - Manage products\n===================='
          '\n1. Add product\n2. Update product details\n3. Remove product\n4. Retrieve product details\n5. Back\n====================')

    manager_product_action = input("Enter Selection:")

    if manager_product_action == '1':
        category_create = input('\nEnter product category:')
        item_create = input('Enter product item name:')
        product_code_create = input('Enter product code:')
        unit_price_create = input('Enter unit price:')
        stock_level_create = input('Enter product quantity:')
        db_cud_query(
            "INSERT INTO product(Category, Item, Product_Code, Unit_Price, Stock_level) VALUES (%s,%s,%s,%s,%s)",
            [category_create, item_create, product_code_create, unit_price_create, stock_level_create])
        returned_rows, data = db_r_query("SELECT * FROM product WHERE Product_Code=%s", [product_code_create])
        if not data:
            print('\n*** Failed to add product ***')
        else:
            print('\n*** Product added ***')
        input('\n*** Enter any key to go back ***')
        manager_product_menu()

    elif manager_product_action == '2':
        product_id_update = input('\nEnter Product ID:')

        returned_rows, data = db_r_query('SELECT * FROM product WHERE ProductID=%s', [product_id_update])

        if not data:  # where data = []
            print('\n*** No matching product ***')
            manager_product_menu()

        category_update = data[0][1]
        item_name_update = data[0][2]
        product_code_update = data[0][3]
        unit_price_update = float(data[0][4])
        stock_level_update = data[0][5]

        def manager_update_product_menu(new_category, new_item_name, new_product_code, new_unit_price, new_stock_level):
            print('\nManager Menu - Manage products - Update product\n============================'
                  '\n1. Update product category    ', new_category,
                  '\n2. Update item name           ', new_item_name,
                  '\n3. Update product code        ', new_product_code,
                  '\n4. Update unit selling price  ', new_unit_price,
                  '\n5. Update quantity            ', new_stock_level,
                  '\n6. Confirm Update\n7. Back\n============================')

            manager_update_product_action = input("Enter Selection:")

            if manager_update_product_action == '1':
                new_category = input('Enter new category:')
            elif manager_update_product_action == '2':
                new_item_name = input('Enter new item name:')
            elif manager_update_product_action == '3':
                new_product_code = input('Enter new product code:')
            elif manager_update_product_action == '4':
                new_unit_price = input('Enter new unit price:')
            elif manager_update_product_action == '5':
                new_stock_level = input('Enter new quantity:')
            elif manager_update_product_action == '6':
                db_cud_query(
                    "UPDATE product SET Category=%s, Item=%s, Product_Code=%s, Unit_Price=%s, Stock_level=%s WHERE ProductID=%s",
                    [new_category, new_item_name, new_product_code, new_unit_price, new_stock_level, product_id_update])

                print('\n*** Product updated ***')

                input('\n*** Enter any key to go back ***')
                manager_product_menu()
            else:
                manager_product_menu()

            manager_update_product_menu(new_category, new_item_name, new_product_code, new_unit_price, new_stock_level)

        manager_update_product_menu(category_update, item_name_update, product_code_update, unit_price_update,
                                    stock_level_update)

    elif manager_product_action == '3':
        product_code_delete = input('\nEnter Product ID:')
        db_cud_query("DELETE FROM product WHERE ProductID=%s", [product_code_delete])
        print('\n*** Product removed ***')
        input('\n*** Enter any key to go back ***')
        manager_product_menu()

    elif manager_product_action == '4':
        product_code_retrieve = input('\nEnter Product ID:')
        returned_rows, data = db_r_query('SELECT * FROM product WHERE ProductID=%s', [product_code_retrieve])
        if not data:  # where data = []
            print('\n*** No matching product ***')
        else:
            print('')
            sexy_product_display(data)
        input('\n*** Enter any key to go back ***')
        manager_product_menu()

    elif manager_product_action == '5':
        manager_menu()

    else:
        manager_product_menu()


def merchandiser_order_menu():
    print('\nMerchandiser Menu - Manage customer order\n===================='
          '\n1. Add order\n2. Update order details\n3. Remove order\n4. Retrieve order details\n5. Back\n====================')

    merchandiser_order_action = input("Enter Selection:")

    if merchandiser_order_action == '1':
        customer_id_create = input('\nEnter customer ID:')

        returned_rows2, data2 = db_r_query('SELECT * FROM customer WHERE CustomerID=%s', [customer_id_create])

        if not data2:
            print('*** No matching customer ***')
            input('\n*** Enter any key to go back ***')
            merchandiser_order_menu()

        order_product_id_list = []
        order_product_item_name_list = []
        order_product_quantity_list = []
        order_product_revenue_list = []
        total_cost = 0.00

        def merchandiser_order_product_menu(id_list, item_name_list, quantity_list, revenue_list, cost):
            product_id_create = input('\nEnter product ID:')
            returned_rows6, data3 = db_r_query('SELECT * FROM product WHERE ProductID=%s', [product_id_create])
            if not data3:
                print('*** No matching product ***')
                input('\n*** Enter any key to go back ***')
                merchandiser_order_product_menu(id_list, item_name_list, quantity_list, revenue_list, cost)
            product_quantity_create = input('Enter product quantity:')
            try:  # ensure quantity is int for calculation later on
                int(product_quantity_create)
            except ValueError:
                print('*** Invalid product quantity ***')
                input('\n*** Enter any key to go back ***')
                merchandiser_order_product_menu(id_list, item_name_list, quantity_list, revenue_list, cost)

            only_this_order_cost = float(data3[0][4]) * float(product_quantity_create)
            cost += only_this_order_cost

            if product_id_create in id_list:  # if adding another product w/ same product id as previous order
                selected_index_item = id_list.index(product_id_create)
                quantity_list[selected_index_item] = str(
                    int(quantity_list[selected_index_item]) + int(product_quantity_create))
                revenue_list[selected_index_item] = str(float(revenue_list[selected_index_item]) + only_this_order_cost)
            else:
                id_list.append(str(data3[0][0]))
                item_name_list.append(str(data3[0][2]))
                quantity_list.append(str(product_quantity_create))
                revenue_list.append(str(only_this_order_cost))

            print('\n====================')
            for item2 in id_list:
                print(quantity_list[id_list.index(item2)] + '  ' + item_name_list[id_list.index(item2)])
            print('\nTotal: $' + "{:.2f}".format(cost))  # show 2dp
            print('====================')

            reorder_product = input('Add another product? (Y/N):')
            if reorder_product == 'Y':
                merchandiser_order_product_menu(id_list, item_name_list, quantity_list, revenue_list, cost)
            if reorder_product == 'N':

                order_date_create = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # customer_order table
                db_cud_query("INSERT INTO customer_order(Order_Date, CustomerID, Revenue) VALUES (%s,%s,%s)",
                             [order_date_create, customer_id_create, cost])

                # retrieve order ID using Super Key unique identification for the next few tables
                returned_rows7, data4 = db_r_query(
                    'SELECT * FROM customer_order WHERE Order_Date=%s AND CustomerID=%s AND Revenue=%s',
                    [order_date_create, customer_id_create, cost])
                order_id_create = data4[0][0]

                # order_product table + update stock lvl with: stock lvl -= quantity > Update stock lvl
                for item3 in id_list:
                    db_cud_query("UPDATE product SET Stock_Level=Stock_Level-%s WHERE ProductID=%s",
                                 [quantity_list[id_list.index(item3)], item3])

                    db_cud_query(
                        "INSERT INTO order_product(OrderID, ProductID, Product_Quantity, Product_Revenue) VALUES (%s,%s,%s,%s)",
                        [order_id_create, id_list[id_list.index(item3)], quantity_list[id_list.index(item3)],
                         revenue_list[id_list.index(item3)]])

                # order_deliver table
                db_cud_query("INSERT INTO order_deliver(OrderID, Delivery_Status) VALUES (%s,%s)",
                             [order_id_create, 'Pending'])

                # order_pack table
                db_cud_query("INSERT INTO order_pack(OrderID, Packing_Status) VALUES (%s,%s)",
                             [order_id_create, 'Pending'])

                # order_merchandise table
                db_cud_query(
                    "INSERT INTO order_merchandise(OrderID, Merchandiser_StaffID, Merchandiser_Name) VALUES (%s,%s,%s)",
                    [order_id_create, current_user_staff_id, current_user_staff_name])

                print('\n*** Order added ***')
                input('\n*** Enter any key to go back ***')
                merchandiser_order_menu()
            else:
                merchandiser_order_menu()

        merchandiser_order_product_menu(order_product_id_list, order_product_item_name_list,
                                        order_product_quantity_list, order_product_revenue_list, total_cost)

    if merchandiser_order_action == '2':
        order_id_update = input('\nEnter Order ID:')

        returned_rows, data = db_r_query('SELECT * FROM customer_order WHERE OrderID=%s', [order_id_update])
        returned_rows2, data2 = db_r_query('SELECT * FROM order_product WHERE OrderID=%s', [order_id_update])

        if not data or not data2:  # where data = []
            print('\n*** No matching order ***')
            merchandiser_order_menu()

        new_order_customer_id = data[0][2]
        removed_order_product_id_list = []
        new_order_product_id_list = []
        new_order_product_item_name_list = []
        new_order_product_quantity_list = []
        new_order_product_revenue_list = []

        for item in data2:
            new_order_product_id_list.append(str(item[1]))
            returned_rows3, data3 = db_r_query('SELECT * FROM product WHERE ProductID=%s', [item[1]])
            new_order_product_item_name_list.append(data3[0][2])
            new_order_product_quantity_list.append(str(item[2]))
            new_order_product_revenue_list.append(str(item[3]))

        # print(new_order_product_quantity_list)
        # print(new_order_product_revenue_list)

        def merchandiser_update_order_menu(customer_id, removed_id_list, id_list, item_list, quantity_list,
                                           revenue_list):
            print('\nMerchandiser Menu - Manage customer order - Update order details\n============================'
                  '\n1. Update customer ID:  ', customer_id,
                  '\n\nRemove product from order:')
            for item2 in item_list:
                print(str(item_list.index(item2) + 2) + '. ' + str(quantity_list[item_list.index(item2)]) + ' ' + str(
                    item2))
            print('\n' + str(len(item_list) + 2) + '. Add product to order'
                                                   '\n' + str(len(item_list) + 3) + '. Confirm update'
                                                                                    '\n' + str(
                len(item_list) + 4) + '. Back'
                                      '\n============================')

            parsed = False  # force int input from user
            merchandiser_update_order_action = 0
            while not parsed:
                merchandiser_update_order_action = input("Enter Selection:")
                try:
                    int(merchandiser_update_order_action)
                    parsed = True
                except ValueError:
                    pass
            # change customer id
            if merchandiser_update_order_action == '1':
                customer_id = input('Enter new customer ID:')
                returned_rows6, data6 = db_r_query('SELECT * FROM customer WHERE CustomerID=%s', [customer_id])
                if not data6:  # where data = []
                    print('\n*** No matching customer ***')
                    merchandiser_order_menu()
                merchandiser_update_order_menu(customer_id, removed_id_list, id_list, item_list, quantity_list,
                                               revenue_list)

            # delete product
            if 1 < int(merchandiser_update_order_action) < len(item_list) + 2:

                selected_index = int(merchandiser_update_order_action) - 2

                if not id_list[selected_index] in removed_id_list:
                    removed_id_list.append(id_list[selected_index])  # DELETE FROM
                id_list.remove(id_list[selected_index])  # INSERT INTO
                item_list.remove(item_list[selected_index])
                quantity_list.remove(quantity_list[selected_index])
                revenue_list.remove(revenue_list[selected_index])

                merchandiser_update_order_menu(customer_id, removed_id_list, id_list, item_list, quantity_list,
                                               revenue_list)

            # add product
            if int(merchandiser_update_order_action) == len(item_list) + 2:
                product_id_create = input('Enter product ID:')

                returned_rows7, data7 = db_r_query('SELECT * FROM product WHERE ProductID=%s', [product_id_create])

                if not data7:  # where data = []
                    print('\n*** No matching product ***')
                    merchandiser_update_order_menu(customer_id, removed_id_list, id_list, item_list, quantity_list,
                                                   revenue_list)

                parsed = False  # force int input to user
                product_quantity_create = 0
                while not parsed:
                    product_quantity_create = input('Enter product quantity:')
                    try:
                        int(product_quantity_create)
                        parsed = True
                    except ValueError:
                        pass

                product_revenue_create = float(data7[0][4]) * float(
                    product_quantity_create)  # $$$ = unit price * quantity

                if product_id_create in id_list:
                    selected_index2 = id_list.index(product_id_create)
                    quantity_list[selected_index2] = str(
                        int(quantity_list[selected_index2]) + int(product_quantity_create))
                    revenue_list[selected_index2] = str(float(revenue_list[selected_index2]) + product_revenue_create)
                else:
                    id_list.append(product_id_create)
                    item_list.append(data7[0][2])
                    quantity_list.append(product_quantity_create)
                    revenue_list.append(str(product_revenue_create))

                merchandiser_update_order_menu(customer_id, removed_id_list, id_list, item_list, quantity_list,
                                               revenue_list)

            # UPDATE SET customerid, INSERT INTO/DELETE FROM order product id
            if int(merchandiser_update_order_action) == len(item_list) + 3:
                db_cud_query("UPDATE customer_order SET CustomerID=%s WHERE OrderID=%s",
                             [customer_id, order_id_update])

                # restore stock lvls of deleted product > reset product_order
                returned_rows8, data8 = db_r_query('SELECT * FROM order_product WHERE OrderID=%s', [order_id_update])
                for item5 in data8:
                    db_cud_query("UPDATE product SET Stock_Level=Stock_Level+%s WHERE ProductID=%s",
                                 [item5[2], item5[1]])

                db_cud_query("DELETE FROM order_product WHERE OrderID=%s", [order_id_update])

                # refill the product order with new changes
                for item3 in id_list:
                    db_cud_query(
                        "INSERT INTO order_product(OrderID, ProductID, Product_Quantity, Product_Revenue) VALUES (%s,%s,%s,%s)",
                        [order_id_update, item3, quantity_list[id_list.index(item3)],
                         revenue_list[id_list.index(item3)]])

                # secondary update: update order total revenue in relation to product revenue change
                new_order_total_revenue = 0.00
                for item4 in revenue_list:
                    new_order_total_revenue += float(item4)
                db_cud_query("UPDATE customer_order SET Revenue=%s WHERE OrderID=%s",
                             [new_order_total_revenue, order_id_update])

                # secondary update: update product stock lvl in relation to quantity change
                for item6 in id_list:
                    db_cud_query("UPDATE product SET Stock_Level=Stock_Level-%s WHERE ProductID=%s",
                                 [quantity_list[id_list.index(item6)], item6])

                print('\n*** Order updated ***')
                input('\n*** Enter any key to go back ***')
                merchandiser_order_menu()

            # back to menu
            if int(merchandiser_update_order_action) == len(item_list) + 4:
                merchandiser_order_menu()

            # no change
            else:
                merchandiser_update_order_menu(customer_id, removed_id_list, id_list, item_list, quantity_list,
                                               revenue_list)

        merchandiser_update_order_menu(new_order_customer_id, removed_order_product_id_list, new_order_product_id_list,
                                       new_order_product_item_name_list, new_order_product_quantity_list,
                                       new_order_product_revenue_list)

    if merchandiser_order_action == '3':
        order_id_delete = input('\nEnter Order ID:')

        # restore stock lvl of products
        returned_rows, data = db_r_query('SELECT * FROM order_product WHERE OrderID=%s', [order_id_delete])
        for item in data:
            db_cud_query("UPDATE product SET Stock_Level=Stock_Level+%s WHERE ProductID=%s",
                         [item[2], item[1]])

        db_cud_query("DELETE FROM customer_order WHERE OrderID=%s", [order_id_delete])
        print('\n*** Order removed ***')
        input('\n*** Enter any key to go back ***')
        merchandiser_order_menu()

    if merchandiser_order_action == '4':
        order_id_retrieve = input('\nEnter Order ID:')
        sexy_order_display(order_id_retrieve, 'merchandiser')
        input('\n*** Enter any key to go back ***')
        merchandiser_order_menu()

    if merchandiser_order_action == '5':
        merchandiser_menu()
    merchandiser_order_menu()


def manager_sales_menu():
    print('\nManager Menu - View Sales\n===================='  # Welcome Myles
          '\n1. By product\n2. By product category\n3. By customer'
          '\n4. By region\n5. Back'
          '\n====================')

    manager_sales_action = input("Enter Selection:")

    if manager_sales_action == '1':
        product_id_sales = input("\nEnter product id:")
        returned_rows, data = db_r_query('SELECT SUM(Product_Revenue) FROM order_info WHERE ProductID=%s',
                                         [product_id_sales])
        if str(data[0][0]) == 'None':
            print('\n*** No matching product in orders ***')
        else:
            print('\nSales made: $' + str(data[0][0]))
        input('\n*** Enter any key to go back ***')
        manager_sales_menu()

    if manager_sales_action == '2':
        product_category_sales = input("\nEnter product category:")
        returned_rows2, data2 = db_r_query('SELECT SUM(Product_Revenue) FROM product_sales_info WHERE Category=%s',
                                           [product_category_sales])
        if str(data2[0][0]) == 'None':
            print('\n*** No matching product category in orders ***')
        else:
            print('\nSales made: $' + str(data2[0][0]))
        input('\n*** Enter any key to go back ***')
        manager_sales_menu()

    if manager_sales_action == '3':
        customer_id_sales = input("\nEnter customer id:")
        returned_rows3, data3 = db_r_query('SELECT SUM(Revenue) FROM customer_sales_info WHERE CustomerID=%s',
                                           [customer_id_sales])
        if str(data3[0][0]) == 'None':
            print('\n*** No matching customer in orders ***')
        else:
            print('\nSales made: $' + str(data3[0][0]))
        input('\n*** Enter any key to go back ***')
        manager_sales_menu()

    if manager_sales_action == '4':
        customer_region_sales = input("\nEnter region:")
        returned_rows4, data4 = db_r_query('SELECT SUM(Revenue) FROM customer_sales_info WHERE Region=%s',
                                           [customer_region_sales])
        if str(data4[0][0]) == 'None':
            print('\n*** No matching region in orders ***')
        else:
            print('\nSales made: $' + str(data4[0][0]))
        input('\n*** Enter any key to go back ***')
        manager_sales_menu()

    if manager_sales_action == '5':
        manager_menu()
    manager_sales_menu()


def manager_menu():
    print('\nManager Menu\n===================='  # Welcome Myles
          '\n1. Manage products\n2. Manage staff\n3. Manage outlets'
          '\n4. View sales\n5. View order details by merchandiser\n6. View order details by outlet'
          '\n7. View order fulfilment details by packer & deliverer\n8. Log out'
          '\n====================')

    manager_action = input("Enter Selection:")

    if manager_action == '1':
        manager_product_menu()
    if manager_action == '2':
        manager_staff_menu()
    if manager_action == '3':
        manager_customer_menu()
    if manager_action == '4':
        manager_sales_menu()
    if manager_action == '5':
        merchandiser_id_retrieve = input('\nEnter merchandiser id:')
        returned_rows, data = db_r_query('SELECT DISTINCT OrderID FROM order_info WHERE Merchandiser_StaffID=%s',
                                         [merchandiser_id_retrieve])
        if not data:
            print('*** No matching merchandiser in orders ***')
        else:
            print('\n' + str(returned_rows) + ' orders found'
                                              '\n====================')
            for item in data:
                print(item[0])
            print('====================')
            order_id_retrieve = input('Enter order id selection:')
            sexy_order_display(order_id_retrieve, 'manager')
        input('\n*** Enter any key to go back ***')
        manager_menu()

    if manager_action == '6':
        customer_id_retrieve = input('\nEnter customer id:')
        returned_rows, data = db_r_query('SELECT DISTINCT OrderID FROM order_info WHERE CustomerID=%s',
                                         [customer_id_retrieve])
        if not data:
            print('*** No matching customer in orders ***')
        else:
            print('\n' + str(returned_rows) + ' orders found'
                                              '\n====================')
            for item in data:
                print(item[0])
            print('====================')
            order_id_retrieve = input('Enter order id:')
            sexy_order_display(order_id_retrieve, 'manager')
        input('\n*** Enter any key to go back ***')
        manager_menu()

    if manager_action == '7':
        order_id_retrieve2 = input('\nEnter order id:')
        returned_rows, data = db_r_query('SELECT * FROM order_info WHERE OrderID=%s', [order_id_retrieve2])

        if not data:
            print('\n*** No matching order ***')
        else:
            packing_status = data[0][3]
            packer_name = data[0][6]
            pack_date = data[0][7]

            delivery_status = data[0][4]
            deliverer_name = data[0][9]
            delivery_date = data[0][10]

            if str(packing_status) == 'Pending':
                print('\nPacking status       Pending')
            else:
                print('\nPacking status       Fulfilled')
                print('Packed by            ' + str(packer_name))
                print('Pack date            ' + str(pack_date)[:10])

            if str(delivery_status) == 'Pending':
                print('Delivery status      Pending')
            else:
                print('Delivery status      Fulfilled')
                print('Delivered by         ' + str(deliverer_name))
                print('Delivery date        ' + str(delivery_date)[:10])

        input('\n*** Enter any key to go back ***')
        manager_menu()

    if manager_action == '8':
        login()
    manager_menu()


def merchandiser_menu():
    print('\nMerchandiser Menu\n===================='  # Welcome Myles
          '\n1. Manage customer order\n2. View product quantity\n3. View customer order fulfilment status'
          '\n4. Log out'
          '\n====================')

    merchandiser_action = input("Enter Selection:")

    if merchandiser_action == '1':
        merchandiser_order_menu()
    if merchandiser_action == '2':
        product_id_view = input('\nEnter Product ID:')
        returned_rows, data = db_r_query('SELECT * FROM product WHERE ProductID=%s', [product_id_view])
        if not data:
            print('\n*** No matching product ***')
        else:
            print('\nProduct quantity for ' + '{}'.format(data[0][2]) + ': ' + str(data[0][5]))
        input('\n*** Enter any key to go back ***')
        merchandiser_menu()

    if merchandiser_action == '3':
        customer_id_view = input('\nEnter Customer ID:')
        order_id_view = input('\nEnter Order ID:')
        returned_rows2, data2 = db_r_query('SELECT * FROM order_info WHERE CustomerID=%s AND OrderID=%s',
                                           [customer_id_view, order_id_view])
        if not data2:
            print('\n*** No matching customer order ***')
        else:
            print('Packing Status: ', data2[0][3],
                  '\nDelivery Status ', data2[0][4])
        input('\n*** Enter any key to go back ***')
        merchandiser_menu()

    if merchandiser_action == '4':
        login()

    merchandiser_menu()


def packer_menu():
    print('\nPacker Menu\n===================='  # Welcome Myles
          '\n1. Retrieve unpacked orders\n2. Retrieve own packed orders\n3. Endorse customer order'
          '\n4. Log out'
          '\n====================')

    packer_action = input("Enter Selection:")

    if packer_action == '1':
        returned_rows, data = db_r_query('SELECT DISTINCT OrderID FROM order_info WHERE Packing_Status=%s', ['Pending'])
        if not data:
            print('\n*** No matching orders ***')
        else:
            print('\n' + str(returned_rows) + ' orders found'
                                              '\n====================')
            for item in data:
                print(item[0])
            print('====================')
            order_id_retrieve = input('Enter order id selection:')
            sexy_order_display(order_id_retrieve, 'packer')
        input('\n*** Enter any key to go back ***')
        packer_menu()

    if packer_action == '2':
        returned_rows2, data2 = db_r_query(
            'SELECT DISTINCT OrderID FROM order_info WHERE Packing_Status=%s AND Packer_StaffID=%s',
            ['Fulfilled', current_user_staff_id])
        if not data2:
            print('\n*** No matching orders ***')
        else:
            print('\n' + str(returned_rows2) + ' orders found'
                                               '\n====================')
            for item in data2:
                print(item[0])
            print('====================')
            order_id_retrieve = input('Enter order id selection:')
            sexy_order_display(order_id_retrieve, 'packer')
        input('\n*** Enter any key to go back ***')
        packer_menu()

    if packer_action == '3':
        order_id_endorse = input('\nEnter order id:')
        returned_rows3, data3 = db_r_query('SELECT * FROM order_pack WHERE OrderID=%s', [order_id_endorse])
        if not data3:
            print('\n*** No matching orders ***')
        else:
            order_endorse_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db_cud_query(
                "UPDATE order_pack SET Packer_StaffID=%s, Packer_Name=%s, Packing_Status=%s, Pack_Date=%s WHERE OrderID=%s",
                [current_user_staff_id, current_user_staff_name, 'Fulfilled', order_endorse_date, order_id_endorse])
            print('\n*** Order endorsed successfully ***')
        input('\n*** Enter any key to go back ***')
        packer_menu()

    if packer_action == '4':
        login()

    packer_menu()


def deliverer_menu():
    print('\nDeliverer Menu\n===================='  # Welcome Myles
          '\n1. Retrieve undelivered orders\n2. Retrieve own delivered orders\n3. Endorse customer order'
          '\n4. Log out'
          '\n====================')

    deliverer_action = input("Enter Selection:")

    if deliverer_action == '1':
        returned_rows, data = db_r_query('SELECT DISTINCT OrderID FROM order_info WHERE Delivery_Status=%s',
                                         ['Pending'])
        if not data:
            print('\n*** No matching orders ***')
        else:
            print('\n' + str(returned_rows) + ' orders found'
                                              '\n====================')
            for item in data:
                print(item[0])
            print('====================')
            order_id_retrieve = input('Enter order id selection:')
            sexy_order_display(order_id_retrieve, 'deliverer')
        input('\n*** Enter any key to go back ***')
        deliverer_menu()

    if deliverer_action == '2':
        returned_rows2, data2 = db_r_query(
            'SELECT DISTINCT OrderID FROM order_info WHERE Packing_Status=%s AND Deliverer_StaffID=%s',
            ['Fulfilled', current_user_staff_id])
        if not data2:
            print('\n*** No matching orders ***')
        else:
            print('\n' + str(returned_rows2) + ' orders found'
                                               '\n====================')
            for item in data2:
                print(item[0])
            print('====================')
            order_id_retrieve = input('Enter order id selection:')
            sexy_order_display(order_id_retrieve, 'deliverer')
        input('\n*** Enter any key to go back ***')
        deliverer_menu()

    if deliverer_action == '3':
        order_id_endorse = input('\nEnter order id:')
        returned_rows3, data3 = db_r_query('SELECT * FROM order_pack WHERE OrderID=%s', [order_id_endorse])
        if not data3:
            print('\n*** No matching orders ***')
        else:
            order_endorse_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db_cud_query(
                "UPDATE order_deliver SET Deliverer_StaffID=%s, Deliverer_Name=%s, Delivery_Status=%s, Delivery_Date=%s WHERE OrderID=%s",
                [current_user_staff_id, current_user_staff_name, 'Fulfilled', order_endorse_date, order_id_endorse])
            print('\n*** Order endorsed successfully ***')
        input('\n*** Enter any key to go back ***')
        deliverer_menu()

    if deliverer_action == '4':
        login()

    deliverer_menu()


def login():
    global current_user_staff_id, current_user_staff_name
    print('\n=== Login ===')
    username = input("Username:")

    # password = pyautogui.password(text='', title='', default='', mask='*')
    password = input("Password:")

    returned_rows, data = db_r_query('SELECT * FROM staff WHERE username=%s', [username])
    # print(data)
    if not data or password != data[0][5]:  # if (data is empty) || (password is wrong)
        print('*** fail ***')
        login()
    print('*** success ***')
    current_user_staff_id = data[0][0]
    current_user_staff_name = data[0][1]

    if data[0][2] == 'Admin':
        admin_menu()
    if data[0][2] == 'Manager':
        manager_menu()
    if data[0][2] == 'Merchandiser':
        merchandiser_menu()
    if data[0][2] == 'Packer':
        packer_menu()
    if data[0][2] == 'Deliverer':
        deliverer_menu()
    login()


login()
