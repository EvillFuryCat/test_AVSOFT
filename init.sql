CREATE DATABASE IF NOT EXISTS avsoft DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci;

USE avsoft;

CREATE TABLE IF NOT EXISTS word_counts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url_file VARCHAR(255) NOT NULL,
    word VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
    count INT NOT NULL
);

SET NAMES utf8;