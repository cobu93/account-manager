CREATE DATABASE account_manager;

USE account_manager;

CREATE TABLE account(
    id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    email VARCHAR(100) NOT NULL
) ENGINE=INNODB;

CREATE TABLE transaction(
    id INT PRIMARY KEY NOT NULL,
    account_id INT NOT NULL,
    op_date DATE NOT NULL,
    amount FLOAT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES account(id) ON DELETE CASCADE
) ENGINE=INNODB;

INSERT INTO account(email) VALUES ("urielcoro@gmail.com");

GRANT ALL PRIVILEGES ON account_manager.* TO "accmgr";