use court_case_scheduling_system;


DELIMITER $$

CREATE TRIGGER BeforeCaseDelete
BEFORE DELETE ON Cases
FOR EACH ROW
BEGIN
    DECLARE case_exists INT;
    SELECT COUNT(*) INTO case_exists
    FROM Schedules
    WHERE CaseID = OLD.CaseID;
    
    IF case_exists > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot delete case, schedules exist for this case';
    END IF;
END $$

DELIMITER ;
