USE WATTapplication

--SELECT * FROM WATT.worked

/* MAKE VIEW */

/* VIEW: INQ / FALLOUT REVIEW REPORT TEMPLATE */

--SELECT * FROM watt.V_reviewTrackingReport
--WHERE [Date Worked] = '2019-04-19'

SELECT 
	taskType.taskTypeName,
	worked.workedItemNote,
	worked.clientCode, 
	CAST(worked.startedAtTime AS DATE) [Date Worked],
	FORMAT(worked.startedAtTime, 'hh:mm tt', 'en-US') AS StartTimeForDisplay,
	FORMAT(worked.endedAtTime, 'hh:mm tt', 'en-US') AS EndTimeForDisplay,
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
		WHEN  CAST(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as INT) < 45
			THEN '45 min'
		WHEN  CAST(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as INT) < 60
			THEN '60 min'
		WHEN  CAST(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as INT) < 75
			THEN '75 min'
		WHEN  CAST(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as INT) < 90
			THEN '90 min'
		WHEN  CAST(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as INT) < 120
			THEN '120 min'
		WHEN  CAST(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as INT) < 150
			THEN '150 min'
		WHEN  endedAtTime IS NULL 
			THEN 'Open'
		ELSE 
			'unknown'
	END AS timeworked,
	worked.duration,
	FORMAT(endedAtTime - startedAtTime, 'HH:mm:ss', 'en-US') as INFOtimediff,
	FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as INFOminutes
FROM 
	WATT.worked 
	LEFT JOIN WATT.taskType 
		ON worked.taskTypeId = taskType.taskTypeId
WHERE 
	CAST(worked.startedAtTime AS DATE)  = '2019-04-19'


/*
UPDATE watt.worked
SET startedAtTime = '2019-04-19 08:47:00'
WHERE workedItemId = 23
*/

