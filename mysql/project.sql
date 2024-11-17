create database Court_Case_Scheduling_System;
use Court_Case_Scheduling_System;




CREATE TABLE Clients (
    ClientID INT PRIMARY KEY,
    Name VARCHAR(100),
    ContactInfo VARCHAR(100)
);

CREATE TABLE Lawyers (
    LawyerID INT PRIMARY KEY,
    Name VARCHAR(100),
    Specialty VARCHAR(100),
    ContactInfo VARCHAR(100)
);

CREATE TABLE Judges (
    JudgeID INT PRIMARY KEY,
    Name VARCHAR(100),
    ExperienceYears INT,
    ContactInfo VARCHAR(100)
);

CREATE TABLE Courtrooms (
    CourtroomID INT PRIMARY KEY,
    Location VARCHAR(100),
    Capacity INT,
    Availability VARCHAR(20)
);

CREATE TABLE Cases (
    CaseID INT PRIMARY KEY,
    ClientID INT,
    LawyerID INT,
    CaseType VARCHAR(100),
    CaseStatus VARCHAR(50),
    StartDate DATE,
    EndDate DATE,
    FOREIGN KEY (ClientID) REFERENCES Clients(ClientID),
    FOREIGN KEY (LawyerID) REFERENCES Lawyers(LawyerID)
);

CREATE TABLE Schedules (
    ScheduleID INT PRIMARY KEY,
    CaseID INT,
    CourtroomID INT,
    JudgeID INT,
    Date DATE,
    Time TIME,
    FOREIGN KEY (CaseID) REFERENCES Cases(CaseID),
    FOREIGN KEY (CourtroomID) REFERENCES Courtrooms(CourtroomID),
    FOREIGN KEY (JudgeID) REFERENCES Judges(JudgeID)
);

#BASIC QUERIES

#1
SELECT * FROM Clients;

#2
SELECT LawyerID, Name, Specialty FROM Lawyers;

#3
SELECT * FROM Judges;

#4
SELECT CourtroomID, Location, Capacity FROM Courtrooms;

#5
SELECT COUNT(*) AS TotalCases FROM Cases;


#INTERMEDIATE QUERIES


#1 Get the number of cases handled by each lawyer:
SELECT L.LawyerID, L.Name, COUNT(C.CaseID) AS NumberOfCases
FROM Lawyers L
LEFT JOIN Cases C ON L.LawyerID = C.LawyerID
GROUP BY L.LawyerID;


#2 Find all cases for a specific client
SELECT * FROM Cases WHERE ClientID = 807;

#3 Get the total number of cases scheduled for each judge
SELECT J.JudgeID, J.Name, COUNT(S.ScheduleID) AS TotalScheduled
FROM Judges J
LEFT JOIN Schedules S ON J.JudgeID = S.JudgeID
GROUP BY J.JudgeID;


#4 List all courtrooms that are currently available
SELECT * FROM Courtrooms WHERE Availability = 'Available';

#5 Find the average experience of judges:
SELECT AVG(ExperienceYears) AS AverageExperience FROM Judges;


#ADVANCED QUERIES

#1 Get case details along with client and lawyer names for all open cases:
SELECT C.CaseID, CL.Name AS ClientName, L.Name AS LawyerName
FROM Cases C
JOIN Clients CL ON C.ClientID = CL.ClientID
JOIN Lawyers L ON C.LawyerID = L.LawyerID
WHERE C.CaseStatus = 'Open';


#2 Find the most common case type and its count:
SELECT CaseType, count(*) AS Count
FROM Cases
GROUP BY CaseType
order by count desc
limit 1;


#3 Get a report of all schedules for the next month, including judge and courtroom details:
SELECT S.ScheduleID, C.CaseID, J.Name AS JudgeName, CR.Location AS CourtroomLocation, S.Date, S.Time
FROM Schedules S
JOIN Cases C ON S.CaseID = C.CaseID
JOIN Judges J ON S.JudgeID = J.JudgeID
JOIN Courtrooms CR ON S.CourtroomID = CR.CourtroomID
WHERE S.Date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 1 MONTH)
ORDER BY S.Date, S.Time;


#4 List clients who have more than one case:
SELECT CL.ClientID, CL.Name, COUNT(C.CaseID) AS CaseCount
FROM Clients CL
JOIN Cases C ON CL.ClientID = C.ClientID
GROUP BY CL.ClientID
HAVING COUNT(C.CaseID) > 1;

#5 Find the next scheduled court date for each case:
SELECT C.CaseID, MIN(S.Date) AS NextCourtDate
FROM Cases C
JOIN Schedules S ON C.CaseID = S.CaseID
GROUP BY C.CaseID;

#6 Find judges who have not been assigned any cases:
SELECT J.JudgeID, J.Name
FROM Judges J
LEFT JOIN Schedules S ON J.JudgeID = S.JudgeID
WHERE S.JudgeID IS  NULL;

#7 List the top 5 lawyers with the highest number of cases:
SELECT L.LawyerID, L.Name, COUNT(C.CaseID) AS NumberOfCases
FROM Lawyers L
JOIN Cases C ON L.LawyerID = C.LawyerID
GROUP BY L.LawyerID
ORDER BY NumberOfCases DESC
LIMIT 5;

#8 Get the schedule of all cases along with client names and status of the case:
SELECT S.ScheduleID, C.CaseID, CL.Name AS ClientName, C.CaseStatus
FROM Schedules S
JOIN Cases C ON S.CaseID = C.CaseID
JOIN Clients CL ON C.ClientID = CL.ClientID
ORDER BY S.Date, S.Time;






#11 Find the case with the latest scheduled court date:
SELECT C.CaseID, MAX(S.Date) AS LatestCourtDate
FROM Cases C
JOIN Schedules S ON C.CaseID = S.CaseID
GROUP BY C.CaseID
ORDER BY LatestCourtDate DESC
LIMIT 1;


#12 Get the total number of cases for each case type and their average duration:
SELECT CaseType, COUNT(CaseID) AS TotalCases, AVG(DATEDIFF(EndDate, StartDate)) AS AverageDuration
FROM Cases
GROUP BY CaseType;


#13 List clients who have the most cases scheduled in the next month:
SELECT CL.ClientID, CL.Name, COUNT(C.CaseID) AS ScheduledCases
FROM Clients CL
JOIN Cases C ON CL.ClientID = C.ClientID
JOIN Schedules S ON C.CaseID = S.CaseID
WHERE S.Date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 1 MONTH)
GROUP BY CL.ClientID
ORDER BY ScheduledCases DESC
LIMIT 1;


#14 Find the most frequent courtroom used for scheduling cases:
SELECT CR.CourtroomID, CR.Location, COUNT(S.ScheduleID) AS Frequency
FROM Courtrooms CR
JOIN Schedules S ON CR.CourtroomID = S.CourtroomID
GROUP BY CR.CourtroomID
ORDER BY Frequency DESC
LIMIT 1;


#15 Get a report of all lawyers along with the total number of scheduled cases they are handling:
SELECT L.LawyerID, L.Name, COUNT(C.CaseID) AS ScheduledCases
FROM Lawyers L
JOIN Cases C ON L.LawyerID = C.LawyerID
JOIN Schedules S ON C.CaseID = S.CaseID
GROUP BY L.LawyerID;

#16 Get the total number of cases by status for each lawyer:
SELECT L.LawyerID, L.Name, C.CaseStatus, COUNT(C.CaseID) AS NumberOfCases
FROM Lawyers L
JOIN Cases C ON L.LawyerID = C.LawyerID
GROUP BY L.LawyerID, C.CaseStatus;


