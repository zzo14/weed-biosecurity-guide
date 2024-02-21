DROP SCHEMA IF EXISTS biosercurity;
CREATE SCHEMA biosercurity;
USE biosercurity;

/* ----- Create the tables: ----- */
CREATE TABLE IF NOT EXISTS userAuth (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    userType ENUM('Admin', 'Staff', 'Gardener') NOT NULL
);

CREATE TABLE IF NOT EXISTS gardener (
    gardener_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    address VARCHAR(100) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    date_joined DATE NOT NULL,
    status ENUM('Active', 'Inactive') NOT NULL,
    FOREIGN KEY (gardener_id) REFERENCES userAuth(id)
);

CREATE TABLE IF NOT EXISTS staff (
    staff_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    work_phone VARCHAR(20) NOT NULL,
    hire_date DATE NOT NULL,
    position VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    status ENUM('Active', 'Inactive') NOT NULL,
    FOREIGN KEY (staff_id) REFERENCES userAuth(id)
);

CREATE TABLE IF NOT EXISTS administration (
    admin_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    work_phone VARCHAR(20) NOT NULL,
    hire_date DATE NOT NULL,
    position VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    status ENUM('Active', 'Inactive') NOT NULL,
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
INSERT INTO userAuth (username, password_hash, userType) VALUES
    ('gardener1', 'scrypt:32768:8:1$3RY2MpKJfMBL6y2M$face964ccc797ac918e011d307e0d1b33c4d63ebce4a241d912edc0d498c47861f36ec03a6a39394376a930a982434b2edfa03283f4ea20f0b292c6514fce8e0', 'Gardener'),
    ('gardener2', 'scrypt:32768:8:1$3RY2MpKJfMBL6y2M$face964ccc797ac918e011d307e0d1b33c4d63ebce4a241d912edc0d498c47861f36ec03a6a39394376a930a982434b2edfa03283f4ea20f0b292c6514fce8e0', 'Gardener'),
    ('gardener3', 'scrypt:32768:8:1$3RY2MpKJfMBL6y2M$face964ccc797ac918e011d307e0d1b33c4d63ebce4a241d912edc0d498c47861f36ec03a6a39394376a930a982434b2edfa03283f4ea20f0b292c6514fce8e0', 'Gardener'),
    ('gardener4', 'scrypt:32768:8:1$3RY2MpKJfMBL6y2M$face964ccc797ac918e011d307e0d1b33c4d63ebce4a241d912edc0d498c47861f36ec03a6a39394376a930a982434b2edfa03283f4ea20f0b292c6514fce8e0', 'Gardener'),
    ('gardener5', 'scrypt:32768:8:1$3RY2MpKJfMBL6y2M$face964ccc797ac918e011d307e0d1b33c4d63ebce4a241d912edc0d498c47861f36ec03a6a39394376a930a982434b2edfa03283f4ea20f0b292c6514fce8e0', 'Gardener'),
    ('staff1', 'scrypt:32768:8:1$3RY2MpKJfMBL6y2M$face964ccc797ac918e011d307e0d1b33c4d63ebce4a241d912edc0d498c47861f36ec03a6a39394376a930a982434b2edfa03283f4ea20f0b292c6514fce8e0', 'Staff'),
    ('staff2', 'scrypt:32768:8:1$3RY2MpKJfMBL6y2M$face964ccc797ac918e011d307e0d1b33c4d63ebce4a241d912edc0d498c47861f36ec03a6a39394376a930a982434b2edfa03283f4ea20f0b292c6514fce8e0', 'Staff'),
    ('staff3', 'scrypt:32768:8:1$3RY2MpKJfMBL6y2M$face964ccc797ac918e011d307e0d1b33c4d63ebce4a241d912edc0d498c47861f36ec03a6a39394376a930a982434b2edfa03283f4ea20f0b292c6514fce8e0', 'Staff'),
    ('admin', 'scrypt:32768:8:1$3RY2MpKJfMBL6y2M$face964ccc797ac918e011d307e0d1b33c4d63ebce4a241d912edc0d498c47861f36ec03a6a39394376a930a982434b2edfa03283f4ea20f0b292c6514fce8e0', 'Admin');

INSERT INTO gardener (gardener_id, username, first_name, last_name, address, email, phone_number, date_joined, status) VALUES
    (1, 'gardener1', 'John', 'Doe', '121 Main St', 'john.doe@example.com', '0271234567', '2024-01-01', 'Active'),
    (2, 'gardener2', 'Jane', 'Smith', '122 Main St', 'jane.smith@example.com', '0271235678', '2024-01-01', 'Active'),
    (3, 'gardener3', 'Joe', 'Jackson', '123 Main St', 'joe.jackson@example.com', '0271237890', '2024-01-01', 'Active'),
    (4, 'gardener4', 'Jim', 'Milly', '124 Main St', 'jim.milly@example.com', '0272345678', '2024-01-01', 'Active'),
    (5, 'gardener5', 'Jack', 'Johnson', '125 Main St', 'jack.johnson@example.com', '0272346789', '2024-01-01', 'Active');

INSERT INTO staff (staff_id, username, first_name, last_name, email, work_phone, hire_date, position, department, status) VALUES
    (6, 'staff1', 'Alice', 'Brown', 'alice.brown@example.com', '123-456-7895', '2024-01-01', 'Researcher', 'Botany', 'Active'),
    (7, 'staff2', 'Bob', 'Green', 'bob.green@example.com', '123-456-7896', '2024-01-01', 'Technician', 'Maintenance', 'Active'),
    (8, 'staff3', 'Charlie', 'Blue', 'charlie.blue@example.com', '123-456-7897', '2024-01-01', 'Agent', 'Operations', 'Active');

INSERT INTO administration (admin_id, username, first_name, last_name, email, work_phone, hire_date, position, department, status) VALUES
    (9, 'admin', 'Diana', 'White', 'diana.white@example.com', '123-456-7898', '2024-01-01', 'Manager', 'Administration', 'Active');

INSERT INTO weedGuide (common_name, scientific_name, weed_type, description, impacts, control_methods) VALUES
    ('Annual Poa', 'Poa annua', 'Grass', 'A samll grass often unnoticed in turf.','Can die off leaving bare ground, making turf look patchy.', 'Fungicide spraying, herbicides like Ethofumesate and Pendimethalin.'),
    ('Black nightshade', 'Solanum nigrum', 'Summer annual', 'Grows tall and leafy, creating competition with crops', 'Toxic, especially unripe berries; hard to seperate berries from peas at harvest','Cultivation, herbicides; resistant to some sulfonylurea herbicides and trifluralin.'),
    ('Blackberry', 'Rubus fruticosus', 'Scrub weed', 'Troublesome in pastures and forests, with hooks on stems.', 'Can trap woolly sheep;  seeds dispersed by birds.', 'Grazing by goats, herbicides like metsulfuron, triclopyr, picloram, and glyphosate.'),
    ('Bracken', 'Pteridium esculentum', 'Fern', 'Bracken is an invasive fern species in New Zealand, reproducing through spores and having a tough rhizome system.', 'Bracken is carcinogenic and competes with young trees in forestry, and invades hill-country pastures.', 'Control methods include cultivation, heavy treading by cattle, repeated mowing, and use of herbicides like glyphosate and asulam.'),
    ('Daisy', 'Bellis perennis', 'Rosette', 'Daisy is a well-known plant with white flowers and spoon-shaped leaves, mainly causing problems in lawns.', 'Daisies can dominate pastures in some regions, leading to low pasture production. Livestock generally avoid eating it.', 'Selective control in pastures is difficult. In turf, herbicides like clopyralid, triclopyr/picloram, and 2,4-D/dicamba mixes give good control.'),
    ('Dandelion', 'Taraxacum officinale', 'Rosette', 'Dandelion is a rosette-forming weed with yellow flowers, common in pastures and turf.', 'Not a major concern in pastures, but an eyesore in turf.', 'Herbicides like clopyralid, dicamba, and glyphosate can be used for control.'),
    ('Fathen', 'Chenopodium album', 'Annual', 'Tall, leafy weed that germinates in spring/summer.', 'Competitive in crops, some biotypes herbicide resistant.', 'Controlled by cultivation and herbicides, resistant types need alternative treatments.'),
    ('Fiddle Dock', 'Rumex pulcher', 'Perennial', 'Rosette-forming weed with fiddle-shaped leaves, common in turf.', 'Main dock species in turf, tolerates regular mowing.', 'Controlled by herbicides like mecoprop + ioxynil + bromoxynil in turf, asulam or thifensulfuron in pastures.'),
    ('Ivy', 'Hedera helix', 'Vine', 'Ivy is a vine-like weed commonly found in gardens and on buildings.', 'Can cause damage to structures and smother native vegetation.', 'Control methods include cutting and treating stumps with herbicides like glyphosate or triclopyr/picloram.'),
    ('Mallow', 'Malva spp', 'Perennial', 'Mallow is a group of short-lived perennial weeds often found in pastures and orchards.', 'Mildly toxic, animals avoid eating them, and they are tolerant of many herbicides.', 'No selective herbicides for pastures; flumetsulam, MCPA, 2,4-D/dicamba, and triclopyr/picloram can be effective.'),
    ('Manuka', 'Leptospermum scoparium', 'Perennial', 'Manuka is a native NZ scrub species with small leaves, often forming dense thickets.', 'Not a strong competitor as a seedling, but can grow several metres tall.', 'Susceptible to physical weed control and herbicides like glyphosate and metsulfuron.'),
    ('Mouse-ear Hawkweed', 'Pilosella officinarum', 'Perennial', 'Mouse-ear hawkweed has long hairs on foliage and forms dense mats in pastures.', 'Major problem in South Island high country, tolerant of low soil fertility and over-grazing.', 'Control is difficult; strategies include increasing fertiliser inputs and biological control agents.'),
    ('Ragwort', 'Jacobaea vulgaris', 'Biennial', 'Ragwort starts as a rosette and produces yellow flowers, problematic in cattle pastures.', 'Contains poisonous alkaloids, avoided by cattle, can dominate pastures.', 'Controlled by grazing with sheep or goats, keeping pastures dense, and herbicides like 2,4-D.'),
    ('Red Deadnettle', 'Lamium purpureum', 'Annual', 'Red dead-nettle has jagged leaves and produces lilac flowers, common in gardens and crops.', 'Non-stinging weed, tends to sprawl rather than grow upright.', 'Controlled by herbicides like bromoxynil in cereals and trifluralin in other crops.'),
    ('Redroot', 'Amaranthus powellii', 'Annual', 'Redroot is a tall, upright weed that can grow over a metre in height, common in warmer regions.', 'Summer annual, competitive in infested crops, prefers warmer conditions.', 'Susceptible to mowing, cultivation, and herbicides like atrazine, mesotrione, and glyphosate.'),
    ('Scarlet Pimpernel', 'Anagallis arvensis', 'Annual', 'Scarlet pimpernel is a small, scrambling weed with orange flowers, common in gardens and crops.', 'Can germinate and grow year-round, occasionally problematic in high densities.', 'Controlled by cultivation and most herbicides, but resistant to clopyralid.'),
    ('Tauhinu', 'Ozothamnus leptophyllus', 'Perennial', 'Tauhinu is a native NZ scrub weed with small, rounded leaves, mainly problematic in eastern districts.', 'Similar to manuka but with white undersides on leaves and fluffy seed heads.', 'Controlled by metsulfuron, triclopyr, and triclopyr/picloram, but resistant to glyphosate.'),
    ('Tradescantia', 'Tradescantia fluminensis', 'Perennial', 'Tradescantia is a succulent, brittle weed forming thick mats in moist, shady areas.', 'Causes environmental problems, stops new seedlings from establishing, and can cause allergic reactions in animals.', 'Control is difficult; best treated with triclopyr, but re-treatment may be necessary.'),
    ('Turf Speedwell', 'Veronica serpyllifolia', 'Perennial', 'Turf speedwell is a small perennial weed with white flowers, common in turf and pastures.', 'Forms dense mats in turf, tolerant of many turf herbicides.', 'Best controlled with a mixture of mecoprop and ioxynil, may require re-treatment.'),
    ('Twin Cress', 'Lepidium didymum', 'Annual', 'Twin cress is a small weed that starts as a rosette and sends out prostrate stems, common in crops and gardens.', 'Can cause milk taint in dairy farms, forms mats on the ground.', 'Controlled by MCPB or MCPA in young pastures, flumetsulam before the 4-leaf stage, and various turf herbicides in lawns.');

INSERT INTO weedImage (weed_id, image_url, is_primary) VALUES
    (1, 'https://d2ub1k1pknil0e.cloudfront.net/media/images/annual_poa_N1_.width-400.format-webp.webp', TRUE),
    (2, 'https://d2ub1k1pknil0e.cloudfront.net/media/images/nightshadeB1.width-400.format-webp.webp', TRUE),
    (3, 'https://d2ub1k1pknil0e.cloudfront.net/media/images/blackberryB1.width-400.format-webp.webp', TRUE),
    (4, 'https://d2ub1k1pknil0e.cloudfront.net/media/images/bracken1.width-400.format-webp.webp', TRUE),
    (5, 'https://d2ub1k1pknil0e.cloudfront.net/media/images/daisy_1.width-400.format-webp.webp', TRUE),
    (6, 'https://d2ub1k1pknil0e.cloudfront.net/media/images/dandelionB1.width-400.format-webp.webp', TRUE),
    (7, 'https://d2ub1k1pknil0e.cloudfront.net/media/images/fathen_N1.width-400.format-webp.webp', TRUE),
    (8, 'https://d2ub1k1pknil0e.cloudfront.net/media/images/fiddleB2.width-400.format-webp.webp', TRUE),
    (9, 'https://d2ub1k1pknil0e.cloudfront.net/media/images/ivy_N1.width-400.format-webp.webp', TRUE),
    (10, 'https://d2ub1k1pknil0e.cloudfront.net/media/images/mallowB1.width-400.format-webp.webp', TRUE),
    (11, 'https://d2ub1k1pknil0e.cloudfront.net/media/images/manuka_N2.width-400.format-webp.webp', TRUE),
    (12, 'https://d2ub1k1pknil0e.cloudfront.net/media/images/mouse-ear_hawkweed_N1.width-400.format-webp.webp', TRUE),
    (13, 'https://d2ub1k1pknil0e.cloudfront.net/media/images/ragwort_N1.width-400.format-webp.webp', TRUE),
    (14, 'https://d2ub1k1pknil0e.cloudfront.net/media/images/red_dead-nettle_N1.width-400.format-webp.webp', TRUE),
    (15, 'https://d2ub1k1pknil0e.cloudfront.net/media/images/redroot_N1.width-400.format-webp.webp', TRUE),
    (16, 'https://d2ub1k1pknil0e.cloudfront.net/media/images/scarletB1.width-400.format-webp.webp', TRUE),
    (17, 'https://d2ub1k1pknil0e.cloudfront.net/media/images/tauhinuB2.width-400.format-webp.webp', TRUE),
    (18, 'https://d2ub1k1pknil0e.cloudfront.net/media/images/wandJewB1.width-400.format-webp.webp', TRUE),
    (19, 'https://d2ub1k1pknil0e.cloudfront.net/media/images/turf_speedwell_N1.width-400.format-webp.webp', TRUE),
    (20, 'https://d2ub1k1pknil0e.cloudfront.net/media/images/Twin_cress_N1.width-400.format-webp.webp', TRUE);
    