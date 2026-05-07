-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema f1db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema f1db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `f1db` ;
USE `f1db` ;

-- -----------------------------------------------------
-- Table `f1db`.`status`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `f1db`.`status` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `statusName` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `f1db`.`constructor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `f1db`.`constructor` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `constructorName` VARCHAR(45) NOT NULL,
  `constructorRef` VARCHAR(100) NULL,
  `constructorNationality` VARCHAR(100) NOT NULL,
  `constructorUrl` VARCHAR(255) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `f1db`.`circuit`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `f1db`.`circuit` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `circuitRef` VARCHAR(45) NOT NULL,
  `circuitName` VARCHAR(100) NOT NULL,
  `location` VARCHAR(45) NOT NULL,
  `country` VARCHAR(45) NOT NULL,
  `lat` DECIMAL NULL,
  `lng` DECIMAL NULL,
  `alt` VARCHAR(45) NULL,
  `circuitUrl` VARCHAR(255) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `f1db`.`race`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `f1db`.`race` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `year` YEAR NOT NULL,
  `round` INT NOT NULL,
  `circuit_id` INT NOT NULL,
  `name` VARCHAR(255) NOT NULL,
  `date` DATE NOT NULL,
  `race_time` TIME NULL,
  `url` VARCHAR(255) NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_race_circuit1_idx` (`circuit_id` ASC) VISIBLE,
  CONSTRAINT `fk_race_circuit1`
    FOREIGN KEY (`circuit_id`)
    REFERENCES `f1db`.`circuit` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `f1db`.`constructorResult`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `f1db`.`constructorResult` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `race_id` INT NOT NULL,
  `constructor_id` INT NOT NULL,
  `points` DECIMAL(5,2) NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_constructorResult_constructor1_idx` (`constructor_id` ASC) VISIBLE,
  INDEX `fk_constructorResult_race1_idx` (`race_id` ASC) VISIBLE,
  CONSTRAINT `fk_constructorResult_constructor1`
    FOREIGN KEY (`constructor_id`)
    REFERENCES `f1db`.`constructor` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_constructorResult_race1`
    FOREIGN KEY (`race_id`)
    REFERENCES `f1db`.`race` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `f1db`.`constructorStanding`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `f1db`.`constructorStanding` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `race_id` INT NOT NULL,
  `constructor_id` INT NOT NULL,
  `points` DECIMAL(5,2) NOT NULL,
  `positionConstructor` INT NOT NULL,
  `wins` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_constructorStanding_race1_idx` (`race_id` ASC) VISIBLE,
  INDEX `fk_constructorStanding_constructor1_idx` (`constructor_id` ASC) VISIBLE,
  CONSTRAINT `fk_constructorStanding_race1`
    FOREIGN KEY (`race_id`)
    REFERENCES `f1db`.`race` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_constructorStanding_constructor1`
    FOREIGN KEY (`constructor_id`)
    REFERENCES `f1db`.`constructor` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `f1db`.`driver`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `f1db`.`driver` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `driverRef` VARCHAR(100) NOT NULL,
  `number` VARCHAR(45),
  `code` VARCHAR(45) NULL,
  `forename` VARCHAR(45) NOT NULL,
  `surname` VARCHAR(45) NOT NULL,
  `dob` DATE,
  `nationality` VARCHAR(45) NULL,
  `url` VARCHAR(255) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `f1db`.`driverStandings`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `f1db`.`driverStandings` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `race_id` INT NOT NULL,
  `driver_id` INT NOT NULL,
  `points` DECIMAL(5,2) NOT NULL,
  `position` INT NOT NULL,
  `positionText` VARCHAR(45) NOT NULL,
  `wins` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_driverStandings_driver1_idx` (`driver_id` ASC) VISIBLE,
  INDEX `fk_driverStandings_race1_idx` (`race_id` ASC) VISIBLE,
  CONSTRAINT `fk_driverStandings_driver1`
    FOREIGN KEY (`driver_id`)
    REFERENCES `f1db`.`driver` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_driverStandings_race1`
    FOREIGN KEY (`race_id`)
    REFERENCES `f1db`.`race` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `f1db`.`pitStops`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `f1db`.`pitStops` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `race_id` INT NOT NULL,
  `driver_id` INT NOT NULL,
  `stop` INT NOT NULL,
  `lap` INT NOT NULL,
  `timePits` TIME NOT NULL,
  `duration` DECIMAL NOT NULL,
  `milliseconds` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_pitStops_driver1_idx` (`driver_id` ASC) VISIBLE,
  INDEX `fk_pitStops_race1_idx` (`race_id` ASC) VISIBLE,
  CONSTRAINT `fk_pitStops_driver1`
    FOREIGN KEY (`driver_id`)
    REFERENCES `f1db`.`driver` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_pitStops_race1`
    FOREIGN KEY (`race_id`)
    REFERENCES `f1db`.`race` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `f1db`.`qualifying`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `f1db`.`qualifying` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `race_id` INT NOT NULL,
  `driver_id` INT NOT NULL,
  `constructor_id` INT NOT NULL,
  `number` INT NOT NULL,
  `positionQualifyer` INT NOT NULL,
  `q1` VARCHAR(45) NULL,
  `q2` VARCHAR(45) NULL,
  `q3` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_qualifying_race1_idx` (`race_id` ASC) VISIBLE,
  INDEX `fk_qualifying_driver1_idx` (`driver_id` ASC) VISIBLE,
  INDEX `fk_qualifying_constructor1_idx` (`constructor_id` ASC) VISIBLE,
  CONSTRAINT `fk_qualifying_race1`
    FOREIGN KEY (`race_id`)
    REFERENCES `f1db`.`race` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_qualifying_driver1`
    FOREIGN KEY (`driver_id`)
    REFERENCES `f1db`.`driver` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_qualifying_constructor1`
    FOREIGN KEY (`constructor_id`)
    REFERENCES `f1db`.`constructor` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `f1db`.`results`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `f1db`.`results` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `race_id` INT NOT NULL,
  `driver_id` INT NOT NULL,
  `constructor_id` INT NOT NULL,
  `number` VARCHAR(45) NULL,
  `grid` INT NULL,
  `position` INT NULL,
  `positionText` VARCHAR(45) NULL,
  `positionOrder` INT NOT NULL,
  `points` DECIMAL NOT NULL,
  `laps` INT NOT NULL,
  `resultsTime` VARCHAR(45) NULL,
  `milliseconds` INT NULL,
  `fastestLap` INT NULL,
  `rankResults` INT NULL,
  `fastestLapTime` VARCHAR(45) NULL,
  `fastestLapSpeed` DECIMAL NULL,
  `status_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_results_driver1_idx` (`driver_id` ASC) VISIBLE,
  INDEX `fk_results_race1_idx` (`race_id` ASC) VISIBLE,
  INDEX `fk_results_constructor1_idx` (`constructor_id` ASC) VISIBLE,
  INDEX `fk_results_status1_idx` (`status_id` ASC) VISIBLE,
  CONSTRAINT `fk_results_driver1`
    FOREIGN KEY (`driver_id`)
    REFERENCES `f1db`.`driver` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_results_race1`
    FOREIGN KEY (`race_id`)
    REFERENCES `f1db`.`race` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_results_constructor1`
    FOREIGN KEY (`constructor_id`)
    REFERENCES `f1db`.`constructor` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_results_status1`
    FOREIGN KEY (`status_id`)
    REFERENCES `f1db`.`status` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `f1db`.`lapTimes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `f1db`.`lapTimes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `race_id` INT NOT NULL,
  `driver_id` INT NOT NULL,
  `lap` INT NOT NULL,
  `lapPosition` INT NOT NULL,
  `lapTime` VARCHAR(45) NOT NULL,
  `milliseconds` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_lapTimes_race1_idx` (`race_id` ASC) VISIBLE,
  INDEX `fk_lapTimes_driver1_idx` (`driver_id` ASC) VISIBLE,
  CONSTRAINT `fk_lapTimes_race1`
    FOREIGN KEY (`race_id`)
    REFERENCES `f1db`.`race` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_lapTimes_driver1`
    FOREIGN KEY (`driver_id`)
    REFERENCES `f1db`.`driver` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE='';
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;




