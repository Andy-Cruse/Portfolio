-- Instagram wishes to find the oldest users and reward them.
-- Find the 5 oldest users in the intstagram DB.
SELECT 
    username, created_at AS 'Date Created'
FROM
    users
ORDER BY created_at
LIMIT 5;

-- Instagram wants to schedule an ad campaign but isn't sure
-- when the best time is to do so.
-- Find which day of the week has the most users registering.
SELECT 
    DAYNAME(created_at) AS day_of_week, COUNT(*) AS count
FROM
    users
GROUP BY day_of_week
ORDER BY count DESC;

-- Instagram wants to target users that are inactive with
-- an email campaign.
-- Find the users that have never posted a photo.
SELECT 
    username, image_url
FROM
    users
        LEFT JOIN
    photos ON users.id = photos.user_id
WHERE
    image_url IS NULL;

-- Instagram is running a contest to see who's post has
-- the most likes.
-- Find out who won.
SELECT 
    username, COUNT(*) AS num_of_likes, image_url AS post
FROM
    likes
        INNER JOIN
    users ON users.id = likes.user_id
        INNER JOIN
    photos ON photos.user_id = users.id
GROUP BY username
ORDER BY num_of_likes DESC
LIMIT 1;

-- Instagram's investor's want to know...
-- Find out how much the average user posts
SELECT 
    AVG(num_of_posts)
FROM
    (SELECT 
        COUNT(*) AS num_of_posts
    FROM
        photos
    INNER JOIN users ON users.id = photos.user_id
    GROUP BY username) AS avg_table;
    
-- A brand wants to know which hashtags to use in a post.
-- Find the top 5 most commonly used hashtags
SELECT 
    tag_name, COUNT(*) AS num_of_uses
FROM
    tags
        INNER JOIN
    photo_tags ON tags.id = photo_tags.tag_id
GROUP BY tag_name
ORDER BY num_of_uses DESC
LIMIT 5;

-- Instagram is having a problem with bots. Bots can be identified
-- if they have liked every post on the site. 
-- Find out which users are likely bots.
SELECT 
    username, COUNT(*) AS num_likes
FROM
    users
        INNER JOIN
    likes ON users.id = likes.user_id
GROUP BY likes.user_id
HAVING num_likes = (SELECT 
        COUNT(*)
    FROM
        photos);
    
    