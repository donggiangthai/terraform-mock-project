CREATE OR REPLACE PROCEDURE cart_delete_data("CarId" integer, "CartId" integer)
LANGUAGE SQL
AS $$
DELETE FROM public.cart_cartitem
WHERE car_id = "CarId" AND cart_id = "CartId";
$$;