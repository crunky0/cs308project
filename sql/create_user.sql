INSERT INTO users (username, password, role, name, surname, email, taxid, homeaddress)
VALUES (:username, :password, :role, :name, :surname, :email, :taxid, :homeaddress)
RETURNING userid;
