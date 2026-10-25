# Identity Resolution Prompt

## Objective
Identify all current and historical identifiers associated with the target user for case audit.

## Inputs
- Case Request Email, Name, Phone, and Request Timestamp (`requested_at`)
- `user_identities.csv` (Current identities mapping `user_id`, `email`, `phone`, `email_hash`, `created_at`)
- `user_audit_log.csv` (Identity change history including old email, new email, change timestamp)

## Output Schema
Provide a structured JSON object containing:
- `user_id`: Stable internal identifier
- `primary_email`: Email at request time
- `historical_emails`: List of previous emails used by the user
- `email_hashes`: List of SHA-256 hashes of primary and historical emails
- `phones`: List of associated phone numbers
- `aliases`: List of alternate account usernames or handles
