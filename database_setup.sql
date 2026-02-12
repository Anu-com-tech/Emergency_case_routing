-- Emergency Routing System Database Setup
-- Run this script in MySQL to create the required database and tables

-- Create database
CREATE DATABASE IF NOT EXISTS emergency_routing_db;
USE emergency_routing_db;

-- Create hospitals table
CREATE TABLE IF NOT EXISTS hospitals (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL UNIQUE,
  latitude DECIMAL(10, 8) NOT NULL,
  longitude DECIMAL(11, 8) NOT NULL,
  available_beds INT DEFAULT 0,
  available_icu INT DEFAULT 0,
  available_oxygen INT DEFAULT 0,
  available_ventilator INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create emergency_requests table
CREATE TABLE IF NOT EXISTS emergency_requests (
  id INT PRIMARY KEY AUTO_INCREMENT,
  patient_type VARCHAR(50) NOT NULL,
  emergency_type VARCHAR(50) NOT NULL,
  need_bed BOOLEAN DEFAULT TRUE,
  need_icu BOOLEAN DEFAULT FALSE,
  need_oxygen BOOLEAN DEFAULT FALSE,
  need_ventilator BOOLEAN DEFAULT FALSE,
  hospital_id INT NOT NULL,
  status VARCHAR(50) DEFAULT 'Pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (hospital_id) REFERENCES hospitals(id) ON DELETE RESTRICT ON UPDATE CASCADE,
  INDEX idx_status (status),
  INDEX idx_created_at (created_at),
  INDEX idx_hospital_id (hospital_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert sample hospitals (Coimbatore, Tamil Nadu, India)
INSERT INTO hospitals (name, latitude, longitude, available_beds, available_icu, available_oxygen, available_ventilator) VALUES
('Apollo Hospital Coimbatore', 11.0168, 76.9558, 50, 10, 30, 5),
('Ganga Hospital', 11.0211, 76.9506, 40, 8, 25, 4),
('Billroth Hospital', 11.0089, 76.9642, 35, 6, 20, 3),
('Aravind Eye Hospital', 11.0346, 76.9456, 25, 5, 15, 2),
('CMC Hospital', 11.0289, 76.9722, 60, 12, 40, 6);

-- Verify installation
SELECT 'Database setup complete!' as status;
SELECT COUNT(*) as total_hospitals FROM hospitals;
