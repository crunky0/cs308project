SELECT userid, username, name, surname, email, taxid, homeaddress, role
FROM users
WHERE userid = :userid;