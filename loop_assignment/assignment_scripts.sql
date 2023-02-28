-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema assignment
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema assignment
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `assignment` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `assignment` ;

-- -----------------------------------------------------
-- Table `assignment`.`report_status`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `assignment`.`report_status` (
  `report_id` INT NOT NULL AUTO_INCREMENT,
  `report_status` VARCHAR(45) NULL DEFAULT NULL,
  `report_content` BLOB NULL DEFAULT NULL,
  PRIMARY KEY (`report_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 12
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `assignment`.`store_hours`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `assignment`.`store_hours` (
  `store_id` BIGINT NULL DEFAULT NULL,
  `day` INT NULL DEFAULT NULL,
  `start_time_local` TEXT NULL DEFAULT NULL,
  `end_time_local` TEXT NULL DEFAULT NULL,
  INDEX `store_hours_status_idx` (`store_id` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `assignment`.`store_status`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `assignment`.`store_status` (
  `store_id` BIGINT NULL DEFAULT NULL,
  `status` TEXT NULL DEFAULT NULL,
  `timestamp_utc` DATETIME NULL DEFAULT NULL)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `assignment`.`store_timezones`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `assignment`.`store_timezones` (
  `store_id` BIGINT NULL DEFAULT NULL,
  `timezone_str` TEXT CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL,
  INDEX `store_timezone_hours_idx` (`store_id` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = armscii8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
