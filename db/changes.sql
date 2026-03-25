UPDATE cases
SET status = 'in_progress',
    updated_at = now()
WHERE case_id IN (1, 2, 3, 4, 5);

INSERT INTO customers (name, email, country, updated_at)
VALUES
  ('Customer 31', 'customer31@example.com', 'US', now()),
  ('Customer 32', 'customer32@example.com', 'CA', now());

INSERT INTO cases (customer_id, title, description, status, updated_at)
VALUES
  (1, 'Billing retry issue', 'payments billing retry follow-up', 'open', now()),
  (2, 'Audit log gap', 'audit reconciliation evidence review', 'open', now()),
  (3, 'Compliance review', 'compliance control confirmation', 'in_progress', now()),
  (4, 'Onboarding delay', 'customer onboarding blocked by verification', 'open', now()),
  (5, 'Fraud signal review', 'fraud trigger needs analysis', 'open', now()),
  (6, 'AML screening update', 'AML checks need refresh', 'in_progress', now()),
  (31, 'New customer onboarding', 'onboarding for new enterprise customer', 'open', now()),
  (31, 'Payment mapping issue', 'payments reconciliation setup', 'open', now()),
  (32, 'Compliance intake', 'compliance onboarding validation', 'open', now()),
  (32, 'Fraud monitoring setup', 'fraud and AML monitoring setup', 'open', now());