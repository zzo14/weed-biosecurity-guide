DROP SCHEMA IF EXISTS biosercurity;
CREATE SCHEMA biosercurity;
USE biosercurity;

/* ----- Create the tables: ----- */
CREATE TABLE IF NOT EXISTS userAuth (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    password_salt VARCHAR(255) NOT NULL,
    userType ENUM('Admin', 'Staff', 'Gardener') NOT NULL
);

CREATE TABLE IF NOT EXISTS gardener (
    gardener_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    address VARCHAR(100) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    date_joined DATE NOT NULL,
    status ENUM("Active", "Inactive") NOT NULL,
    FOREIGN KEY (gardener_id) REFERENCES userAuth(id)
);

CREATE TABLE IF NOT EXISTS staff (
    staff_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    work_phone VARCHAR(20) NOT NULL,
    hire_date DATE NOT NULL,
    position VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    status ENUM("Active", "Inactive") NOT NULL,
    FOREIGN KEY (staff_id) REFERENCES userAuth(id)
);

CREATE TABLE IF NOT EXISTS administration (
    admin_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    work_phone VARCHAR(20) NOT NULL,
    hire_date DATE NOT NULL,
    position VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    status ENUM("Active", "Inactive") NOT NULL,
    FOREIGN KEY (admin_id) REFERENCES userAuth(id)
);

CREATE TABLE IF NOT EXISTS weedGuide (
    weed_id INT PRIMARY KEY AUTO_INCREMENT,
    common_name VARCHAR(50) NOT NULL,
    scientific_name VARCHAR(50) NOT NULL,
    weed_type VARCHAR(50) NOT NULL,
    description TEXT,
    impacts TEXT,
    control_methods TEXT
);

CREATE TABLE IF NOT EXISTS weedImage (
    image_id INT PRIMARY KEY AUTO_INCREMENT,
    weed_id INT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    is_primary BOOLEAN NOT NULL,
    FOREIGN KEY (weed_id) REFERENCES weedGuide(weed_id)
);

/* ----- Insert data into the tables: ----- */
INSERT INTO userAuth (username, password_hash, password_salt, userType) VALUES
    ('gardener1', 'hash1', 'salt1', 'Gardener'),
    ('gardener2', 'hash2', 'salt2', 'Gardener'),
    ('gardener3', 'hash3', 'salt3', 'Gardener'),
    ('gardener4', 'hash4', 'salt4', 'Gardener'),
    ('gardener5', 'hash5', 'salt5', 'Gardener');

INSERT INTO gardener (gardener_id, first_name VARCHAR(50), last_name, address, email, phone_number, date_joined, status) VALUES
    (LAST_INSERT_ID() - 4, "John", "Doe", "121 Main St", "john.doe@example.com", "123-456-7860", "2024-01-01", "Active"),
    (LAST_INSERT_ID() - 3, "Jane", "Smith", "122 Main St", "jane.smith@example.com", "123-456-7860", "2024-01-01", "Active"),
    (LAST_INSERT_ID() - 2, "Joe", "Jackson", "123 Main St", "joe.jackson@example.com", "123-456-7860", "2024-01-01", "Active"),
    (LAST_INSERT_ID() - 1, "Jim", "Milly", "125 Main St", "jim.milly@example.com", "123-456-7860", "2024-01-01", "Active"),
    (LAST_INSERT_ID(), "Jack", "Johnson", "124 Main St", "jack.johnson@example.com", "123-456-7860", "2024-01-01", "Active"),

INSERT INTO userAuth (username, password_hash, password_salt, userType) VALUES
    ('staff1', 'hash6', 'salt6', 'Staff'),
    ('staff2', 'hash7', 'salt7', 'Staff'),
    ('staff3', 'hash8', 'salt8', 'Staff');

INSERT INTO staff (staff_id, first_name, last_name, email, work_phone, hire_date, position, department, status) VALUES
    (LAST_INSERT_ID() - 2, "Alice", "Brown", "alice.brown@example.com", "123-456-7860", "2024-01-01", "Researcher", "Botany", "Active"),
    (LAST_INSERT_ID() - 1, "Bob", "Green", "bob.green@example.com", "123-456-7860", "2024-01-01", "Technician", "Maintenance", "Active"),
    (LAST_INSERT_ID(), "Charlie", "Blue", "charlie.blue@example.com", "123-456-7860", "2024-01-01", "Agent", "Operations", "Active"),

INSERT INTO userAuth (username, password_hash, password_salt, userType) VALUES
    ('admin', 'hash9', 'salt9', 'Admin');

INSERT INTO administration (admin_id, first_name VARCHAR(50), last_name, address, email, phone_number, date_joined, status) VALUES
    (LAST_INSERT_ID(), "Diana", "White", "diana.white@example.com", "123-456-7860", "2024-01-01", "Manager", "Administration", "Active"),

INSERT INTO weedGuide (common_name, scientific_name, weed_type, description, impacts, control_methods)

INSERT INTO weedImage (weed_id, image_url, is_primary)
