
# DROP TABLE IF EXISTS `origin_data`;
# DROP TABLE IF EXISTS `origin_data1`;
# DROP TABLE IF EXISTS `car_has_recall_current`;
# DROP TABLE IF EXISTS `company_has_recall_current`;
# DROP TABLE IF EXISTS `company`;
# DROP TABLE IF EXISTS `domestic_international`;
# DROP TABLE IF EXISTS `recall_current_has_recall_reason`;
# DROP TABLE IF EXISTS `car`;
# DROP TABLE IF EXISTS `ev`;
# DROP TABLE IF EXISTS `recall_key`;
# DROP TABLE IF EXISTS `recall_current`;


-- 1. origin_data (CSV 원본 데이터 넣는 테이블)
# CREATE TABLE origin_data (
#     company VARCHAR(100),
#     car_name VARCHAR(100),
#     prod_period_from DATE,
#     prod_period_to DATE,
#     recall_start DATE,
#     recall_reason TEXT
# );


-- 1. recall_current (parent)
CREATE TABLE recall_current (
    current_id INT PRIMARY KEY AUTO_INCREMENT,
    prod_period_from DATE,
    prod_period_to DATE,
    recall_start DATE,
    recall_reason TEXT
);


-- 1. ev


CREATE TABLE ev (
    ev_id INT PRIMARY KEY AUTO_INCREMENT,
    is_ev ENUM('EV', 'Non-EV') NOT NULL
);

-- 2. domestic_international
CREATE TABLE domestic_international (
    di_id INT PRIMARY KEY AUTO_INCREMENT,
    is_di ENUM('Domestic', 'International') NOT NULL
);

-- 3. company
CREATE TABLE company (
    company_id INT PRIMARY KEY AUTO_INCREMENT,
    comp_name VARCHAR(45) NOT NULL,
    domestic_international_di_id INT,
    FOREIGN KEY (domestic_international_di_id) REFERENCES domestic_international(di_id)
);

-- 4. car
CREATE TABLE car (
    car_id INT PRIMARY KEY AUTO_INCREMENT,
    car_name VARCHAR(45) NOT NULL,
    ev_ev_id INT,
    FOREIGN KEY (ev_ev_id) REFERENCES ev(ev_id)
);



-- 6. recall_key
CREATE TABLE recall_key (
    reason_id INT PRIMARY KEY AUTO_INCREMENT,
    keyword VARCHAR(20) NOT NULL
);

-- 7. car_has_recall_current
CREATE TABLE car_has_recall_current (
    car_car_id INT,
    recall_current_current_id INT,
    PRIMARY KEY (car_car_id, recall_current_current_id),
    FOREIGN KEY (car_car_id) REFERENCES car(car_id),
    FOREIGN KEY (recall_current_current_id) REFERENCES recall_current(current_id)
);

-- 8. company_has_recall_current
CREATE TABLE company_has_recall_current (
    company_company_id INT,
    recall_current_current_id INT,
    PRIMARY KEY (company_company_id, recall_current_current_id),
    FOREIGN KEY (company_company_id) REFERENCES company(company_id),
    FOREIGN KEY (recall_current_current_id) REFERENCES recall_current(current_id)
);

-- 9. recall_current_has_recall_reason
CREATE TABLE recall_current_has_recall_reason (
    recall_current_current_id INT,
    recall_reason_reason_id INT,
    PRIMARY KEY (recall_current_current_id, recall_reason_reason_id),
    FOREIGN KEY (recall_current_current_id) REFERENCES recall_current(current_id),
    FOREIGN KEY (recall_reason_reason_id) REFERENCES recall_key(reason_id)
);

