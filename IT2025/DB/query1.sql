-- Створення таблиці Engagements
CREATE TABLE Engagements (
    EngagementID SERIAL PRIMARY KEY, -- Унікальний ідентифікатор
    Date DATE NOT NULL, -- Дата зіткнення
    Location VARCHAR(100) NOT NULL, -- Локація
    EnemyLosses INT NOT NULL, -- Втрати ворога
    FriendlyLosses INT NOT NULL, -- Власні втрати
    Outcome VARCHAR(50) NOT NULL -- Результат (наприклад, 'Victory', 'Defeat', 'Stalemate')
);

-- Заповнення таблиці 5 записами
INSERT INTO Engagements (Date, Location, EnemyLosses, FriendlyLosses, Outcome)
VALUES
    ('2025-01-15', 'Kyiv', 150, 10, 'Victory'),
    ('2025-01-16', 'Kharkiv', 200, 25, 'Victory'),
    ('2025-01-17', 'Lviv', 50, 5, 'Stalemate'),
    ('2025-01-18', 'Odessa', 100, 20, 'Victory'),
    ('2025-01-19', 'Donetsk', 300, 50, 'Defeat');

-- Перевірка даних у таблиці
SELECT * FROM Engagements;
