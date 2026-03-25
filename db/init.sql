CREATE TABLE customers (
  customer_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  country TEXT NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE cases (
  case_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  customer_id BIGINT NOT NULL REFERENCES customers(customer_id),
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  status TEXT NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX idx_customers_updated_at ON customers(updated_at);
CREATE INDEX idx_cases_updated_at ON cases(updated_at);
CREATE INDEX idx_cases_customer_id ON cases(customer_id);


INSERT INTO customers (name, email, country, updated_at)
SELECT
  'Customer ' || gs,
  'customer' || gs || '@example.com',
  CASE
    WHEN gs % 5 = 0 THEN 'US'
    WHEN gs % 5 = 1 THEN 'CA'
    WHEN gs % 5 = 2 THEN 'UK'
    WHEN gs % 5 = 3 THEN 'DE'
    ELSE 'AU'
  END,
  now() - ((gs % 30) || ' days')::interval
FROM generate_series(1, 30) AS gs;



INSERT INTO cases (customer_id, title, description, status, updated_at)
SELECT
  ((gs - 1) % 30) + 1,
  CASE
    WHEN gs % 8 = 0 THEN 'Billing discrepancy investigation'
    WHEN gs % 8 = 1 THEN 'Audit trail review'
    WHEN gs % 8 = 2 THEN 'Compliance evidence request'
    WHEN gs % 8 = 3 THEN 'Payments delay follow-up'
    WHEN gs % 8 = 4 THEN 'Reconciliation mismatch'
    WHEN gs % 8 = 5 THEN 'Onboarding setup issue'
    WHEN gs % 8 = 6 THEN 'Fraud alert review'
    ELSE 'AML verification check'
  END,
  'Case #' || gs || ' covering billing audit compliance payments reconciliation onboarding fraud AML workflows.',
  CASE
    WHEN gs % 3 = 0 THEN 'open'
    WHEN gs % 3 = 1 THEN 'in_progress'
    ELSE 'closed'
  END,
  now() - ((gs % 30) || ' days')::interval
FROM generate_series(1, 200) AS gs;