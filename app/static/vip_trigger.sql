SELECT * FROM "user"

SELECT * FROM "order"

SELECT COUNT(id) FROM "order" WHERE "order".user_id IN (SELECT 24)
AND "order".status = 'Paga' 


CREATE FUNCTION user_vip()
RETURNS TRIGGER
LANGUAGE PLPGSQL
AS 
$$
BEGIN
	IF ((SELECT COUNT(id) FROM "order" WHERE "order".user_id IN
		(SELECT user_id FROM NEW)AND "order".status = 'Paga') > 10) THEN 
		UPDATE "user" SET is_vip = TRUE WHERE id = (SELECT user_id FROM NEW);
	END IF;
END;
$$



CREATE TRIGGER atualiza_vip
AFTER INSERT ON "order"
FOR EACH ROW
EXECUTE PROCEDURE user_vip()