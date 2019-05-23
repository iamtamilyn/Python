USE WATTapplication

SELECT * FROM WATT.worked WHERE  CAST(worked.startedAtTime AS DATE) LIKE CAST(GETDATE() as DATE)

/****************RESEARCH***************************************

--SELECT * FROM WATT.worked WHERE clientCode LIKE 'POD4'
--SELECT * FROM WATT.worked WHERE  CAST(worked.startedAtTime AS DATE) LIKE '2019-05-02%'

*****************REPORTS****************************************

SELECT *
FROM 
	watt.V_trackingReports
WHERE  CAST(dateWorked AS DATE) BETWEEN '2019-05-10' AND '2019-05-16'
AND taskTypeName = 'Call'
--AND taskTypeName = 'Data Inquiries'
*****************TRACKING UTILIZATION**************************
SELECT 
CAST(worked.startedAtTime AS DATE) dateWorked,
SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) AS totalMinutesWorked,
SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) / 60.0 AS hours
FROM WATT.worked 
GROUP BY CAST(worked.startedAtTime AS DATE)
ORDER BY CAST(worked.startedAtTime AS DATE) DESC

*****************WORK TRACKED BY CLIENT************************
SELECT 
worked.clientCode,
SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) AS totalMinutesWorked,
SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) / 60.0 AS hours
FROM WATT.worked 
--WHERE  CAST(worked.startedAtTime AS DATE) BETWEEN '2019-04-26' AND '2019-05-02'
WHERE  CAST(worked.startedAtTime AS DATE) BETWEEN '2019-05-10' AND '2019-05-15'
GROUP BY worked.clientCode
ORDER BY totalMinutesWorked DESC


*****************UPDATE START DATETIME**************************
UPDATE watt.worked
SET startedAtTime = '2019-05-21 10:17:00'
WHERE workedItemId = 168

*****************UPDATE END DATETIME****************************
UPDATE watt.worked
SET endedAtTime = '2019-05-21 10:29:00'
WHERE workedItemId = 168

*****************UPDATE TASK TYPE*******************************
UPDATE watt.worked
SET taskTypeId =  10
WHERE workedItemId = 311

*****************UPDATE CLIENT CODE*****************************
UPDATE watt.worked
SET clientCode =  ''
WHERE workedItemId = 280

*****************DELETE TASK************************************
DELETE watt.worked WHERE workedItemId = 280


*/
