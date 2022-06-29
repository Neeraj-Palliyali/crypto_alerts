def check_status(limit, alert_on, current_val):
    if alert_on == "G":
        val = False if current_val > limit else  True 

    elif  alert_on == "GE":        
        val = False if current_val >= limit else  True 

    elif  alert_on == "E":        
        val = False if current_val == limit else  True 
    
    elif  alert_on == "LE":        
        val = False if current_val <= limit else  True 
    
    elif  alert_on == "L":        
        val = False if current_val < limit else  True 

    return val