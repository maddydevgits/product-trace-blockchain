// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract traceability {
  string[] _productids;
  string[] _manufacturerids;

  struct manufacturer{
    string _name;
    string _address;
    string _email;
    string _username;
    string _contact;
    string _password;
    uint _role; 
    bool _status;
  }

  struct product{
    string _manufacturer;
    string _productId;
    string _productName;
    string _productDescription;
    string _distributor;
    string _retailer;
    bool _productStatus;
    bool _distributorStatus;
    bool _retailerStatus;
  }

  mapping(string=>manufacturer) _manufacturers;
  mapping(string=>product) _products;

  function addManufacturer(string memory name,string memory addr,string memory email,string memory username,string memory contact, string memory password,uint role) public {
    require(!_manufacturers[username]._status,"Username already taken");

    manufacturer memory new_manufacturer =  manufacturer(name,addr,email,username,contact,password,role,true);
    _manufacturers[username]=new_manufacturer;
    _manufacturerids.push(username);
  }

  function viewManufacturers(string memory username) public view returns(manufacturer memory) {
    return (_manufacturers[username]);
  }

  function addProduct(string memory manu,string memory productid,string memory productname,string memory productdescription) public {
    require(!_products[productid]._productStatus,"Product Exist");

    product memory new_product = product(manu,productid,productname,productdescription,manu,manu,true,false,false);
    _products[productid]=new_product;

    _productids.push(productid);
  }

  function viewProduct(string memory productid) public view returns (product memory){
    return (_products[productid]);
  }

  function viewProducts() public view returns(product[] memory){
    product[] memory allProducts = new product[](_productids.length);

    for(uint i=0;i<_productids.length;i++){
      allProducts[i]=_products[_productids[i]];
    }
    return allProducts;
  }

  function updateDistributor(string memory manu,string memory productid,string memory d) public {
    if(keccak256(abi.encodePacked(_products[productid]._manufacturer))==keccak256(abi.encodePacked(manu))){
      if(_products[productid]._distributorStatus==false){
        _products[productid]._distributor=d;
        _products[productid]._distributorStatus=true;
      }
    }
  }

  function updateRetailer(string memory d,string memory productid,string memory r) public {
    if(keccak256(abi.encodePacked(_products[productid]._distributor))==keccak256(abi.encodePacked(d))){
      if(_products[productid]._distributorStatus==true){
        _products[productid]._retailer=r;
        _products[productid]._retailerStatus=true;
      }
    }
  }

  function viewUsers() public view returns(manufacturer[] memory){
    manufacturer[] memory allUsers = new manufacturer[](_manufacturerids.length);

    for(uint i=0;i<_manufacturerids.length;i++){
      allUsers[i]=_manufacturers[_manufacturerids[i]];
    }
    return allUsers;
  }

  function viewProductsByManu(string memory username) public view returns(product[] memory){
    uint count=0;

    for(uint i=0;i<_productids.length;i++){
      if(keccak256(abi.encodePacked(_products[_productids[i]]._manufacturer))==keccak256(abi.encodePacked(username))){
        count++;
      }
    }

    product[] memory myProducts = new product[](count);
    uint index=0;

    for(uint i=0;i<_productids.length;i++){
      if(keccak256(abi.encodePacked(_products[_productids[i]]._manufacturer))==keccak256(abi.encodePacked(username))){
        myProducts[index]=_products[_productids[i]];
        index++;
      }
    }
    return myProducts;
  }

  function viewProductsByDistributor(string memory distributor) public view returns (product[] memory) {
    uint count = 0;

    for (uint i = 0; i < _productids.length; i++) {
        if (keccak256(abi.encodePacked(_products[_productids[i]]._distributor)) == keccak256(abi.encodePacked(distributor))) {
            count++;
        }
    }

    product[] memory distributorProducts = new product[](count);
    uint index = 0;

    for (uint i = 0; i < _productids.length; i++) {
        if (keccak256(abi.encodePacked(_products[_productids[i]]._distributor)) == keccak256(abi.encodePacked(distributor))) {
            distributorProducts[index] = _products[_productids[i]];
            index++;
        }
    }
    return distributorProducts;
  }

  function viewProductsByRetailer(string memory retailer) public view returns (product[] memory) {
    uint count = 0;

    for (uint i = 0; i < _productids.length; i++) {
        if (keccak256(abi.encodePacked(_products[_productids[i]]._retailer)) == keccak256(abi.encodePacked(retailer))) {
            count++;
        }
    }

    product[] memory retailerProducts = new product[](count);
    uint index = 0;

    for (uint i = 0; i < _productids.length; i++) {
        if (keccak256(abi.encodePacked(_products[_productids[i]]._retailer)) == keccak256(abi.encodePacked(retailer))) {
            retailerProducts[index] = _products[_productids[i]];
            index++;
        }
    }
    return retailerProducts;
  }

  function traceProduct(string memory productId) public view 
        returns (
            string memory productName,
            string memory productDescription,
            string memory manufacturerName,
            string memory manufacturerAddress,
            string memory distributorName,
            string memory distributorAddress,
            string memory retailerName,
            string memory retailerAddress
        ) 
    {
        // Fetch the product using product ID
        product memory prod = _products[productId];

        // Fetch manufacturer details
        manufacturer memory manu = _manufacturers[prod._manufacturer];
        
        // Default values for distributor and retailer
        string memory distributorName = "Not Assigned";
        string memory distributorAddress = "Not Assigned";
        string memory retailerName = "Not Assigned";
        string memory retailerAddress = "Not Assigned";
        
        // Fetch distributor details if assigned
        if (prod._distributorStatus) {
            manufacturer memory dist = _manufacturers[prod._distributor];
            distributorName = dist._name;
            distributorAddress = dist._address;
        }
        
        // Fetch retailer details if assigned
        if (prod._retailerStatus) {
            manufacturer memory retail = _manufacturers[prod._retailer];
            retailerName = retail._name;
            retailerAddress = retail._address;
        }
        
        return (
            prod._productName,
            prod._productDescription,
            manu._name,
            manu._address,
            distributorName,
            distributorAddress,
            retailerName,
            retailerAddress
        );
    }



}
