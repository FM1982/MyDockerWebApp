USE DockerWebApp;
DROP PROCEDURE IF EXISTS RetrieveDataWebApp;

DELIMITER $$
USE DockerWebApp$$
CREATE PROCEDURE RetrieveDataWebApp (
	IN myrd_entry_id bigint
)
BEGIN
	select * from dbentries where entry_id = myrd_entry_id;
END$$

