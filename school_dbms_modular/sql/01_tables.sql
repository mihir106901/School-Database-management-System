-- Creates tables inside the database.
-- The Python initializer runs `USE {{DB_NAME}};` before executing this file.

-- Student master table
CREATE TABLE IF NOT EXISTS student (
  GR_number     INT PRIMARY KEY,
  Roll_number   INT NOT NULL,
  Name          VARCHAR(100) NOT NULL,
  Mobile_Number VARCHAR(20),
  Address       VARCHAR(255),
  Class         INT NOT NULL,
  Section       VARCHAR(10) NOT NULL,
  created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- One-to-one (or one-per-student) fees record
CREATE TABLE IF NOT EXISTS fees (
  GR_number        INT PRIMARY KEY,
  Tuition_Fee      INT NOT NULL,
  Technology_Fee   INT NOT NULL,
  Fees_Paid        INT NOT NULL DEFAULT 0,
  CONSTRAINT fk_fees_student
    FOREIGN KEY (GR_number) REFERENCES student(GR_number)
    ON DELETE CASCADE ON UPDATE CASCADE
);

-- Library issue history (many per student)
CREATE TABLE IF NOT EXISTS library (
  id                 BIGINT AUTO_INCREMENT PRIMARY KEY,
  GR_number           INT NOT NULL,
  Ticket_number       INT NOT NULL,
  Name_of_book_issued VARCHAR(255) NOT NULL,
  ISBN                VARCHAR(40) NOT NULL,
  Date_of_issue       DATE NOT NULL,
  Date_of_return      DATE NULL,
  CONSTRAINT fk_library_student
    FOREIGN KEY (GR_number) REFERENCES student(GR_number)
    ON DELETE CASCADE ON UPDATE CASCADE,
  INDEX idx_library_gr (GR_number),
  INDEX idx_library_book (Name_of_book_issued)
);

-- Exam marks (one per student)
CREATE TABLE IF NOT EXISTS exam (
  GR_number      INT PRIMARY KEY,
  First_UT       FLOAT NULL,
  Second_UT      FLOAT NULL,
  Third_UT       FLOAT NULL,
  Fourth_UT      FLOAT NULL,
  PRE_MID_TERM   FLOAT NULL,
  MID_TERM       FLOAT NULL,
  POST_MID_TERM  FLOAT NULL,
  ANNUAL         FLOAT NULL,
  CONSTRAINT fk_exam_student
    FOREIGN KEY (GR_number) REFERENCES student(GR_number)
    ON DELETE CASCADE ON UPDATE CASCADE
);
