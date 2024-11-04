
# Product Traceability Blockchain Application

This application provides a blockchain-based solution for tracking products throughout the supply chain, ensuring transparency and authenticity by leveraging Ethereum smart contracts.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Architecture](#architecture)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Routes and Functionalities](#routes-and-functionalities)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This application enables manufacturers, distributors, and retailers to register, manage, and trace products through the supply chain. By recording product information on an immutable ledger, it helps prevent counterfeiting and builds trust among stakeholders.

## Features

- **Role-based Access**:
  - **Manufacturer**: Register, log in, add products, assign distributors.
  - **Distributor**: Register, log in, view assigned products, assign retailers.
  - **Retailer**: Register, log in, view assigned products.
  - **Customer**: View product traceability.
- **Product Traceability**: Trace a product’s history, viewing details about each entity involved.
- **Blockchain Integration**: Uses Ethereum smart contracts to manage product and user data on the blockchain, ensuring transparency and security.

## Technologies Used

- **Backend**: Python with Flask
- **Blockchain Platform**: Ethereum
- **Smart Contract Development**: Solidity
- **Web3 Interface**: Web3.py
- **Local Blockchain Testing**: Ganache

## Architecture

The application uses Flask as a web server and connects to an Ethereum blockchain (via Ganache) to interact with a deployed smart contract. The smart contract, `traceability`, stores data on products and users (manufacturers, distributors, and retailers).

### Smart Contract Overview

- **manufacturer**: Struct that holds information about each registered manufacturer.
- **product**: Struct that stores details about each product and tracks its journey across different entities in the supply chain.

## Setup and Installation

### Prerequisites

Ensure you have the following installed:
- [Python](https://www.python.org/downloads/)
- [Node.js and npm](https://nodejs.org/)
- [Truffle](https://www.trufflesuite.com/truffle)
- [Ganache](https://www.trufflesuite.com/ganache)
- [MetaMask](https://metamask.io/) (for blockchain interaction if deploying to a testnet)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/maddydevgits/product-trace-blockchain.git
   cd product-trace-blockchain
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install and configure Ganache**:
   - Start Ganache and ensure it’s running on `http://127.0.0.1:7545`.

4. **Deploy the Smart Contract**:
   - Use Truffle to deploy the contract to your Ganache blockchain.
   ```bash
   truffle migrate --network development
   ```

5. **Configure Contract ABI and Address**:
   - Update `app.py` to point to the correct path for the contract ABI (`traceability.json`) and network address in `../build/contracts`.

6. **Run the Flask Application**:
   ```bash
   flask run --host=0.0.0.0 --port=2000
   ```

7. **Access the Application**:
   - Open a browser and go to `http://localhost:2000`.

## Usage

- **Homepage** (`/`): Main landing page.
- **Manufacturer Registration** (`/manufacturer`): Register as a manufacturer.
- **Product Management**:
  - Add, view, and manage products via the manufacturer dashboard.
- **Distributor and Retailer**: Each role can log in, view assigned products, and update product status as it moves through the supply chain.
- **Traceability**:
  - Customers can view the full history of any product through the supply chain.

## Routes and Functionalities

### Manufacturer Routes

- **`/manufacturer`**: Register as a manufacturer.
- **`/manufacturerRegistrationForm`**: Handle manufacturer registration.
- **`/manufacturerLogin`**: Log in as a manufacturer.
- **`/manufacturerDashboard`**: Access the manufacturer dashboard.
- **`/manufacturerViewProducts`**: View all products created by the manufacturer.
- **`/updateDistributor`**: Assign a distributor to a product.

### Distributor Routes

- **`/distributor`**: Register as a distributor.
- **`/distributorRegistrationForm`**: Handle distributor registration.
- **`/distributorLogin`**: Log in as a distributor.
- **`/distributorDashboard`**: Access the distributor dashboard, view assigned products, and assign retailers.

### Retailer Routes

- **`/retailer`**: Register as a retailer.
- **`/retailerRegistrationForm`**: Handle retailer registration.
- **`/retailerLogin`**: Log in as a retailer.
- **`/retailerDashboard`**: Access the retailer dashboard and view assigned products.

### Customer Routes

- **`/traceProduct`**: Trace a product’s journey by viewing details about each entity involved (manufacturer, distributor, retailer).

### Logout

- **`/logout`**: Clear the session and log out of the application.

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
