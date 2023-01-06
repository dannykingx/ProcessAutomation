# ProcessAutomation
#Developing a points systems for drillers based on W2S, S2S, S2W, W2W connection times.
#############################################################################################################################
#reading all the values (both from database and PLC)
#convert to python data set, then read from dataset and store values in variables


#connectionKPIStatus - connection times

def mainCalc(connectionNumber):

	'''
	PLC TAGS 
	
	weightToSlipsTime = system.tag.read("[s1500]ProcessAutomation/Monitor/KPIandComplaince/drillingConnectionKPIStatus/timeInWeightToSlips_s").value
	print "weightToSlipsTime: " + str(weightToSlipsTime)
	slipsToSlipsTime = system.tag.read("[s1500]ProcessAutomation/Monitor/KPIandComplaince/drillingConnectionKPIStatus/timeInSlipsToSlips_s").value
	print "slipsToSlipsTime: " + str(slipsToSlipsTime)
	slipsToWeightTime = system.tag.read("[s1500]ProcessAutomation/Monitor/KPIandComplaince/drillingConnectionKPIStatus/timeInSlipsToWeight_s").value
	print "slipsToWeightTime: " + str(slipsToWeightTime)
	weightToWeightTime = system.tag.read("[s1500]ProcessAutomation/Monitor/KPIandComplaince/drillingConnectionKPIStatus/timeInWeightToWeight_s").value
	print "weightToWeightTime: " + str(weightToWeightTime)
	'''
	
	weightToSlipsTime = system.tag.read("[s1500]Gamification/drillingConnectionKPIStatus/W2S_S").value
	print "weightToSlipsTime: " + str(weightToSlipsTime)
	slipsToSlipsTime = system.tag.read("[s1500]Gamification/drillingConnectionKPIStatus/S2S_S").value
	print "slipsToSlipsTime: " + str(slipsToSlipsTime)
	slipsToWeightTime = system.tag.read("[s1500]Gamification/drillingConnectionKPIStatus/S2W_S").value
	print "slipsToWeightTime: " + str(slipsToWeightTime)
	weightToWeightTime = system.tag.read("[s1500]Gamification/drillingConnectionKPIStatus/W2W_S").value
	print "weightToWeightTime: " + str(weightToWeightTime)
	
	#initializing points
	points_WS = 0
	points_SS = 0
	points_SW = 0
	points_WW = 0
	totalPoints = 0
	
	#targetKPI 
	
	targetKPIDataSet = system.tag.read("[s1500]Gamification/targetKPI/targetKPI").value
	targetKPIDataSetPython = system.dataset.toPyDataSet(targetKPIDataSet)
	targetKPI_len = targetKPIDataSet.getRowCount()
	#print targetKPIDataSetPython
	#print targetKPI_len
	
	#connectionKPIRubrics
	
	connectionKPIRubricsDataSet = system.tag.read("[s1500]Gamification/connectionKPIRubrics/connectionRubrics").value
	connectionKPIRubricsDataSetPython = system.dataset.toPyDataSet(connectionKPIRubricsDataSet)
	connectionKPIRubrics_len = connectionKPIRubricsDataSet.getRowCount()
	#connectionKPIRubricsDataSetPython_mutable = [[field for field in row] for row in connectionKPIRubricsDataSetPython]  
	#print connectionKPIRubricsDataSetPython
	#print connectionKPIRubrics_len
	
	#challengeList
	
	challengeListDataSet = system.tag.read("[s1500]Gamification/challengeList/challengeList").value
	challengeListDataSetPython = system.dataset.toPyDataSet(challengeListDataSet)
	challengeList_len = challengeListDataSet.getRowCount()
	#print challengeListDataSetPython
	#print challengeList_len
	
	#pointsStatus
	
	pointsStatusDataSet = system.tag.read("[s1500]Gamification/connectionPointsStatus/connectionPointsStatus").value
	pointsStatusDataSetPython = system.dataset.toPyDataSet(pointsStatusDataSet)
	connectionPointsStatus_len = pointsStatusDataSet.getRowCount()
	#print pointsStatusDataSetPython
	
	#userInfo	
	
	userInfoDataSet = system.tag.read("[s1500]Gamification/userInfo/userInfo").value
	userInfoDataSetPython = system.dataset.toPyDataSet(userInfoDataSet)
	userInfoDataSet_len = userInfoDataSet.getRowCount()
	#print userInfoDataSetPython
	
	W2S_rounded = round(weightToSlipsTime, 2)
	S2S_rounded = round(slipsToSlipsTime, 2)
	S2W_rounded = round(slipsToWeightTime, 2)
	#W2W_rounded = round(weightToWeightTime, 2)
	#e = round(targetKPIDataSetPython[0][3], 2)
	#f = round(targetKPIDataSetPython[1][3], 2)
	#g = round(targetKPIDataSetPython[2][3], 2)
	#h = round(targetKPIDataSetPython[3][3], 2)
	
	category_met_WS = targetComparison(W2S_rounded, targetKPIDataSetPython[0][3]) #Met the target? - 1 min
	category_met_SS = targetComparison(S2S_rounded, targetKPIDataSetPython[1][3]) #Met the target? - 2.2 min
	category_met_SW = targetComparison(S2W_rounded, targetKPIDataSetPython[2][3]) #Met the target? - 2 min
	#category_met_WW = targetComparison(W2W_rounded, targetKPIDataSetPython[3][3]) #Met the target? - 5.2 min
	
	
	
	#looping through rubrics to compare strings returned and string in table and allocates the points accordingly		
	for i in range (0, connectionKPIRubrics_len): 
		if connectionKPIRubricsDataSetPython [i][1] == str(category_met_WS):
			points_WS = points_WS + connectionKPIRubricsDataSetPython [i][2]
	for i in range(0, connectionKPIRubrics_len):
		if connectionKPIRubricsDataSetPython [i][1] == str(category_met_SS):
			points_SS = points_SS + connectionKPIRubricsDataSetPython [i][3]
	for i in range (0, connectionKPIRubrics_len):
		if connectionKPIRubricsDataSetPython [i][1] == str(category_met_SW):
			points_SW = points_SW + connectionKPIRubricsDataSetPython [i][4]
			
	'''		
	for i in range (0, connectionKPIRubrics_len):
		if connectionKPIRubricsDataSetPython [i][1] == str(category_met_WW):
			points_WW = points_WW + connectionKPIRubricsDataSetPython [i][5]
	'''			
				
	totalPoints = points_WS + points_SS + points_SW
	#points_WW
	#addPointsForCompletedChallenge()
		
	print "points_WS: " + str(points_WS)
	print "points_SS: " + str(points_SS)
	print "points_SW: " + str(points_SW)
	#print "points_WW: " + str(points_WW)
	#print "pointsChallenge: " + str(addPointsForCompletedChallenge())
	print "totalPoints:" + str(totalPoints)
	
	import time
	ts = time.time()
	from datetime import datetime
	timeStamp = datetime.fromtimestamp(ts)
	last_mod = timeStamp.strftime('%Y-%m-%d %H:%M:%S')
	
	
	userEntry = 'jsmith'
	userInfoNotFound = shared.Gamification.verification.CheckForUser(userEntry)
	
	#another var or tag where connection num
	print userInfoNotFound
	if userInfoNotFound[0] == 0:
		depthUOM = 'ft'
		userID = userInfoNotFound[1]
		tourID = 1
		wellID = system.tag.read("[s1500]ProcessAutomation/WellPlan/CachedData/Wellplan_details/current_well_ID_cacheMemory").value
		connectionHoleDepth = system.tag.read("[s1500]Gamification/drillingConnectionKPIStatus/connectionHoleDepth").value
		
		#insert/ update query
		params = {"connectionHoleDepth":connectionHoleDepth, "depthUOM":depthUOM, "connectionNumber":connectionNumber, "userID":userID, "tourID":tourID, "points":totalPoints, "timeStamp":last_mod, "wellID":wellID}
		print params
		system.db.runNamedQuery(project = "EdgeControlsPlusStandard", path = "Gamification/CreateNewConnectionPointsStatus", parameters = params)
			
	else:
		#for now if the user is not found in the database then the points are not stored 
		pass
		#temp user -001
