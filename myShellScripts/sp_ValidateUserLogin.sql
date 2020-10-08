USE DockerWebApp;
DROP PROCEDURE IF EXISTS ValidateUserLogin;

DELIMITER $$
USE DockerWebApp$$
CREATE DEFINER=root@localhost PROCEDURE ValidateUserLogin (
	IN myp_username VARCHAR(30)
)
BEGIN
	select * from credentials where myuser_username = myp_username;
END$$

