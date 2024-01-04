-- Table for the User model
CREATE TABLE user_user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    email VARCHAR(254) NOT NULL,
    password VARCHAR(128) NOT NULL,
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    is_superuser BOOLEAN NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL,
    role VARCHAR(30) DEFAULT 'PATIENT',
    CHECK (role IN ('ADMIN', 'DOCTOR', 'PATIENT'))
);

-- Table for the Doctor model (inherits from User)
CREATE TABLE user_doctor (
    id SERIAL PRIMARY KEY,
    medical_degree VARCHAR(30) DEFAULT 'Specialist',
    working_shift VARCHAR(8),
    profile_picture VARCHAR(512),
    rating DOUBLE PRECISION DEFAULT 5.0,
    specialization VARCHAR(30) DEFAULT 'Cardiology',
    experience VARCHAR(400),
    completed_appointments INTEGER DEFAULT 1,
    user_id INTEGER REFERENCES user_user(id) ON DELETE CASCADE
);

-- Table for the Patient model (inherits from User)
CREATE TABLE user_patient (
    id SERIAL PRIMARY KEY,
    sex CHAR(1),
    age INTEGER,
    history VARCHAR(255),
    user_id INTEGER REFERENCES user_user(id) ON DELETE CASCADE
);

-- Table for the Prescription model
CREATE TABLE hospital_prescription (
    id SERIAL PRIMARY KEY,
    doctor_id INTEGER REFERENCES user_doctor(id) ON DELETE NO ACTION,
    patient_id INTEGER REFERENCES user_patient(id) ON DELETE CASCADE,
    text VARCHAR(64) NOT NULL
);

-- Table for the Appointment model
CREATE TABLE hospital_appointment (
    id SERIAL PRIMARY KEY,
    doctor_id INTEGER REFERENCES user_doctor(id) ON DELETE CASCADE,
    patient_id INTEGER REFERENCES user_patient(id) ON DELETE CASCADE,
    appointment_date DATE NOT NULL,
    appointment_time TIME NOT NULL,
    image VARCHAR(100),
    done BOOLEAN DEFAULT FALSE,
    prescription_id INTEGER REFERENCES hospital_prescription(id) ON DELETE NO ACTION,
    CHECK (doctor_id <> patient_id) -- Ensure doctor and patient are different
);

-- Table for the Article model
CREATE TABLE hospital_article (
    id SERIAL PRIMARY KEY,
    subject VARCHAR(256),
    body TEXT,
    article_picture VARCHAR(512),
    tag VARCHAR(64)
);

-- Table for the Message model
CREATE TABLE hospital_message (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER REFERENCES user_patient(id) ON DELETE CASCADE,
    receiver_id INTEGER REFERENCES user_user(id) ON DELETE CASCADE,
    message_subject VARCHAR(128) NOT NULL,
    message VARCHAR(256) NOT NULL
);
