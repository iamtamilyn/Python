USE WATTapplication

/* Minutes Spent per Task by Date */

SELECT 
	taskTypeName, 
	SUM(CAST(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) as INFOminutes
FROM 
	WATT.worked 
	LEFT JOIN WATT.taskType 
		ON worked.taskTypeId = taskType.taskTypeId
WHERE
	CAST(worked.startedAtTime AS DATE)  = '2019-04-19'
GROUP BY
	taskTypeName