'''		
def addPointsForCompletedChallenge():
		
	pointsChallenge = 0
	
	for i in range (0, challengeList_len):
		if(challengeListDataSetPython[i][3] == 1):
			pointsChallenge = pointsChallenge + challengeListDataSetPython[i][2]
			import time
			ts = time.time()
			from datetime import datetime
			timeStamp = datetime.fromtimestamp(ts)
			last_mod = timeStamp.strftime('%Y-%m-%d %H:%M:%S')
			
		elif(challengeListDataSetPython[i][3] == 0):
			pointsChallenge = pointsChallenge + 0
			
	return pointsChallenge
'''
		  
def targetComparison (connectionTime, targetKPI):
	#what condition was met
	#compare the connection time with the target KPI
	if connectionTime > targetKPI or connectionTime == 0:
		categoryMet = "Didnt meet the target?"
	elif 0.9 * targetKPI < connectionTime <= targetKPI:
		categoryMet = "Met the target?"
	elif 0.75 * targetKPI < connectionTime <= 0.9 * targetKPI:
		categoryMet = "10% Lower"
	elif 0.50 * targetKPI < connectionTime <= 0.75 * targetKPI:
		categoryMet = "25% Lower"
	elif connectionTime <= 0.50 * targetKPI:
		categoryMet = "50% Lower"
	
	return categoryMet 
    
    
#############################################################################

#verification script
#update user
def CheckForUser(userEntry):
	#userInfo	
	userInfoDataSet = system.tag.read("[s1500]Gamification/userInfo/userInfo").value
	userInfoDataSetPython = system.dataset.toPyDataSet(userInfoDataSet)
	userInfoDataSet_len = userInfoDataSet.getRowCount()
	#print userInfoDataSetPython


	for i in range(0,userInfoDataSet_len):
		#print (type(str(userInfoDataSetPython[i][1])))
		if(userEntry == str(userInfoDataSetPython[i][1])):
			userInfoNotFound = 0     #user is found in the database hence breaking the for loop
			break
		elif(userEntry != userInfoDataSetPython[i][1]):
			userInfoNotFound = 1
	if userInfoNotFound == 1:		
		userID = -1
		#system.gui.messageBox("User does not exist, please sign up on connections window.")
		
	else:
		userID = userInfoDataSetPython[i][0]
		paramsUpdate = {"userID":userID}
		#system.db.runNamedQuery(project = "EdgeControlsPlusStandard", path = "Gamification/updateConnectionPointsStatus", parametersUpdate = paramsUpdate)
		
	return userInfoNotFound, userID
	
#verifying = CheckForUser("jsmith")
