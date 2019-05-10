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
ORDER BY CAST(worked.startedAtTime AS DATE) DESC

SELECT 
worked.clientCode,
SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) AS totalMinutesWorked,
SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) / 60.0 AS hours
FROM WATT.worked 
--WHERE  CAST(worked.startedAtTime AS DATE) BETWEEN '2019-04-26' AND '2019-05-02'
WHERE  CAST(worked.startedAtTime AS DATE) BETWEEN '2019-05-03' AND '2019-05-10'
GROUP BY worked.clientCode
ORDER BY totalMinutesWorked DESC


SELECT * FROM watt.V_TrackingReports
WHERE dateWorked BETWEEN '2019-04-22' AND '2019-04-25'

SELECT *
FROM 
	watt.V_trackingReport
WHERE 
	CAST(V_trackingReport.dateWorked AS DATE) LIKE CAST(GETDATE() as DATE)


*/



--SELECT * FROM WATT.worked WHERE  CAST(worked.startedAtTime AS DATE) LIKE '2019-05-02%'
SELECT * FROM WATT.worked WHERE  CAST(worked.startedAtTime AS DATE) LIKE CAST(GETDATE() as DATE)
/*


UPDATE watt.worked
SET startedAtTime = '2019-05-07 13:24:00'
WHERE workedItemId = 312

UPDATE watt.worked
SET endedAtTime = '2019-05-07 13:24:00'
WHERE workedItemId = 311

*/

/*
RESEARCH

SELECT cast(GETDATE() as smalldatetime)
SELECT cast(GETDATE() as datetime)
SELECT cast(GETDATE() as datetime2)

UPDATE watt.worked
SET taskTypeId =  10
WHERE workedItemId = 311

UPDATE watt.worked
SET clientCode =  'MULT'
WHERE workedItemId = 305

DELETE watt.worked WHERE workedItemId IN (215,216)
*/

