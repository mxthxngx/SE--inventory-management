
DROP TABLE IF EXISTS orderDetails;
DROP TABLE IF EXISTS stockDetails;
DROP TABLE IF EXISTS auth;
CREATE TABLE orderDetails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_order TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    partner_name TEXT NOT NULL,
    destination TEXT NOT NULL,
    item_name TEXT UNIQUE NOT NULL,
    items INTEGER,
    item_status TEXT NOT NULL
);

CREATE TABLE stockDetails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    items_available INTEGER,
    items_total INTEGER NOT NULL,
    action_needed TEXT NOT NULL,
    FOREIGN KEY (item_name) REFERENCES orderDetails(item_name)

);

CREATE TABLE auth(
    username varchar(20) PRIMARY KEY,
    passw varchar(20) NOT NULL
)