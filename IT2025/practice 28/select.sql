-- 1. Отримати список усіх курсів
SELECT * FROM Courses;

-- 2. Отримати список усіх слухачів
SELECT * FROM Students;

-- 3. Отримати список усіх інструкторів
SELECT * FROM Instructors;

-- 4. Переглянути слухачів, які записані на курс "Основи програмування"
SELECT s.FirstName, s.LastName, c.CourseName
FROM Students s
JOIN CourseStudent cs ON s.StudentID = cs.StudentID
JOIN Courses c ON cs.CourseID = c.CourseID
WHERE c.CourseName = 'Основи програмування';

-- 5. Переглянути курси, на які призначений інструктор "Марія Гриценко"
SELECT c.CourseName, c.StartDate, c.EndDate
FROM Courses c
JOIN CourseInstructor ci ON c.CourseID = ci.CourseID
JOIN Instructors i ON ci.InstructorID = i.InstructorID
WHERE i.FirstName = 'Марія' AND i.LastName = 'Гриценко';

-- 6. Порахувати кількість слухачів на кожному курсі
SELECT c.CourseName, COUNT(cs.StudentID) AS NumberOfStudents
FROM Courses c
LEFT JOIN CourseStudent cs ON c.CourseID = cs.CourseID
GROUP BY c.CourseID;

-- 7. Порахувати кількість курсів для кожного інструктора
SELECT i.FirstName, i.LastName, COUNT(ci.CourseID) AS NumberOfCourses
FROM Instructors i
LEFT JOIN CourseInstructor ci ON i.InstructorID = ci.InstructorID
GROUP BY i.InstructorID;

-- 8. Отримати список курсів, які тривають у квітні 2025 року
SELECT * FROM Courses
WHERE '2025-04-01' BETWEEN StartDate AND EndDate;

-- 9. Отримати список слухачів, які ще не записані на жоден курс
SELECT * FROM Students s
WHERE NOT EXISTS (
    SELECT 1 FROM CourseStudent cs WHERE s.StudentID = cs.StudentID
);

-- 10. Видалити всі записи про слухача з ID = 3
DELETE FROM Students WHERE StudentID = 3;

-- 11. Оновити опис курсу "Веб-розробка"
UPDATE Courses
SET Description = 'Розширений курс з веб-розробки для досвідчених користувачів'
WHERE CourseName = 'Веб-розробка';

-- 12. Додати новий курс і відразу призначити інструктора
INSERT INTO Courses (CourseName, Description, StartDate, EndDate)
VALUES ('Кібербезпека', 'Курс із основ інформаційної безпеки', '2025-05-01', '2025-06-01');

INSERT INTO CourseInstructor (CourseID, InstructorID, AssignmentDate)
VALUES (4, 1, '2025-04-15');

-- 13. Знайти слухачів, які записані більше ніж на 1 курс
SELECT s.FirstName, s.LastName, COUNT(cs.CourseID) AS Courseid
FROM Students s
JOIN CourseStudent cs ON s.StudentID = cs.StudentID
GROUP BY s.FirstName, s.LastName, Courseid
HAVING Courseid > 1;

-- 14. Отримати список інструкторів із зазначенням їхніх експертиз
SELECT * FROM Instructors;

-- 15. Видалити курс із ID = 2
DELETE FROM Courses WHERE CourseID = 2;

-- 16. Показати всі курси, на які ще не призначені інструктори
SELECT * FROM Courses c
WHERE NOT EXISTS (
    SELECT 1 FROM CourseInstructor ci WHERE c.CourseID = ci.CourseID
);

-- 17. Додати нового слухача і записати його на курс
INSERT INTO Students (FirstName, LastName, Email, PhoneNumber)
VALUES ('Наталія', 'Мельник', 'nataliya.melnyk@example.com', '+380501234567');

INSERT INTO CourseStudent (CourseID, StudentID, EnrollmentDate)
VALUES (1, 4, '2025-04-10');

-- 18. Порахувати кількість курсів, які тривають у 2025 році
SELECT COUNT(*) AS CoursesIn2025
FROM Courses
WHERE EXTRACT(YEAR FROM StartDate) = 2025;

-- 19. Показати слухачів із поштою на домені "@example.com"
SELECT * FROM Students
WHERE Email LIKE '%@example.com';

-- 20. Видалити всі дані про інструкторів, які не ведуть жодного курсу
DELETE FROM Instructors
WHERE NOT EXISTS (
    SELECT 1 FROM CourseInstructor ci WHERE ci.InstructorID = Instructors.InstructorID
);
