'''
to manage your stocks on NSE
lopez.steven01@gmail.com
'''
from nsetools import Nse
import time
nse = Nse()

def timeit(method):
    def timed(*args, **kw):
        print("Started executing function:%s" % method.__name__)
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r  %2.2f s' % (method.__name__, (te - ts)))
        return result

    return timed

def get_details(temp):
    if type(temp) is dict:
        holdings = {}
        columns= ['companyName', 'lastPrice', 'change', 'totalBuyQuantity', 'totalSellQuantity']
        columns2 = ['CompanyName', 'Price', 'Change', 'SellQty', 'BuyQty']
        for name, cols in zip(columns, columns2):
                holdings[cols]=temp.get(name)
        return holdings
    
def comb_holds(name, holdings, all_holdings):
    all_holdings[name]= holdings
    
def check_codes(st_dict):
    final= {}
    c_all = nse.get_stock_codes().keys()
    check = [item for item in st_dict.keys() if item in c_all]
    for x in check:
        final[x] = st_dict.get(x)
    return final

def read_holdings(file):
    import csv
    st_dict2={}
    with open(file, mode='r') as infile:
        reader = csv.reader(infile)
        reader=list(reader)[1:]
        for row in reader:
            st_dict2[row[0]]={}
            st_dict2[row[0]]['no']=float(row[1])
            st_dict2[row[0]]['ltp']=float(row[2])
    return (st_dict2)

def cal_holds(st_dict, all_holdings):
    import sys
    original_stdout = sys.stdout 
    with open('/home/pi/pi/adownload/Begin_report.txt', 'w') as f:
        sys.stdout = f
        print('*************************REPORT*************************\n')
        pos,neg,bal = 0,0,0
        for x in (st_dict.keys()):
            old_val = st_dict.get(x).get('no') * st_dict.get(x).get('ltp')
            new_val = st_dict.get(x).get('no') * all_holdings.get(x).get('Price')
            diff = new_val - old_val
            bal += old_val
            if diff>0:
                pos += diff
            else:
                neg += diff
            print('%s | %0*d Shares | Value: %0*d | Earning: %0*d' %(x.ljust(11), 3,st_dict.get(x).get('no'), 5,new_val, 5,diff))
        print('\nInvested: %0*d | Positives: %0*d | Negatives: %0*d' %(5, bal, 5, pos, 5, neg))
        sys.stdout = original_stdout

@timeit    
def main(file):
    all_holdings= {}
    st_dict=check_codes(read_holdings(file))
    for x in st_dict.keys():
        temp = nse.get_quote(x)
        holdings = get_details(temp)
        comb_holds(x, holdings, all_holdings)
    cal_holds(st_dict,all_holdings)
    
main('/home/pi/project/MAL.csv')