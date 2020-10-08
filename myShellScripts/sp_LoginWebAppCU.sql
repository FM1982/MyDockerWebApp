USE DockerWebApp;
DROP PROCEDURE IF EXISTS LoginWebAppCU;

DELIMITER $$
USE DockerWebApp$$
CREATE DEFINER=root@localhost PROCEDURE LoginWebAppCU (
	IN myp_name VARCHAR(30),
	IN myp_username VARCHAR(30),
	IN myp_password VARCHAR(255)
)
BEGIN
	IF ( select exists ( select 1 from credentials where myuser_username = myp_username ) ) THEN
		select 'Username Exists !!';
	ELSE
		INSERT INTO credentials
		(
			myuser_name,
			myuser_username,
			myuser_password
		)
		VALUES
		(
			myp_name,
			myp_username,
			myp_password
		);
	END IF;
END$$
