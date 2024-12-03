CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

INSERT INTO users (id, email, password, role) VALUES
    (uuid_generate_v4(), 'admin@example.com', 'hashed_admin_password', 'ADMIN'),
    (uuid_generate_v4(), 'editor@example.com', 'hashed_editor_password', 'EDITOR'),
    (uuid_generate_v4(), 'viewer@example.com', 'hashed_viewer_password', 'VIEWER');

INSERT INTO articles (id, title, content, owner_id)
VALUES
    (uuid_generate_v4(), 'Admin Tips', 'Tips for Admins to manage the platform.', 
        (SELECT id FROM users WHERE email = 'admin@example.com')),
    (uuid_generate_v4(), 'Editing Tips', 'How to edit articles effectively.', 
        (SELECT id FROM users WHERE email = 'editor@example.com')),
    (uuid_generate_v4(), 'Viewing Articles', 'Best practices for viewing content.', 
        (SELECT id FROM users WHERE email = 'viewer@example.com')),
    (uuid_generate_v4(), 'Collaborative Writing', 'Tips for teamwork in writing.', 
        (SELECT id FROM users WHERE email = 'editor@example.com'));