SET FOREIGN_KEY_CHECKS = 0;

-- 1. circuit
LOAD DATA INFILE '/var/lib/mysql-files/data/circuits.csv'
INTO TABLE circuit
CHARACTER SET latin1
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id, circuitRef, circuitName, location, country, lat, lng, alt, circuitUrl);

-- 2. status
LOAD DATA INFILE '/var/lib/mysql-files/data/status.csv'
INTO TABLE status
CHARACTER SET latin1
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id, statusName);

-- 3. constructor
LOAD DATA INFILE '/var/lib/mysql-files/data/constructors.csv'
INTO TABLE constructor
CHARACTER SET latin1
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id, constructorRef, constructorName, constructorNationality, constructorUrl);

-- 4. driver
LOAD DATA INFILE '/var/lib/mysql-files/data/drivers.csv'
INTO TABLE driver
CHARACTER SET latin1
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id, driverRef, number, code, forename, surname, @dob, nationality, url)
SET dob = IF(@dob = '' OR @dob IS NULL, NULL,
          IF(@dob REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2}$',
             STR_TO_DATE(@dob, '%Y-%m-%d'),
             STR_TO_DATE(@dob, '%d/%m/%Y')
          ));

-- 5. race
LOAD DATA INFILE '/var/lib/mysql-files/data/races.csv'
INTO TABLE race
CHARACTER SET latin1
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id, year, round, circuit_id, name, date, @race_time, url)
SET race_time = IF(TRIM(@race_time) = '', NULL, TRIM(@race_time));

