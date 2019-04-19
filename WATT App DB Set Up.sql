/* 
*************
RUN ONLY ONCE
*************
*/

CREATE DATABASE WATTapplication;

USE WATTapplication

CREATE SCHEMA WATT;

CREATE TABLE WATT.taskType (
	taskTypeId INT PRIMARY KEY NOT NULL IDENTITY(1,1),
	taskTypeName VARCHAR(50)
)

INSERT INTO WATT.taskType (taskTypeName)
VALUES 
('Files'),
('Data Inquiries'),
('Email'),
('Review'),
('Call'),
('Meeting'),
('Break'),
('Chat/Questions')
('Notes/Planning'),
('Miscellaneous');


--DROP TABLE WATT.task
CREATE TABLE watt.worked (
	workedItemId INT PRIMARY KEY NOT NULL IDENTITY(1,1),
	taskTypeId INT,
	clientCode VARCHAR(4),
	workedItemNote VARCHAR(100),
	startedAtTime SMALLDATETIME ,
	endedAtTime SMALLDATETIME,
	duration INT,
	FOREIGN KEY (taskTypeId) REFERENCES WATT.taskType (taskTypeId)
)
--DROP TABLE WATT.worked
CREATE TABLE watt.worked (
	workedItemId INT PRIMARY KEY NOT NULL IDENTITY(1,1),
	taskTypeId INT,
	clientCode VARCHAR(10),
	workedItemNote VARCHAR(100), 
	startedAtTime SMALLDATETIME,
	endedAtTime SMALLDATETIME,
	duration TIME,
	FOREIGN KEY (taskTypeId) REFERENCES WATT.taskType (taskTypeId)
)

--DROP TABLE WATT.settings
CREATE TABLE WATT.settings (
	username VARCHAR(10) PRIMARY KEY, 
	backgroundColor VARCHAR(10),
)

SELECT * FROM WATT.taskType;

SELECT * FROM WATT.worked;


CREATE TABLE watt.clientCodeList (
	clientCodeOption VARCHAR(4)
)

INSERT INTO watt.clientCodeList 
VALUES
('4460'),
('4420'),
('watt')

--DROP TABLE WATT.archivedWork
CREATE TABLE watt.archivedWork (
	archivedWorkId INT PRIMARY KEY IDENTITY(1,1),
	taskTypeName VARCHAR(20),
	clientCode VARCHAR(4),
	workedItemNote VARCHAR(100), 
	startedAtTime SMALLDATETIME,
	endedAtTime SMALLDATETIME,
	duration TIME
)

UPDATE watt.worked
SET endedAtTime = GETDATE()
WHERE workedItemId = 11


select * from watt.archivedWork

MERGE INTO WATT.archivedWork AS target
USING 
	(SELECT 
		taskTypeName, clientCode, workedItemNote, startedAtTime, endedAtTime, endedAtTime 
	FROM watt.worked 
	INNER JOIN watt.taskType 
		ON worked.taskTypeId = taskType.taskTypeId) 
	AS source (taskTypeName,clientCode,workedItemNote,startedAtTime,endedAtTime,duration)
	ON (target.taskTypeName = source.taskTypeName
		AND target.clientCode = source.clientCode
		AND target.workedItemNote = source.workedItemNote
		AND target.startedAtTime = source.startedAtTime)

WHEN NOT MATCHED THEN
	INSERT (taskTypeName,clientCode,workedItemNote,startedAtTime,endedAtTime,duration)
	VALUES (source.taskTypeName,source.clientCode,source.workedItemNote,source.startedAtTime,source.endedAtTime,source.duration);


/* sTORED pROCEDURE?  */

/*DURATION TRIGGER*/


/* VIEW: INQ / FALLOUT REVIEW REPORT TEMPLATE */
--DROP VIEW watt.V_reviewReportTracking
CREATE VIEW watt.V_reviewTrackingReport AS
SELECT 
	worked.clientCode, 
	CAST(worked.startedAtTime AS DATE) [Date Worked],
	FORMAT(worked.startedAtTime, 'hh:mm tt', 'en-US') AS StartTimeForDisplay,
	FORMAT(worked.endedAtTime, 'hh:mm tt', 'en-US') AS EndTimeForDisplay,
	worked.duration,
	FORMAT(endedAtTime - startedAtTime, 'HH:mm:ss', 'en-US') as timediff,
	FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as minutes, 
	CASE 
		WHEN  CAST(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as INT) < 5
			THEN '5 min'
		WHEN  CAST(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as INT) < 10
			THEN '10 min'
		WHEN  CAST(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as INT) < 15
			THEN '15 min'
		WHEN  CAST(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as INT) < 20
			THEN '20 min'
		WHEN  CAST(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as INT) < 25
			THEN '25 min'
		WHEN  CAST(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as INT) < 30
			THEN '30 min'
		ELSE 
			'unknown'
	END AS timeworked
FROM 
	WATT.worked 
	INNER JOIN WATT.taskType 
		ON worked.taskTypeId = taskType.taskTypeId
WHERE 
	taskType.taskTypeName = 'Review'
