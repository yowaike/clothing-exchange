-- 1. Получить все вещи
SELECT * FROM items;

-- 2. Получить только доступные для обмена вещи
SELECT * FROM items
WHERE is_available = 1;

-- 3. Найти вещь по названию
SELECT * FROM items
WHERE item_name LIKE '%кофта%';

-- 4. Найти вещи определённого размера
SELECT * FROM items
WHERE size = 's';

-- 5. Найти вещи по состоянию
SELECT * FROM items
WHERE condition = 'нормальное';

-- 6. Получить вещи конкретного владельца
SELECT * FROM items
WHERE owner_name = 'сашик';

-- 7. Посчитать общее количество вещей
SELECT COUNT(*) AS total_items
FROM items;

-- 8. Посчитать количество доступных вещей
SELECT COUNT(*) AS available_items
FROM items
WHERE is_available = 1;

-- 9. Получить всех пользователей
SELECT * FROM users;

-- 10. Найти пользователя по email
SELECT * FROM users
WHERE email = 'arrosasha@gmail.com';

-- 11. Получить заявки на обмен вместе с информацией о вещах
SELECT exchanges.id, items.item_name, exchanges.status
FROM exchanges
JOIN items ON exchanges.item_id = items.id;

-- 12. Посчитать количество заявок по каждому статусу
SELECT status, COUNT(*) AS request_count
FROM exchanges
GROUP BY status;