-- 6. results
LOAD DATA INFILE '/var/lib/mysql-files/data/results.csv'
INTO TABLE results
CHARACTER SET latin1
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id, race_id, driver_id, constructor_id, number, grid, position, positionText, positionOrder, points, laps, resultsTime, milliseconds, fastestLap, rankResults, fastestLapTime, fastestLapSpeed, status_id);

-- 7. constructorResult
LOAD DATA INFILE '/var/lib/mysql-files/data/constructorResults.csv'
INTO TABLE constructorResult
CHARACTER SET latin1
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id, race_id, constructor_id, points);

-- 8. constructorStanding
LOAD DATA INFILE '/var/lib/mysql-files/data/constructorStandings.csv'
INTO TABLE constructorStanding
CHARACTER SET latin1
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id, race_id, constructor_id, points, positionConstructor, wins);

-- 9. driverStandings
LOAD DATA INFILE '/var/lib/mysql-files/data/driverStandings.csv'
INTO TABLE driverStandings
CHARACTER SET latin1
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id, race_id, driver_id, points, position, positionText, wins);

-- 10. qualifying
LOAD DATA INFILE '/var/lib/mysql-files/data/qualifying.csv'
INTO TABLE qualifying
CHARACTER SET latin1
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(id, race_id, driver_id, constructor_id, number, positionQualifyer, q1, q2, q3);

-- 11. lapTimes
LOAD DATA INFILE '/var/lib/mysql-files/data/lapTimes.csv'
INTO TABLE lapTimes
CHARACTER SET latin1
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(race_id, driver_id, lap, lapPosition, lapTime, milliseconds);

-- 12. pitStops
LOAD DATA INFILE '/var/lib/mysql-files/data/pitStops.csv'
INTO TABLE pitStops
CHARACTER SET latin1
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(race_id, driver_id, stop, lap, timePits, duration, milliseconds);

SET FOREIGN_KEY_CHECKS = 1;