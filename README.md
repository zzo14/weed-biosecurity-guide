# WEED BIOSECURITY GUIDE

Welcome to our Weed Biosecurity Guide Web App. This Flask Python web application serves as a biosecurity guide, providing information on weeds present in New Zealand. The application features a responsive design with a garden weed theme and offers different levels of access for various user roles.

## Showcase
Check out our live demo here: [WEED BIOSECURITY GUIDE](https://patrickzou.pythonanywhere.com/)

## Requirements
 - Python 3.12
 - Flask
 - MySQL
 - Other dependencies listed in requirements.txt

## Features
 - **User Authentication**: Secure login and registration system for Gardeners, Staff, and Administrators.
 - **Role-Based Access Control**: Different levels of access and functionalities for each user role.
 - **Weed Guide**: Comprehensive guide with primary images, common names, and types of weeds. Detailed information when clicking the primary image.
 - **User Profile Management**: Users can update their personal information and change passwords.
 - **Responsive Design**: The web app is styled to reflect a garden weed theme and is responsive to different screen sizes.

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

## References
The information and images in this web app are sourced from the New Zealand Weeds Database by Massey University. [Visit the database](https://www.massey.ac.nz/about/colleges-schools-and-institutes/college-of-sciences/our-research/themes-and-research-strengths/plant-science-research/new-zealand-weeds-database/).
