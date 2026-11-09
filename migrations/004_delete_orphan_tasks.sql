-- Remove tasks that have no owner (created before user_id existed).
DELETE FROM tasks WHERE user_id IS NULL;

-- From now on, every task must belong to a user.
ALTER TABLE tasks ALTER COLUMN user_id SET NOT NULL;