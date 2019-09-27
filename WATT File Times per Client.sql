USE WATTapplication

SELECT 
	clientCode,
	NULL AS 'File Type',
	SUM((CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int)) AS [MInutes]
FROM 
	WATT.worked
WHERE 
	taskTypeId =  1
	AND CAST(startedAtTime AS DATE) BETWEEN '2019-09-20' AND '2019-09-26'
GROUP BY
	clientCode