import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from scipy.optimize import minimize #, rosen, rosen_der
import seaborn as sb
 

#Pulls in monthly and weekly DOW30 stock prices back to 2000 from CSV files, drops columns with incomplete price history

 

data_weekly = pd.read_csv('data/data_weekly.csv')

data_weekly.drop(['V', 'DOW'], axis=1, inplace=True)

data_weekly.Date = pd.to_datetime(data_weekly.Date)

data_weekly.set_index('Date', inplace=True)

 

data_monthly = pd.read_csv('data/data_monthly.csv')

data_monthly.drop(['V', 'DOW'], axis=1, inplace=True)

data_monthly.Date = pd.to_datetime(data_monthly.Date)

data_monthly.set_index('Date', inplace=True)

 

log_weekly = np.log(data_weekly/data_weekly.shift(1))

log_weekly = log_weekly.iloc[1:]

 

log_monthly = np.log(data_monthly/data_monthly.shift(1))

log_monthly = log_monthly.iloc[1:]

 
print(log_monthly)


################ Cor Mat and Moving Window code:

data = data_weekly

print(data.columns.values)

names_list = data.columns.values
chi_col_list = []

for col in data:
    # chi_col will hold our % changes
    chi_col = []

    c_col = list(data[col])

	# use this if the columns are different lengths and you only want the most recent 10 years:
    #point = stock_df.shape[0]-520

    # % increease = close - prev_close / prev_close
    # we want stocks with low VAR of this, high SUM of this

    init_prev_close = c_col[0] #just get the first one

    for i in range(0,data.shape[0]):
        close = c_col[0]
        
        if (i == 0):
            prev_close = init_prev_close
            # make % increase
            _1_chi = (close - init_prev_close) / init_prev_close
        else:
            prev_close = c_col[i-1]

            _1_chi = (close - prev_close) / prev_close

        chi_col.append(_1_chi)

    chi_col_list.append(chi_col)

# now we have a name list and a chi_col_list, could make a cov matrix with this
#print(names_list)
#print(chi_col_list)
#print(len(chi_col_list))
#print(len(chi_col_list[0]))
#for i in range(0, len(chi_col_list)):
#    print(len(chi_col_list[i]))
#    print(names_list[i])


chi_df = np.array(chi_col_list).T
#print(chi_df.shape)

chi_df = pd.DataFrame(chi_df, columns = names_list)
#print(chi_df)

chi_cov = np.cov(chi_df.T)
#print(chi_cov.shape)

chi_cor = np.corrcoef(chi_df.T)
chi_cor = pd.DataFrame(chi_cor, columns = names_list)
chi_cor.index = names_list

#heat_map = sb.heatmap(chi_cov)
#plt.show()


# HERE IS THE CORRELATION MATRICES

heat_map = sb.heatmap(chi_cor, annot = True, xticklabels = 1, yticklabels = 1)
plt.show()



# MAKE A MOVING WINDOW THAT CONSIDERS A 6-MOTH STOCK SUBSET, CAPTURE ITS MEAN CORR:

print(data.shape)
iterations = data.shape[0]

moving_window_size = 10 # size in months of moving window

moving_cor_list = []

for i in range(0, iterations - moving_window_size):

	data_subset = data[i:moving_window_size]

	subset_cor = np.corrcoef(data_subset)
	print(subset_cor.shape)

	subset_cor_mean = subset_cor.mean(axis = 1).mean(axis = 0)

	moving_cor_list.append(subset_cor_mean)



### THIS CODE IS JUST TO CALCULATE THE MEAN AND VARIANCE OF THE CHI COLS, CAN IGNORE:::
# which have lowest variance and highest mean?

#sd_row = list(np.apply_along_axis(statistics.stdev, axis = 0, arr = chi_df))
#print('lowest sd: ', names_list[sd_row.index(min(sd_row))])

#mean_row = list(np.apply_along_axis(statistics.mean, axis = 0, arr = chi_df))
#print('highest mean: ', names_list[mean_row.index(max(mean_row))])

#q_stat = []

#for i in range(0, chi_df.shape[1]):
#    num = mean_row[i] / sd_row[i]
#    q_stat.append(num)

#print('highest q_stat: ', names_list[q_stat.index(max(q_stat))])

#plt.plot(mean_row, sd_row)

#plt.show()

#print('done??')