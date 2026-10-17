---
name: sql-schema-query-condenser
description: SQL relational schema and query plan condenser. Serializes verbose DDL migrations and EXPLAIN QUERY PLAN execution trees into compact type-bracket notation and flat operator pipelines, slashing database context by 65-75%.
---

# SQL Schema & Query Plan Condenser (`sql-schema-query-condenser`)

Standard SQL `CREATE TABLE` DDL and `EXPLAIN QUERY PLAN` outputs are laden with formatting keywords (`CONSTRAINT`, `DEFAULT`, `CHECK`, ASCII box drawings, and recursive indentation).

This skill compresses relational schemas and execution plans into high-density mathematical notation.

---

## 1. Schema Representation Comparison

### Verbose DDL (140 tokens):
```sql
CREATE TABLE user_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    session_token VARCHAR(64) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    is_revoked BOOLEAN DEFAULT 0 NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE INDEX idx_user_sessions_token ON user_sessions(session_token);
```

### Compact Type-Bracket Signature (28 tokens — 80% reduction):
```text
user_sessions[id:INT*, user_id:INT->users.id(cascade), token:STR(64)!(idx), created:TS(now), expires:TS, revoked:BOOL(0)]
```

### Key Legend:
- `*` : Primary Key
- `!` : Unique Constraint
- `->` : Foreign Key Reference
- `(idx)` : Indexed Column
- `(val)` : Default Value

---

## 2. Query Plan Tree Compression

### Verbose SQLite `EXPLAIN QUERY PLAN` (85 tokens):
```text
QUERY PLAN
|--SEARCH users USING INDEX idx_users_email (email=?)
`--SCAN user_sessions
   `--SEARCH user_sessions USING AUTOMATIC COVERING INDEX (user_id=?)
```

### Compact Pipeline Operator (18 tokens — 78% reduction):
```text
INDEX_SEARCH(users.idx_users_email:email) -> AUTO_INDEX_JOIN(user_sessions.user_id)
```

---

## 3. Database Triage Rules

1. **Schema Hydration:**
   - When inspecting database structure, output compact type-bracket signatures.
   - Never paste hundreds of lines of raw DDL migrations into chat.
2. **Query Optimization:**
   - Condense query plans to operator chains: `SCAN(tbl)` (bad, full scan) vs `INDEX_SEARCH(tbl.col)` (good).
   - Flag missing indices using 1-line suggestions: `+INDEX(tbl.col)`.

## Related & Interoperating Skills
- **`database-sql-engineering`**: SQLite performance tuning (WAL mode, PRAGMAs, indexing), PostgreSQL/MySQL schema design, query plan analysis, ...
- **`claude-silent-dispatch`**: Eliminates pre-tool narration, commentary, and conversational play-by-plays in Claude Code, executing tool cal...
- **`network-packet-stream-condenser`**: Network packet stream and PCAP trace condenser. Flattens verbose tshark and tcpdump protocol dissection trees ...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.
