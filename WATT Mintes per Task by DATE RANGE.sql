USE WATTapplication

/* Minutes Spent per Task by Date */

SELECT 
	taskTypeName, 
	SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) as INFOminutes
FROM 
	WATT.worked 
	LEFT JOIN WATT.taskType 
		ON worked.taskTypeId = taskType.taskTypeId
WHERE
	--CAST(worked.startedAtTime AS DATE)  = '2019-04-19'
	CAST(worked.startedAtTime AS DATE) BETWEEN '2019-04-19' AND '2019-04-25'
GROUP BY
	taskTypeName



SELECT 
CAST(worked.startedAtTime AS DATE) [Date Worked],
SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) AS totalMinutesWorked,
SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) / 60.0 AS hours
FROM WATT.worked 
GROUP BY CAST(worked.startedAtTime AS DATE)