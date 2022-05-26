CREATE OR REPLACE PROCEDURE cart_insert_data("CarId" integer, "CartId" integer)
LANGUAGE SQL
AS $$
INSERT INTO public.cart_cartitem(car_id,cart_id) VALUES ("CarId", "CartId");
$$;