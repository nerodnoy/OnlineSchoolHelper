CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    link TEXT,
    week_number INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    notes_lesson1 TEXT,
    notes_lesson2 TEXT,
    present BOOLEAN,
    group_id INTEGER REFERENCES groups(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS students_info (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    group_id INTEGER REFERENCES groups(id) ON DELETE CASCADE,
    info TEXT
);