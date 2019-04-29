USE WATTapplication
/*
SELECT * FROM WATT.worked WHERE  CAST(worked.startedAtTime AS DATE) LIKE CAST(GETDATE() as DATE)

SELECT * FROM WATT.worked WHERE  CAST(worked.startedAtTime AS DATE) BETWEEN '2019-04-19' AND '2019-04-25' AND taskTypeId = 5

SELECT * FROM WATT.worked WHERE workedItemId = 75


SELECT 
CAST(worked.startedAtTime AS DATE) [Date Worked],
SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) AS totalMinutesWorked,
SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) / 60.0 AS hours
FROM WATT.worked 
GROUP BY CAST(worked.startedAtTime AS DATE)

--VIEW: INQ / FALLOUT REVIEW REPORT TEMPLATE 

SELECT * FROM watt.V_reviewTrackingReport
WHERE Date BETWEEN '2019-04-22' AND '2019-04-25'

*/

SELECT 
	worked.workedItemId,
	taskType.taskTypeName,
	worked.workedItemNote,
	worked.clientCode, 
	CAST(worked.startedAtTime AS DATE) [Date Worked],
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
	END AS timeworked,
	worked.duration,
	FORMAT(endedAtTime - startedAtTime, 'HH:mm:ss', 'en-US') as INFOtimediff,
	(CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) as INFOminutes
FROM 
	WATT.worked 
	LEFT JOIN WATT.taskType 
		ON worked.taskTypeId = taskType.taskTypeId
WHERE 
	CAST(worked.startedAtTime AS DATE) LIKE CAST(GETDATE() as DATE)


/*
UPDATE watt.worked
SET taskTypeId =  10
WHERE workedItemId = 75
*/


/*

UPDATE watt.worked
SET startedAtTime = '2019-04-25 10:40:00'
WHERE workedItemId = 106

UPDATE watt.worked
SET endedAtTime = '2019-04-26 14:30:00'
WHERE workedItemId = 140

*/

