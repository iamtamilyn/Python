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

--DROP TABLE WATT.taskType
INSERT INTO WATT.taskType (taskTypeName)
VALUES
('Files'),
('Data Inquiries'),
('Email'),
('Review'),
('Call'),
('Meeting'),
('Break'),
('Little Things'),
('Chat/Questions')
('Notes/Planning'),
('Training/Shadowing'),
('Miscellaneous'),
('Documentation'),
('Project');


--DROP TABLE WATT.worked
CREATE TABLE watt.worked (
	workedItemId INT PRIMARY KEY NOT NULL IDENTITY(1,1),
	taskTypeId INT,
	clientCode VARCHAR(10),
	workedItemNote VARCHAR(100), 
	startedAtTime SMALLDATETIME,
	endedAtTime SMALLDATETIME,
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


/* STORED PROCEDURE  */

/*DURATION TRIGGER*/


/* VIEW: INQ / FALLOUT REVIEW REPORT TEMPLATE */
--DROP VIEW watt.V_reviewTrackingReport
CREATE VIEW watt.V_reviewTrackingReport AS
SELECT 
	worked.clientCode AS CODE, 
	CAST(worked.startedAtTime AS DATE) AS [Date Worked],
	FORMAT(worked.startedAtTime, 'hh:mm tt', 'en-US') AS StartTimeForDisplay,
	FORMAT(worked.endedAtTime, 'hh:mm tt', 'en-US') AS EndTimeForDisplay,
	CASE 
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 5
			THEN '5 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 10
			THEN '10 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)  <= 15
			THEN '15 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)  <= 20
			THEN '20 min'
		WHEN (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 25
			THEN '25 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 30
			THEN '30 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 45
			THEN '45 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 60
			THEN '60 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 75
			THEN '75 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 90
			THEN '90 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 120
			THEN '120 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) < 150
			THEN '150 min'
		WHEN  endedAtTime IS NULL 
			THEN CONCAT((CAST(FORMAT(GETDATE() - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(GETDATE() - startedAtTime, 'mm', 'en-US') as int),'+' )
		ELSE 
			'unknown'
	END AS timeWorkedForDisplay,
	'Tamilyn Peck' AS analystNameForDisplay
FROM 
	WATT.worked 
	INNER JOIN WATT.taskType 
		ON worked.taskTypeId = taskType.taskTypeId
WHERE 
	taskType.taskTypeName = 'Review'

/* VIEW: Durations Report */
--DROP VIEW watt.V_trackingReport
CREATE VIEW watt.V_trackingReport AS
SELECT 
	worked.clientCode AS CODE, 
	CAST(worked.startedAtTime AS DATE) AS dateWorked,
	FORMAT(worked.startedAtTime, 'hh:mm tt', 'en-US') AS StartTimeForDisplay,
	FORMAT(worked.endedAtTime, 'hh:mm tt', 'en-US') AS EndTimeForDisplay,
	CASE 
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 5
			THEN '5 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 10
			THEN '10 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)  <= 15
			THEN '15 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)  <= 20
			THEN '20 min'
		WHEN (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 25
			THEN '25 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 30
			THEN '30 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 45
			THEN '45 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 60
			THEN '60 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 75
			THEN '75 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 90
			THEN '90 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) <= 120
			THEN '120 min'
		WHEN  (CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) < 150
			THEN '150 min'
		WHEN  endedAtTime IS NULL 
			THEN CONCAT((CAST(FORMAT(GETDATE() - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(GETDATE() - startedAtTime, 'mm', 'en-US') as int),'+' )
		ELSE 
			'unknown'
	END AS timeWorkedForDisplay,
	'Tamilyn Peck' AS analystNameForDisplay,
	FORMAT(endedAtTime - startedAtTime, 'HH:mm:ss', 'en-US') as realDurantionInTime,
	(CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) as realDurationInMinutes
FROM 
	WATT.worked 
	INNER JOIN WATT.taskType 
		ON worked.taskTypeId = taskType.taskTypeId