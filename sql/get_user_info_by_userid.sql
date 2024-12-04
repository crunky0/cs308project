SELECT userid, username, name, surname, email, taxid, homeaddress
FROM users
WHERE userid = :userid;