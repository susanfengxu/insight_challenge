
# coding: utf-8

# In[ ]:


import os as os
# read the actual.txt and break each line by delimiter "|"
txt=[] # act_txt will be a list of all information
with open('.' + os.sep + 'input'+ os.sep + 'actual.txt','r') as f:
    for line in f:
        for word in line.split('|'):
            txt.append(word)
f.close()
hour_act = [int(txt[x]) for x in range(0, len(txt),3)] # extract the hour from the list of all
ID_act = [txt[x] for x in range(1, len(txt),3)] # extract the stock ID from the list of all
price_act = [float(txt[x].strip("\n")) for x in range(2, len(txt),3)] # extract the price from the list of all

# read the predict.txt and break each line by delimiter "|"
txt=[] # act_txt will be a list of all information
with open('.' + os.sep + 'input'+ os.sep +'predicted.txt','r') as f:
    for line in f:
        for word in line.split('|'):
            txt.append(word)
hour_prd = [int(txt[x]) for x in range(0, len(txt),3)] # extract the hour from the list of all
ID_prd = [txt[x] for x in range(1, len(txt),3)] # extract the stock ID from the list of all
price_prd = [float(txt[x].strip("\n")) for x in range(2, len(txt),3)] # extract the price from the list of all
txt=[]

# read the window.txt
f=open('.'+ os.sep + 'input'+ os.sep + "window.txt","r")
window=f.read()
f.close()
window = int(window)


# extract_hourly_data function will extract the hour defined by h1 from data lists, i.e. hour list, stock ID list, stock price list
def extract_hourly_data(hour_list, ID_list, price_list, h1): 
    max_hour = max(hour_list)
    if h1<= max_hour-1:
        try:
            hour_index_start = hour_list.index(h1)  # index at hour list of the first occurence, record this index will let the next hour search start from here
            try:
                hour_index_finish = hour_list.index(h1 + 1)  # index at hour list of the first occurence of next hour
            except: # if next hour is empty, then skip this and go to the next one
                if h1+2 <= max_hour:
                    hour_index_finish = hour_list.index(h1 + 2) 
                
            h1_hour_list = hour_list[hour_index_start:hour_index_finish]
            h1_ID_list = ID_list[hour_index_start:hour_index_finish]
            h1_price_list = price_list[hour_index_start:hour_index_finish]
        except : # if current hour i.e. h1 is empty, then return empty lists
            h1_hour_list=[]
            h1_ID_list=[] 
            h1_price_list=[]
            hour_index_start = 0
    return h1_hour_list, h1_ID_list, h1_price_list, hour_index_start


# sort_ID_price function will sort the ID_list by alphabetical order to match the ID between predict and actual faster
def sort_ID_price(ID_list, price_list):
    tp = sorted(zip(ID_list, price_list))
    new_ID_list, new_price_list = [t[0] for t in tp], [t[1] for t in tp]
    return new_ID_list, new_price_list


# get_error_by_matchingID function will match the ID between predict and actual then compute the error = abs(actual-predict)
def get_error_by_matchingID(hour_list_prd,ID_list_prd, price_list_prd, hour_list_act, ID_list_act, price_list_act):
    index_start_match = 0 # this is the starting index at actual stock ID list to find the next stock ID
    err_ID_list = [] # this is the list of stock IDs for the list error-of-prediction, same as prediction list
    err_hour_list = [] # this is the list of hours for the list error-of-prediction, same as prediction list
    err_price_list = [] # this is the list of errors in predicted stock prices, i.e. abs(actual-predict)

    #import pdb; pdb.set_trace()
    for i_prd in range(len(ID_list_prd)):
        tmp_ID = ID_list_prd[i_prd] # tmp_ID is one of stock IDs in the predicted list
        try:
            index_act = ID_list_act[index_start_match:].index(tmp_ID) + index_start_match       
            index_start_match = index_act
            err_ID_list.append(tmp_ID)
            err_hour_list.append(hour_list_prd[i_prd])
            err_price_list.append(abs(price_list_act[index_act]-price_list_prd[i_prd]))
        except :
            print("stock ID in predicted '%s' is not found in actual stock ID \n", tmp_ID)
            continue
    return err_hour_list, err_ID_list, err_price_list

# average_list function will calculate the average of the error in the given list
def average_list(err_price_list):
    if err_price_list: # if the list is not empty
        avg = sum(err_price_list)/len(err_price_list)
    else:
        avg = None    
    return avg

# format_value function will format the value list to the second decimal point
def format_value(value):
    return "%.2f" % value

error_hour_in_window = [] # hour list in a size of one sliding window long 
error_ID_in_window = [] # stock ID list in a size of one sliding window long 
error_price_in_window = [] # price error list in a size of one sliding window long 
res_hour_from = [] # result to print of the list for the starting hour
res_hour_to = [] # result to print of the list for the ending hour
res_avg_err = [] # result to pritn of the list for averaged price error at a given starting and ending hour window


