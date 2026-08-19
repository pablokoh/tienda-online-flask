-- Migración manual para una base creada con las semanas 1-3 del tutorial.
-- Ejecutar una sola vez sobre la base tienda_online existente.

ALTER TABLE productos
ADD COLUMN IF NOT EXISTS imagen VARCHAR(255);

UPDATE productos
SET imagen = 'default_product.svg'
WHERE imagen IS NULL OR imagen = '';

ALTER TABLE productos
ALTER COLUMN imagen SET DEFAULT 'default_product.svg';

ALTER TABLE productos
ALTER COLUMN imagen SET NOT NULL;
