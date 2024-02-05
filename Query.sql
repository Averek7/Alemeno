-- DROP TABLE Customer;
-- DROP TABLE Loan;
-- DROP TABLE IF EXISTS LOAN;

-- CREATE TABLE Customer(
--     Customer_ID SERIAL PRIMARY KEY,
--     FirstName TEXT,
--     LastName TEXT,
--     Age INTEGER NOT NULL,
--     PhoneNumber NUMERIC(10) NOT NULL,
--     MonthlySalary INTEGER NOT NULL,
--     ApprovedLimit INTEGER NOT NULL
-- );

-- CREATE TABLE Loan (
--     Loan_ID INTEGER NOT NULL,
--     Customer_ID INTEGER NOT NULL,
--     LoanAmount NUMERIC NOT NULL,
--     Tenure INTEGER NOT NULL,
--     InterestRate DECIMAL(5, 2) NOT NULL,
--     MonthlyPayment DECIMAL(10, 2) NOT NULL,
--     EMIsOnTime INTEGER NOT NULL,
--     DateOfApproval TEXT,
--     EndDate TEXT
-- );

	
-- copy Customer from 'E:\Projects\Submission\Alemeno\alemenoBackend\customer_data.csv' DELIMITER ',' CSV HEADER;
-- copy Loan from 'E:\Projects\Submission\Alemeno\alemenoBackend\loan_data.csv' DELIMITER ',' CSV HEADER;


