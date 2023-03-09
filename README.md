# alvative

### Preparing the project

- Create a Folder on your Local machine / Computer
- Open Command prompt(git bash) / Terminal in the same folder location

### Creating a virtual environment (for gitbash users)

- run: python -m venv env (To install a virtual environment=> env is the name of your virtual environment in this case)
- run: source env/scripts/activate (To activate the virtual environment)

### Cloning the Repository

Visit the project Repository on Github Website: https://github.com/KimBitrus26/alvative.git

- Click on the "Code" button on the Repo page

- Copy the URL git@github.com:salistech/shop_secure.git (for ssh users) as shown on the dropdown or https://github.com/KimBitrus26/alvative.git

- In your Terminal, run: git clone ghttps://github.com/KimBitrus26/alvative.git


### Project requirements installation:

- pip install -r requirement.txt

### Running the server

- run: python manage.py makemigrations

- run: python manage.py migrate

- python manage.py migrate --run-syncdb


- visit the url http://127.0.0.1:8000 or http://localhost:8000 to view the project


# Endpoints


### An endpoint to initiaten transaction to paystack
- http://kimbitrus.pythonanywhere.com/

### An endpoint to verify paystack payment
- http://kimbitrus.pythonanywhere.com/api/v1/verify-payment/ref_code/

### An endpoint to get list banks from paystack
- http://kimbitrus.pythonanywhere.com/api/v1/get-bank-list/

### An endpoint to resolve or validate bank account details exist from paystack
- http://kimbitrus.pythonanywhere.com/api/v1/resolve-bank-account/

### An endpoint to create bank account to database
- http://kimbitrus.pythonanywhere.com/api/v1/create-bank/


## Loom video demo for the app testing
- https://www.loom.com/share/8545cbac8dee45cf8b838e5e05f5d167