#  Base_application

## Models
- Customer
- Loan
- Payment
- PaymentDetail

## Business Logic
- `customer_logic.py`: Contains logic for customer-related operations.
- `loan_logic.py`: Contains logic for loan-related operations.
- `payment_logic.py`: Contains logic for payment-related operations.

## Serializers
- `serializers.py`: Contains serializers for Customer, Loan, Payment, and PaymentDetail models.

## Tests
- `tests.py`: Contains unit tests for the project.

## Views
- `views.py`: Contains Django views for handling API endpoints.

### Setting Up Virtual Environment and Installing Dependencies

To set up a virtual environment and install dependencies using `requirements.txt`, follow these steps:

1. **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

2. **Activate the virtual environment:**

    - **On Windows:**

        ```bash
        venv\Scripts\activate
        ```

    - **On macOS and Linux:**

        ```bash
        source venv/bin/activate
        ```

3. **Install dependencies using `requirements.txt`:**

    ```bash
    pip install -r requirements.txt
    ```

## Create image with docker


To build the Docker image, follow these steps:

1. Open a terminal.
2. Navigate to the root directory of the project.
3. Run the following command to build the Docker images:
   ```bash
   docker-compose build
   docker-compose up
    ```

 ## Generate Api-Key

 This project uses rest_framework_api_key, the next commands where used to generated it: 
 ```bash
 python manage.py shell
 api_key, key = APIKey.objects.create_key(name="my-remote-service")
 print(f"created API KEY: {key}")
```

## Services

This  outlines the various services available in the system, along with their endpoints, request parameters, response attributes, and status codes.

Each service is described in detail, including examples of request and response payloads, along with explanations of the parameters and attributes.

Feel free to refer to this document to understand how to interact with the different endpoints in the system.

You can also can check the postman collection:  

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/17834641-217bf94d-91ba-4b75-8d38-7e74d3658b34?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D17834641-217bf94d-91ba-4b75-8d38-7e74d3658b34%26entityType%3Dcollection%26workspaceId%3D832be956-8010-4a6f-9044-b5639af51b92)

required Authorization Header with api-key:
```bash
 Authorization: Api-Key sAOzx2dH.c25DGva4USGomyimDhHBtCgqSxVm1TGY
```

### Service: Create Customer

#### Description

This service creates a new customer with the provided information.

#### Endpoint

- **POST** `/create_customer/`

#### Request

##### Parameters:

- `external_id` (string): The external ID of the customer.
- `score` (integer): The score of the customer.
- `preapproved_at` (date, optional): The date and time when the customer was preapproved.

##### Example:

```json
{
    "external_id": "external_1",
    "score": 1000,
    "preapproved_at": "2024-05-20T22:15:54Z"
}
```


##### Response:

```json
{
    "external_id": "external_1",
    "status": 1,
    "score": "1000.00",
    "preapproved_at": "2024-05-20T22:15:54Z"
}
```

##### Attributes

- `external_id` (string): The external ID of the customer.
- `status` (integer): The status of the customer (1 indicates active).
- `score` (string): The credit of the customer.
- `preapproved_at` (date): The date and time when the customer was preapproved.


### Service: Get Customers

#### Description

This service retrieves a list of customers with their details.

#### Endpoint

- **GET** `/get_customers`

#### Response

##### Example:

```json
[
    {
        "external_id": "external_1",
        "score": 1000.0,
        "total_debt": 0.0,
        "available_amount": 1000.0
    },
    {
        "external_id": "external_2",
        "score": 1000.0,
        "total_debt": 0.0,
        "available_amount": 1000.0
    }
]
```


##### Attributes

- `external_id` (string): The external ID of the customer.
- `score` (float): The score of the customer.
- `total_debt` (float): The total debt of the customer.
- `available_amount` (float): The available amount for the customer.


### Service: Get Customer Balance

#### Description

This service retrieves the balance information for a specific customer.

#### Endpoint

- **GET** `/get_customer_balance/{external_id}`

#### Response

##### Example:

```json
{
    "external_id": "external_1",
    "score": 1000.0,
    "total_debt": 0.0,
    "available_amount": 1000.0
}
```

##### Attributes

- `external_id` (string): The external ID of the customer.
- `score` (float): The score of the customer.
- `total_debt` (float): The total debt of the customer.
- `available_amount` (float): The available amount for the customer.


### Service: Create Loan

#### Description

This service creates a new loan for a specific customer.

#### Endpoint

- **POST** `/create_loan/`

#### Request

##### Example:

```json
{
    "external_id": "external_1_01",
    "customer_external_id": "external_1",
    "amount": 50
}
```

##### Parameters:

- `external_id` (string): The external ID of the loan.
- `customer_external_id` (string): The external ID of the customer associated with the loan.
- `amount` (float): The amount of the loan.

#### Response

##### Example:

```json
{
    "external_id": "external_1_01",
    "amount": "50.00"
}
```

### Service: Make Payment

#### Description

This service processes a payment made by a customer.

#### Endpoint

- **POST** `/make_payment/`

#### Request

##### Example:

```json
{
    "external_id": "PAY1",
    "total_amount": 700,
    "paid_at": "2024-05-22T10:00:00Z",
    "customer_external_id": "external_1"
}
```

#### Response

##### Example:

```json
{
    "external_id": "PAY1",
    "total_amount": "700.0000000000",
    "paid_at": "2024-05-22T10:00:00Z"
}
```
#### Attributes

- `external_id` (string): The external ID of the payment.
- `total_amount` (string): The total amount of the payment.
- `paid_at` (date): The date and time when the payment was made.
### Service: Get Loans

#### Description

This service retrieves a list of loans for a specific customer.

#### Endpoint

- **GET** `/getLoans/{customer_external_id}`

#### Response

##### Example:

```json
[
    {
        "external_id": "external_1_01",
        "amount": "50.00",
        "outstanding": "0.00",
        "status": 4,
        "customer_external_id": "external_1"
    },
    {
        "external_id": "external_1_02",
        "amount": "200.00",
        "outstanding": "0.00",
        "status": 4,
        "customer_external_id": "external_1"
    },
    {
        "external_id": "external_1_03",
        "amount": "400.00",
        "outstanding": "0.00",
        "status": 4,
        "customer_external_id": "external_1"
    },
    {
        "external_id": "external_1_04",
        "amount": "350.00",
        "outstanding": "300.00",
        "status": 2,
        "customer_external_id": "external_1"
    }
]
```

##### Attributes

- `external_id` (string): The external ID of the loan.
- `amount` (string): The amount of the loan.
- `outstanding` (string): The outstanding amount of the loan.
- `status` (integer): The status of the loan.
- `customer_external_id` (string): The external ID of the customer associated with the loan.


