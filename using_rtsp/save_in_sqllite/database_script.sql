create database anprresults;

use anprresults ;
CREATE TABLE VehicleTransactions (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    vehiclenumber VARCHAR(255) NOT NULL,
    dateoftransaction DATETIME DEFAULT CURRENT_TIMESTAMP,
    vehicleimgpath VARCHAR(255),
    numberplateimgpath VARCHAR(255)
);

select * from VehicleTransactions
