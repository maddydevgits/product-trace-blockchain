from flask import Flask, flash,redirect,request,render_template,session, url_for
from web3 import Web3,HTTPProvider
import json

app=Flask(__name__)
app.secret_key='hackhive'

def connect_with_register_blockchain(acc):
    blockchainServer='http://127.0.0.1:7545'
    web3=Web3(HTTPProvider(blockchainServer))
    if acc==0:
        acc=web3.eth.accounts[0]
    web3.eth.defaultAccount=acc
    artifact_path='../build/contracts/traceability.json'
    with open(artifact_path) as f:
        contract_json=json.load(f)
        contract_abi=contract_json['abi']
        contract_address=contract_json['networks']['5777']['address']
    contract=web3.eth.contract(address=contract_address,abi=contract_abi)
    return(contract,web3)    

@app.route('/')
def homePage():
    return render_template('home.html')

@app.route('/manufacturer')
def manufacturerPage():
    return render_template('index.html')

@app.route('/manufacturerRegistrationForm',methods=['POST','GET'])
def manufacturerRegistrationForm():
    name=request.form['name']
    address=request.form['address']
    email=request.form['email']
    username=request.form['username']
    contact=request.form['contact']
    password=request.form['password']
    print(name,address,email,username,contact,password)
    try:
        contract,web3=connect_with_register_blockchain(0)
        tx_hash=contract.functions.addManufacturer(name,address,email,username,contact,password,0).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return render_template('index.html',message='account created successful')
    except:
        return render_template('index.html',error='account exist')

@app.route('/manufacturerLogin')
def manufacturerLogin():
    return render_template('manufacturer_login.html')

@app.route('/manufacturerLoginForm',methods=['POST'])
def manufacturerLoginForm():
    username=request.form['username']
    password=request.form['password']
    try:
        contract,web3=connect_with_register_blockchain(0)
        data=contract.functions.viewManufacturers(username).call()
        print(data)
        if(data[-5]==username and data[-3]==password):
            session['username']=username
            session['name']=data[0]
            return redirect('/manufacturerDashboard')
        else:
            return render_template('manufacturer_login.html',error='invalid credentials')
    except:
        return render_template('manufacturer_login.html',error='Invalid login')

@app.route('/manufacturerDashboard')
def manufacturerDashboard():
    return render_template('manufactuer_dashboard.html')

@app.route('/logout')
def logout():
    session['username']=None
    return redirect('/')

@app.route('/manufacturerDashboardForm',methods=['POST'])
def manufacturerDashboardForm():
    manu=session['username']
    productname=request.form['productname']
    productid=request.form['productid']
    productdescription=request.form['productdescription']
    print(manu,productname,productid,productdescription)
    try:
        contract,web3=connect_with_register_blockchain(0)
        tx_hash=contract.functions.addProduct(manu,productid,productname,productdescription).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return render_template('manufactuer_dashboard.html',message='Product Added successfully')
    except:
        return render_template('manufactuer_dashboard.html',error='product not added')

@app.route('/manufacturerViewProducts')
def manufacturerViewProducts():
    contract,web3=connect_with_register_blockchain(0)
    data=contract.functions.viewProductsByManu(session['username']).call()
    manfacturerData=contract.functions.viewManufacturers(session['username']).call()
    print(data)
    # print(manfacturerData)
    name=manfacturerData[0]
    allUsers=contract.functions.viewUsers().call()
    # print(allUsers)
    alld=[]
    for i in range(len(allUsers)):
        if allUsers[i][-2]==1:
            dummy=[]
            dummy.append(allUsers[i][0])
            dummy.append(allUsers[i][-5])
            alld.append(dummy)
        else:
            continue
    print(alld)

    return render_template('manufacturer_view_products.html',products=data,name=name,d=alld)

@app.route('/updateDistributor', methods=['POST'])
def updateDistributor():
    contract, web3 = connect_with_register_blockchain(0)
    product_id = request.form['product_id']
    distributor_id = request.form['distributor_id']
    print(product_id,distributor_id)
    
    # Call the smart contract function to update the distributor
    if distributor_id:
        tx_hash = contract.functions.updateDistributor(session['username'],product_id, distributor_id).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        print("Distributor updated successfully!", "success")
    else:
        print("Please select a distributor.", "error")
    
    return redirect(url_for('manufacturerViewProducts'))

@app.route('/distributor')
def distributor():
    return render_template('distributor_registration.html')

@app.route('/distributorRegistrationForm',methods=['POST'])
def distributorRegistrationForm():
    name=request.form['name']
    address=request.form['address']
    email=request.form['email']
    username=request.form['username']
    contact=request.form['contact']
    password=request.form['password']
    print(name,address,email,username,contact,password)
    try:
        contract,web3=connect_with_register_blockchain(0)
        tx_hash=contract.functions.addManufacturer(name,address,email,username,contact,password,1).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return render_template('distributor_registration.html',message='account created successful')
    except:
        return render_template('distributor_registration.html',error='account exist')

