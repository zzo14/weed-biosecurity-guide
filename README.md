# WEED BIOSECURITY GUIDE

Welcome to our Weed Biosecurity Guide Web App. This Flask Python web application serves as a biosecurity guide, providing information on weeds present in New Zealand. The application features a responsive design with a garden weed theme and offers different levels of access for various user roles.

## Showcase
Check out our live demo here: [WEED BIOSECURITY GUIDE](https://patrickzou.pythonanywhere.com/)

## Installation and Setup
 - Clone the repository: `git clone https://github.com/zzo14/Biosecurity.git`
 - Install the required packages: `pip install -r requirements.txt`
 - Set up the database using the provided MySQL scripts.
 - Change `dbuser` and `dbpass` in `Biosecurity/app/connect.py` to your MySQL username and password.
 - Run the application: `flask run`

## Login Information
The application includes a login system with separate dashboards for three user roles: Gardener, Staff, and Administrator.

### Gardener
 - Username: gardener1
 - Password: 123456Zzz!
 - Access: Manage personal profile, view weed guide with detailed information.

### Staff
 - Username: staff1
 - Password: 123456Zzz!
 - Access: Manage personal profile, view Gardener profiles, manage weed guide.

### Administrator
 - Username: admin
 - Password: 123456Zzz!
 - Access: Full access to the system, manage Gardener and Staff profiles, manage weed guide.
