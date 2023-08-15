from django.db import connection

def getSelectedDate():
    query1 = "SELECT currentDate as DATE FROM tblselecteddate;"

    with connection.cursor() as cursor:
        cursor.execute(query1)
        single_value = cursor.fetchone()
        data1= single_value[0] if single_value else None
    
    return data1

def getFromToDT():
    query2 = "SELECT fromDT as fDT, toDT as tDT FROM tbldtspan;"
    with connection.cursor() as cursor:
        cursor.execute(query2)
        single_value = cursor.fetchone()
        return single_value

def updateSelectedDate(date):
    query4 = f"UPDATE tblselecteddate SET currentDate = '{date}';"
    existing_from_dt, existing_to_dt = getFromToDT()
    if existing_from_dt and existing_to_dt:
        # Split the existing time from the output ('2023-07-13 00:00:01', '2023-07-13 23:59:59')
        existing_from_time = existing_from_dt.split()[1]
        existing_to_time = existing_to_dt.split()[1]

        # Combine the updated date with the existing time
        from_dt_tobeupdated = f"{date} {existing_from_time}"
        to_dt_tobeupdated = f"{date} {existing_to_time}"

        # Update the data in the database
        query5 = f"UPDATE tbldtspan SET fromDT = '{from_dt_tobeupdated}';"
        query6 = f"UPDATE tbldtspan SET toDT = '{to_dt_tobeupdated}';"

        with connection.cursor() as cursor:
            cursor.execute(query5)
            cursor.execute(query6)    

    with connection.cursor() as cursor:
        cursor.execute(query4)
        


def getSwitchStatus():
    query3 = "SELECT STATUS FROM tblhrsswitch;"
    with connection.cursor() as cursor:
        cursor.execute(query3)
        single_value = cursor.fetchone()
        data1= single_value[0] if single_value else None
        return data1

def toggleSwitchStatus(status):
    query7 = f"UPDATE tblhrsswitch SET STATUS = '{status}';"
    if status == "OFF":
        NEW_FROM_TIME = "09:30:00"
        NEW_TO_TIME = "19:00:00"
    else:
        NEW_FROM_TIME = "00:00:01"
        NEW_TO_TIME = "23:59:59"
    
    existing_from_dt, existing_to_dt = getFromToDT()
    if existing_from_dt and existing_to_dt:
        # Split the existing time from the output ('2023-07-13 00:00:01', '2023-07-13 23:59:59')
        existing_from_date = existing_from_dt.split()[0]
        existing_to_date = existing_to_dt.split()[0]

        # Combine the updated date with the existing time
        from_tm_tobeupdated = f"{existing_from_date} {NEW_FROM_TIME}"
        to_tm_tobeupdated = f"{existing_to_date} {NEW_TO_TIME}"

        # Update the data in the database
        query8 = f"UPDATE tbldtspan SET fromDT = '{from_tm_tobeupdated}';"
        query9 = f"UPDATE tbldtspan SET toDT = '{to_tm_tobeupdated}';"

        with connection.cursor() as cursor:
            cursor.execute(query8)
            cursor.execute(query9)  
    
    with connection.cursor() as cursor:
        cursor.execute(query7)

    

def convertCountToTime(time_count):
		time_sec = time_count * 10
		time_h_mod = int(time_sec // 3600)
		time_m_mod = int((time_sec - (time_h_mod * 3600)) // 60)
		time_s_mod = int(time_sec - (time_h_mod * 3600) - (time_m_mod * 60))

		if time_h_mod < 10:
			time_h_mod = "0" + str(time_h_mod)
		if time_m_mod < 10:
			time_m_mod = "0" + str(time_m_mod)
		if time_s_mod < 10:
			time_s_mod = "0" + str(time_s_mod)

		return f"{time_h_mod}:{time_m_mod}:{time_s_mod} (H)"


def getGlanceValues():
    cnt=0;
    existing_from_dt, existing_to_dt = getFromToDT()
    query = f"""
        SELECT USER_ID , RES1 , COUNT(*) as cnt FROM tblproworkingdetails WHERE SYNC_TIME>'{existing_from_dt}' AND SYNC_TIME<'{existing_to_dt}' GROUP BY USER_ID ,RES1 ;
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
                
    user_counts = {}

    for name,status,count in results:
        if name not in user_counts:
            user_counts[name]={'Idle':0,'PRO':0,"UNPRO":0}
        user_counts[name][status]=count


    for name,counts in user_counts.items():
        counts['Idle'] = convertCountToTime(counts['Idle'])
        counts['PRO'] = convertCountToTime(counts['PRO'])
        counts['UNPRO'] = convertCountToTime(counts['UNPRO'])


    print(user_counts)


    return user_counts


