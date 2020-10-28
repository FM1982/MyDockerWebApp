USE DockerWebApp;
DROP PROCEDURE IF EXISTS RetrieveDataWebApp;

DELIMITER $$
USE DockerWebApp$$
CREATE PROCEDURE RetrieveDataWebApp (
	IN myp_entry_user_id int(11)
)
BEGIN
	select * from dbentries where entry_user_id = myp_entry_user_id;
END$$
DELIMITER;
