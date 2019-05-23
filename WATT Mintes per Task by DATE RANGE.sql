USE WATTapplication

/* Minutes Spent per Task by Date Range */

SELECT 
	taskType.taskTypeName,
	SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) AS totalMinutesWorked,
	SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) / 60.0 AS hours
FROM WATT.worked 
	INNER JOIN WATT.taskType 
		ON worked.taskTypeId = taskType.taskTypeId
WHERE  
	CAST(worked.startedAtTime AS DATE) BETWEEN '2019-05-10' AND '2019-05-15'
GROUP BY 
	taskType.taskTypeName
ORDER BY 
	totalMinutesWorked DESC