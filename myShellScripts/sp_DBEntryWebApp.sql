USE DockerWebApp;
DROP PROCEDURE IF EXISTS EntryWebApp;

DELIMITER $$
USE DockerWebApp$$
CREATE DEFINER=root@localhost PROCEDURE EntryWebApp (
	IN myp_entry_name VARCHAR(30),
	IN myp_entry_surname VARCHAR(30),
	IN myp_entry_age int(3),
	IN myp_entry_email VARCHAR(45),
	IN myp_entry_street VARCHAR(30),
	IN myp_entry_houseno VARCHAR(30),
	IN myp_entry_postalcode VARCHAR(10),
	IN myp_entry_country VARCHAR(30),
	IN myp_entry_phonenumber VARCHAR(30),
	IN myp_entry_user_id int(11)
)
BEGIN
	INSERT INTO dbentries(
		entry_name,
		entry_surname,
		entry_age,
		entry_email,
		entry_street,
		entry_houseno,
		entry_postalcode,
		entry_country,
		entry_phonenumber,
		entry_user_id
	)
	VALUES
	(
		myp_entry_name,
		myp_entry_surname,
		myp_entry_age,
		myp_entry_email,
		myp_entry_street,
		myp_entry_houseno,
		myp_entry_postalcode,
		myp_entry_country,
		myp_entry_phonenumber,
		myp_entry_user_id
	);
END$$

