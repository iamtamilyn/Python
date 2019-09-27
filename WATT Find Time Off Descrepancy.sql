USE WATTapplication
/*
SELECT * FROM WATT.worked WHERE  CAST(worked.startedAtTime AS DATE) LIKE '2019-09-19' ORDER BY startedAtTime

SELECT worked.workedItemId, worked.startedAtTime, worked.endedAtTime, 
worked.endedAtTime -  worked.startedAtTime AS math
FROM WATT.worked ORDER BY startedAtTime DESC
*/
BEGIN TRANSACTION

SELECT 
workedItemId, startedAtTime, endedAtTime,
LAG(endedAtTime,1) OVER (ORDER BY workedItemId) as lagAtTime
INTO #testingData
FROM WATT.worked 
WHERE  CAST(worked.startedAtTime AS DATE) LIKE '2019-09-20'
ORDER BY startedAtTime

SELECT
	*,
	#testingData.workedItemId,
	LEFT(CAST(#testingData.startedAtTime AS time),8) as startedAtTime,
	LEFT(CAST(#testingData.endedAtTime AS time),8) as endedAtTime
	--,CAST(#testingData.lagAtTime - startedAtTime AS smalldatetime) lagDifference
	,CAST(endedAtTime - #testingData.lagAtTime AS time) lagDifference
	--,(CAST(FORMAT(endedAtTime - startedAtTime, 'HH', 'en-US') as int) *60) + Cast(FORMAT(endedAtTime - startedAtTime, 'mm', 'en-US') as int) AS totalMinutesWorked
	,LEFT(CAST(endedAtTime - startedAtTime AS time),8) lagDifference
FROM #testingData


ROLLBACK