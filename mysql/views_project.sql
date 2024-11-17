use court_case_scheduling_system;

#1
CREATE VIEW CaseDetails AS
SELECT C.CaseID, C.CaseType, C.CaseStatus, C.StartDate, C.EndDate, 
       Cl.Name AS ClientName, L.Name AS LawyerName
FROM Cases C
JOIN Clients Cl ON C.ClientID = Cl.ClientID
JOIN Lawyers L ON C.LawyerID = L.LawyerID;


SELECT * FROM CaseDetails;


#2
CREATE VIEW ScheduleDetails AS
SELECT S.ScheduleID, S.Date, S.Time, S.CaseID, S.CourtroomID, S.JudgeID,
       Ct.Location AS CourtroomLocation, J.Name AS JudgeName
FROM Schedules S
JOIN Courtrooms Ct ON S.CourtroomID = Ct.CourtroomID
JOIN Judges J ON S.JudgeID = J.JudgeID;


SELECT * FROM ScheduleDetails;


