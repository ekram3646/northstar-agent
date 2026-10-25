# Evidence Analysis Prompt

## Objective
Reconstruct resource states and event timelines as of `audit_at` for resolved user identifiers.

## Evidence Categories
1. Primary & Secondary Databases (Account Service, Order Service, Analytics)
2. Support Attachments & Communication Records
3. Search Indexes (ElasticSearch / Solr exports)
4. Analytics & Data Warehouse Exports (BigQuery / S3 exports)
5. Log Files & Audit Trails
6. Backups & Disaster Recovery Snapshots
7. Active Data Flows (Sync, Replication, Import Jobs)

## Analysis Rules
- Events occurring AFTER `audit_at` must NOT be used to claim state at `audit_at`.
- Active sync processes can recreate deleted data; identify system and job names.
- Check tombstones for prohibited direct PII (emails, names, phone numbers, email hashes).