# asssuming the list of hours is continuous without a gap
hour_start_index_prd = 0
hour_start_index_act = 0
for i_h in range(0, window): # forming the first time window error list from predict list and actual list hour by hour, to extend the whole window list
    next_hour =  i_h + 1
    #h1_hour_list_prd, h1_ID_list_prd, h1_price_list_prd, hour_index_prd =  extract_hourly_data(hour_prd[hour_start_index_prd:], ID_prd, price_prd, next_hour)
    h1_hour_list_prd, h1_ID_list_prd, h1_price_list_prd, hour_index_prd =  extract_hourly_data(hour_prd, ID_prd, price_prd, next_hour)
    #hour_index_prd = hour_index_prd + hour_start_index_prd
    #hour_start_index_prd = hour_index_prd
    if h1_hour_list_prd:
        h1_ID_list_prd, h1_price_list_prd = sort_ID_price(h1_ID_list_prd, h1_price_list_prd)
        #h1_hour_list_act, h1_ID_list_act, h1_price_list_act, hour_index_act =  extract_hourly_data(hour_act[hour_start_index_act:], ID_act, price_act, next_hour)
        h1_hour_list_act, h1_ID_list_act, h1_price_list_act, hour_index_act =  extract_hourly_data(hour_act, ID_act, price_act, next_hour)
        #hour_index_act = hour_index_act + hour_start_index_act
        #hour_start_index_act = hour_index_act
        h1_ID_list_act, h1_price_list_act = sort_ID_price(h1_ID_list_act, h1_price_list_act)
        h1_err_hour_list, h1_err_ID_list, h1_err_price_list = get_error_by_matchingID(h1_hour_list_prd,h1_ID_list_prd, 
                                                                                      h1_price_list_prd, h1_hour_list_act, 
                                                                                      h1_ID_list_act, h1_price_list_act)
        error_hour_in_window.extend(h1_err_hour_list)
        error_ID_in_window.extend(h1_err_ID_list)
        error_price_in_window.extend(h1_err_price_list)
    else:
        continue
    
next_hour = next_hour + 1 
window_start_hour = 1  # the first window start hour
res_hour_from.append(window_start_hour) # window start hour list
window_end_hour = window  # the first window end hour
res_hour_to.append(window_end_hour) # window end hour list
avg = average_list(error_price_in_window)  # average the first window of error price
if avg: # if the average is a number, then save it to the result list
    res_avg_err.append(avg)
end_hour = max(hour_prd)

# from the second window, error list is extend by one hour at the end, then remove the beginning hour
# next_hour, the hour index, move from window+1 to end_hour-1
hour_prd.append(end_hour+1)
hour_act.append(end_hour+1)
for next_hour in range(window+1,end_hour+1):
    #h1_hour_list_prd, h1_ID_list_prd, h1_price_list_prd, hour_index_prd =  extract_hourly_data(hour_prd[hour_start_index_prd:], ID_prd, price_prd, next_hour) # obtain another hour of data from prediction
    h1_hour_list_prd, h1_ID_list_prd, h1_price_list_prd, hour_index_prd =  extract_hourly_data(hour_prd, ID_prd, price_prd, next_hour)
    #hour_index_prd = hour_index_prd + hour_start_index_prd
    #hour_start_index_prd = hour_index_prd
    if h1_hour_list_prd: # if this hour is not empty in predict
        h1_ID_list_prd, h1_price_list_prd = sort_ID_price(h1_ID_list_prd, h1_price_list_prd) # sort for faster stock ID matching
        #h1_hour_list_act, h1_ID_list_act, h1_price_list_act, hour_index_act =  extract_hourly_data(hour_act[hour_start_index_act:], ID_act, price_act, next_hour) # obtain another hour of data from actual
        h1_hour_list_act, h1_ID_list_act, h1_price_list_act, hour_index_act =  extract_hourly_data(hour_act, ID_act, price_act, next_hour) # obtain another hour of data from actual
        #hour_index_act = hour_index_act + hour_start_index_act
        #hour_start_index_act = hour_index_act
        h1_ID_list_act, h1_price_list_act = sort_ID_price(h1_ID_list_act, h1_price_list_act) # sort for faster stock ID matching
        # match stock ID between predict and actual and calculate the error of predicted price
        h1_err_hour_list, h1_err_ID_list, h1_err_price_list = get_error_by_matchingID(h1_hour_list_prd,h1_ID_list_prd, 
                                                                                      h1_price_list_prd, h1_hour_list_act, 
                                                                                      h1_ID_list_act, h1_price_list_act)
    else: # if the next hour is empty in predict hour list, then return empty error list
        h1_err_hour_list = [];
        h1_err_ID_list = [];
        h1_err_price_list = [];
        
    window_start_hour = window_start_hour + 1 # move on the next hour window
    window_end_hour = window_end_hour + 1  # move on the next hour window
    error_hour_in_window.extend(h1_err_hour_list) # extend the hour window list
    error_ID_in_window.extend(h1_err_ID_list) # extend the hour window list
    error_price_in_window.extend(h1_err_price_list) # extend the error list of the hour window
    try:
        index_err_hour_remove = error_hour_in_window.index(window_start_hour) # find the index of beginning hour from the list
        error_hour_in_window = error_hour_in_window[index_err_hour_remove:] # cut the beginning hour from the list
        error_ID_in_window = error_ID_in_window[index_err_hour_remove:] # cut the beginning hour from the list
        error_price_in_window = error_price_in_window[index_err_hour_remove:] # cut the beginning hour from the list
        res_hour_from.append(window_start_hour) # if the hour of stock is not empty, then extend this window to the result
        res_hour_to.append(window_end_hour)  # if the hour of stock is not empty, then extend this window to the result
        res_avg_err.append(average_list(error_price_in_window))  # if the hour of stock is not empty, then extend this window to the result
    except: # if this hour is empty in stock ID, continue the next hour 
        print("Hour %d has no stock ID meet the threshold on confidence prediction") %(window_start_hour)
        continue
        


formatted_res_avg_err = [format_value(v) for v in res_avg_err] # format the result

# write result to comparison text file
with open('.'+os.sep+ 'output'+ os.sep+"comparison.txt", "w") as output:
    for i in range(len(res_hour_from)):
        line = str(res_hour_from[i]) + '|' + str(res_hour_to[i]) + '|' + str(formatted_res_avg_err[i]) + '\n'
        output.write(str(line))