@app.route('/distributorLogin')
def distributorLogin():
    return render_template('distributor_login.html')

@app.route('/distributorLoginForm',methods=['POST'])
def distributorLoginForm():
    username=request.form['username']
    password=request.form['password']
    try:
        contract,web3=connect_with_register_blockchain(0)
        data=contract.functions.viewManufacturers(username).call()
        print(data)
        if(data[-5]==username and data[-3]==password):
            session['username']=username
            session['name']=data[0]
            return redirect('/distributorDashboard')
        else:
            return render_template('distributor_login.html',error='invalid credentials')
    except:
        return render_template('distributor_login.html',error='Invalid login')
    
@app.route('/distributorDashboard')
def distributorDashboard():
    contract, web3 = connect_with_register_blockchain(0)
    distributor_username = session['username']  # Assuming the distributor's username is stored in the session
    
    # Fetch products assigned to this distributor
    products = contract.functions.viewProductsByDistributor(distributor_username).call()
    print(products)

    allUsers=contract.functions.viewUsers().call()
    # print(allUsers)
    allr=[]
    for i in range(len(allUsers)):
        if allUsers[i][-2]==2:
            dummy=[]
            dummy.append(allUsers[i][0])
            dummy.append(allUsers[i][-5])
            allr.append(dummy)
        else:
            continue
    return render_template('distributor_dashboard.html', products=products,r=allr)

@app.route('/updateRetailer', methods=['POST'])
def updateRetailer():
    contract, web3 = connect_with_register_blockchain(0)
    distributor_username = session['username']
    product_id = request.form['product_id']
    retailer_id = request.form['retailer_id']
    
    # Check if a retailer has been selected
    if retailer_id:
        # Call the updateRetailer function in the smart contract
        tx_hash = contract.functions.updateRetailer(distributor_username, product_id, retailer_id).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        print("Retailer updated successfully!", "success")
    else:
        print("Please select a retailer.", "error")
    
    return redirect(url_for('distributorDashboard'))

@app.route('/retailer')
def retailerPage():
    return render_template('retailer_registration.html')

@app.route('/retailerRegistrationForm',methods=['POST'])
def retailerRegistrationForm():
    name=request.form['name']
    address=request.form['address']
    email=request.form['email']
    username=request.form['username']
    contact=request.form['contact']
    password=request.form['password']
    print(name,address,email,username,contact,password)
    try:
        contract,web3=connect_with_register_blockchain(0)
        tx_hash=contract.functions.addManufacturer(name,address,email,username,contact,password,2).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        return render_template('retailer_registration.html',message='account created successful')
    except:
        return render_template('retailer_registration.html',error='account exist')

@app.route('/retailerLogin')
def retailerLogin():
    return render_template('retailer_login.html')

@app.route('/retailerLoginForm',methods=['POST'])
def retailerLoginForm():
    username=request.form['username']
    password=request.form['password']
    try:
        contract,web3=connect_with_register_blockchain(0)
        data=contract.functions.viewManufacturers(username).call()
        print(data)
        if(data[-5]==username and data[-3]==password):
            session['username']=username
            session['name']=data[0]
            return redirect('/retailerDashboard')
        else:
            return render_template('retailer_login.html',error='invalid credentials')
    except:
        return render_template('retailer_login.html',error='Invalid login')

@app.route('/retailerDashboard')
def retailerDashboard():
    contract, web3 = connect_with_register_blockchain(0)
    retailer_username = session['username']  # Assuming the retailer's username is stored in the session

    # Fetch products assigned to this retailer
    products = contract.functions.viewProductsByRetailer(retailer_username).call()

    return render_template('retailer_view_product.html', products=products)

@app.route('/traceProduct', methods=['POST'])
def traceProduct():
    contract, web3 = connect_with_register_blockchain(0)
    product_id = request.form['product_id']

    # Retrieve product details from the blockchain
    product = contract.functions.viewProduct(product_id).call()

    # Extract relevant details
    manufacturer_id = product[0]
    distributor_id = product[4] if product[7] else "Not Assigned"
    retailer_id = product[5] if product[8] else "Not Assigned"

    # Retrieve additional information for each entity
    manufacturer = contract.functions.viewManufacturers(manufacturer_id).call()
    distributor = contract.functions.viewManufacturers(distributor_id).call() if distributor_id != "Not Assigned" else None
    retailer = contract.functions.viewManufacturers(retailer_id).call() if retailer_id != "Not Assigned" else None

    return render_template('trace_results.html', product=product, manufacturer=manufacturer, distributor=distributor, retailer=retailer)

@app.route('/customer')
def customerPage():
    return render_template('customer.html')

if __name__=="__main__":
    app.run(host='0.0.0.0',port=2000,debug=True)
