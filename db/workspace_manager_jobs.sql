-- WorkspaceManager: minimal async job tables
-- MySQL 8.0+ recommended
CREATE DATABASE IF NOT EXISTS dned-jobs CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE dned-jobs;

CREATE TABLE IF NOT EXISTS job (
  id CHAR(36) NOT NULL,
  process_type VARCHAR(64) NOT NULL,
  status ENUM('queued','running','succeeded','failed','canceled','retrying') NOT NULL DEFAULT 'queued',
  params JSON NOT NULL,
  requested_by VARCHAR(128) NULL,
  origin VARCHAR(64) NOT NULL DEFAULT 'organizational',
  priority INT NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  started_at TIMESTAMP NULL DEFAULT NULL,
  finished_at TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (id),
  INDEX idx_job_status (status),
  INDEX idx_job_process_type (process_type),
  INDEX idx_job_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS job_progress (
  job_id CHAR(36) NOT NULL,
  phase VARCHAR(64) NOT NULL DEFAULT 'queued',
  total_units INT NOT NULL DEFAULT 0,
  processed_units INT NOT NULL DEFAULT 0,
  total_emails INT NOT NULL DEFAULT 0,
  processed_emails INT NOT NULL DEFAULT 0,
  last_error VARCHAR(512) NULL,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (job_id),
  CONSTRAINT fk_job_progress_job
    FOREIGN KEY (job_id) REFERENCES job(id)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS job_result (
  job_id CHAR(36) NOT NULL,
  success_count INT NOT NULL DEFAULT 0,
  error_count INT NOT NULL DEFAULT 0,
  error_samples JSON NULL,
  artifacts JSON NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (job_id),
  CONSTRAINT fk_job_result_job
    FOREIGN KEY (job_id) REFERENCES job(id)
    ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
