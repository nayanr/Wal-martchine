import sqlite3

#Open database
conn = sqlite3.connect('database.db')

#Create table
conn.execute('''CREATE TABLE users 
		(userId INTEGER PRIMARY KEY, 
		password TEXT,
		email TEXT,
		firstName TEXT,
		lastName TEXT
		
		)''')

conn.execute('''CREATE TABLE products
		(productId INTEGER PRIMARY KEY,
		name TEXT,
		price REAL
		)''')

conn.execute('''CREATE TABLE kart
		(userId INTEGER,
		productId INTEGER,
		FOREIGN KEY(userId) REFERENCES users(userId),
		FOREIGN KEY(productId) REFERENCES products(productId)
		)''')

conn.execute('''CREATE TABLE orders
             (userId INTEGER,
             productId INTEGER,
             FOREIGN KEY(userId) REFERENCES users(userId),
             FOREIGN KEY(productId) REFERENCES products(productId)
             )''')

conn.execute('''CREATE TABLE recommend
             (
                rid INTEGER PRIMARY KEY,
            		nitem TEXT

             )''')
#
#conn.execute('''DROP TABLE recomm
#            ''')
conn.close()



with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM recomm')
        data = cur.fetchall()
        data
conn.close()
#
import pandas as pd
import numpy
from numpy import array
with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = ?", ('a@sams.com', ))
        userId = cur.fetchone()[0]
        cur.execute("SELECT products.productId, products.name, products.price FROM products, kart WHERE products.productId = kart.productId AND kart.userId = ?", (userId, ))
        products = cur.fetchall()
        listproducts = []
        nameproducts = []
        for i in range(len(products)):
            listproducts.append(products[i][0])
            nameproducts.append(products[i][1])

        cart_vector = [0]*1681
        for item in listproducts:
            cart_vector[item-1] = 1
            
        df = pd.read_csv("d_i.csv")
        df = df.drop(columns = ['dish_id','index'])
        np_matrix = df.as_matrix() 
        
        
        cart_np = array(cart_vector) 
        cart_nptr = cart_np.T
        result = np_matrix.dot(cart_nptr)
        
        result.shape
        
        
        
        import csv
        import pandas as pd
        import numpy as np
        from numpy import array
        u_i = pd.read_csv("u_i.csv")
        u_i = u_i.set_index(["dish_id"])
        u_i = u_i.drop(columns=['Unnamed'])
        u, sig, v_transposed = np.linalg.svd(u_i, full_matrices=False)
        sum_sig_90 = sum(sig)*0.9
        sum_sig_90
        for i in range(len(sig)):
            sum_sig_90 = sum_sig_90 - sig[i]
            if(sum_sig_90<=0):
                j = i
                break
        sig_new = sig[:j]
        
        u_refined = u[:,:j]
        v_t_refined = v_transposed[:j]
        
        u_i_SVD = np.dot(u_refined, np.dot(np.diag(sig_new), v_t_refined))
        normalized_cart = np.multiply(u_i_SVD[userId-1],cart_np)
        
        
        
        normalized_cart.shape
        cart_nptr = normalized_cart.T
        
        result = np_matrix.dot(cart_nptr)
        
        
        result.shape
        dish_no = np.argmax(result)
        
        

        
        import json
        with open('train.json', 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        chosenCuisine = ["indian", "italian", "mexican","chinese","korean","spanish","greek","british","jamaican"]
        data = df.loc[df["cuisine"].isin(chosenCuisine)]        
        data = data.head(1000)
        data.reset_index()
        
        row =data.iloc[dish_no]
        ing_list = list(row['ingredients'])
        
        
        for items in nameproducts:
           if(items in ing_list):
              ing_list.remove(items)
        ing_list
        
        
        with sqlite3.connect('database.db') as conn2:
            
            for items in ing_list:
                try:
                    print(items)
                    string1 = "INSERT INTO recommend (nitem) VALUES ('" + str(items) + "');"
                    conn2.execute(string1)
                    conn2.commit()
                    msg = "Added successfully"
                except:
                    conn2.rollback()
                    msg = "Error occured"
        conn2.close()

with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM kart')
        data = cur.fetchall()
        data
        
conn.close()       





    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = 'a@sams.com'")
        userId = cur.fetchone()[0]
        
    conn.close()    
    
    
    with sqlite3.connect('database.db') as conn3:
        cur = conn3.cursor()
        cur.execute('SELECT nitem FROM recommend')
        recommend = cur.fetchall()
        
        
    conn3.close()
    
    for itemname in recommend:
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            string1 = "SELECT productId FROM products WHERE name = '" + str(itemname[0]) +"'"
            cur.execute(string1)
            productId = cur.fetchone()[0]
            try:
                cur.execute("INSERT INTO kart (userId, productId) VALUES (?, ?)", (userId, productId))
                conn.commit()
                msg = "Added successfully"
            except:
                conn.rollback()
                msg = "Error occured"
        conn.close()
        
    return redirect(url_for('root'))