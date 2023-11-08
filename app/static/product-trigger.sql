CREATE FUNCTION atualiza_status()
RETURNS TRIGGER
AS $$
	BEGIN
		IF NEW.quantity >= 10 THEN
			UPDATE product SET status = 'Estoque Normal' WHERE id = NEW.product_id;
		END IF;
		IF NEW.quantity < 10 THEN
			UPDATE product SET status = 'Estoque Baixo' WHERE id = NEW.product_id;
		END IF;
		RETURN NEW;
	END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER novo_registro_estoque
AFTER INSERT OR UPDATE
ON stock
FOR EACH ROW EXECUTE PROCEDURE atualiza_status()


