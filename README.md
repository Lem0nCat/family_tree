# Family Tree

## Описание проекта
**Family Tree** — это небольшое веб-приложение для создания генеалогического дерева. Проект позволяет визуализировать семейные связи, анализировать семейные данные и проводить исследования структуры семьи.

## Основные функции
- Создание и управление генеалогическим древом.
- Анализ данных о семье:
  - Количество членов семьи.
  - Количество поколений.
  - Распределение родственников по полу (мужчины и женщины).

## Процедуры для анализа данных

### Подсчет количества членов семьи
Определяет общее количество членов семьи, добавленных пользователем.

```sql
CREATE PROCEDURE GetFamilyMemberCountByUser
    @CreatorUserId INT
AS
BEGIN
    SELECT COUNT(*) AS TotalFamilyMembers
    FROM tree_person
    WHERE creator_user_id = @CreatorUserId;
END;
```

### Подсчет количества поколений в семье
Определяет количество поколений, зарегистрированных в генеалогическом древе пользователя.

```sql
CREATE PROCEDURE GetGenerationCountByUser
    @CreatorUserId INT
AS
BEGIN
    SELECT COUNT(*) AS TotalGenerations
    FROM tree_generation
    WHERE creator_user_id = @CreatorUserId;
END;
```

### Подсчет количества родственников женского пола
Определяет количество женщин в семье, начиная с самого младшего поколения и поднимаясь вверх по материнским линиям.

```sql
CREATE PROCEDURE GetFemaleRelativesCount
    @UserId INT
AS
BEGIN
    DECLARE @LatestGenerationId INT;
    SELECT TOP 1 @LatestGenerationId = tg.id
    FROM tree_generation tg
    WHERE tg.creator_user_id = @UserId
    ORDER BY tg.generation_number DESC;

    WITH FemaleAncestors AS (
        SELECT tp.id, tp.mother_id
        FROM tree_person tp
        WHERE tp.generation_id = @LatestGenerationId
          AND tp.gender = 'female'
        
        UNION ALL

        SELECT tp.id, tp.mother_id
        FROM tree_person tp
        INNER JOIN FemaleAncestors fa ON tp.id = fa.mother_id
        WHERE tp.gender = 'female'
    )
    SELECT COUNT(DISTINCT id) AS FemaleRelativesCount
    FROM FemaleAncestors;
END;
```

### Подсчет количества родственников мужского пола
Определяет количество мужчин в семье, начиная с самого младшего поколения и поднимаясь вверх по отцовским линиям.

```sql
CREATE PROCEDURE GetMaleRelativesCount
    @UserId INT
AS
BEGIN
    DECLARE @LatestGenerationId INT;
    SELECT TOP 1 @LatestGenerationId = tg.id
    FROM tree_generation tg
    WHERE tg.creator_user_id = @UserId
    ORDER BY tg.generation_number DESC;

    WITH MaleAncestors AS (
        SELECT tp.id, tp.father_id
        FROM tree_person tp
        WHERE tp.generation_id = @LatestGenerationId
          AND tp.gender = 'male'
        
        UNION ALL

        SELECT tp.id, tp.father_id
        FROM tree_person tp
        INNER JOIN MaleAncestors ma ON tp.id = ma.father_id
        WHERE tp.gender = 'male'
    )
    SELECT COUNT(DISTINCT id) AS MaleRelativesCount
    FROM MaleAncestors;
END;
```
