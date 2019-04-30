USE WATTapplication
/*
SELECT * FROM WATT.worked WHERE  CAST(worked.startedAtTime AS DATE) LIKE CAST(GETDATE() as DATE)

SELECT * FROM WATT.worked WHERE  CAST(worked.startedAtTime AS DATE) BETWEEN '2019-04-19' AND '2019-04-25' AND taskTypeId = 5

SELECT * FROM WATT.worked WHERE workedItemId = 75

SELECT 
CAST(worked.startedAtTime AS DATE) dateWorked,
SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) AS totalMinutesWorked,
SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) / 60.0 AS hours
FROM WATT.worked 
GROUP BY CAST(worked.startedAtTime AS DATE)

--VIEW: INQ / FALLOUT REVIEW REPORT TEMPLATE 

SELECT * FROM watt.V_TrackingReports
WHERE dateWorked BETWEEN '2019-04-22' AND '2019-04-25'

*/

SELECT *
FROM 
	watt.V_trackingReport
WHERE 
	CAST(V_trackingReport.dateWorked AS DATE) LIKE CAST(GETDATE() as DATE)


/*
UPDATE watt.worked
SET taskTypeId =  10
WHERE workedItemId = 75
*/


/*
SELECT * FROM WATT.worked WHERE  CAST(worked.startedAtTime AS DATE) LIKE CAST(GETDATE() as DATE)

UPDATE watt.worked
SET startedAtTime = '2019-04-29 12:58:00'
WHERE workedItemId = 162

UPDATE watt.worked
SET endedAtTime = '2019-04-29 13:10:00'
WHERE workedItemId = 162

*/

