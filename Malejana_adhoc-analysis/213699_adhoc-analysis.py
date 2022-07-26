# Opening the JSON File
import pandas as pd
import json
import matplotlib.pyplot as plt
import datetime
import calendar
path = './transaction-data-adhoc-analysis.json'
df = pd.read_json(path)

# Adding a transaction month 
def date(x):
    
    month = int(x[6:len(x)-3])
    m = calendar.month_name[month]
    return m

df['Month of Transaction'] = df['transaction_date'].apply(date).astype(pd.api.types.CategoricalDtype(categories=['January','February','March','April','May','June']))

# Adding state of transaction
def state(x):
    states = {'AK':'Alaska','AL':'Alabama','AR':'Arkansas','AZ':'Arizona','CA':'California','CO':'Colorado','CT':'Connecticut','DC':'District of Columbia',
    'DE':'Delaware','FL':'Florida','GA':'Georgia','HI':'Hawaii','IA':'Iowa','ID':'Idaho','IL':'Illinois','IN':'Indiana','KS':'Kansas',
    'KY':'Kentucky','LA':'Louisiana','MA':'Massachusetts','MD':'Maryland','ME':'Maine','MI':'Michigan','MN':'Minnesota','MO':'Missouri',
    'MS':'Mississippi','MT':'Montana','NC':'North Carolina','ND':'North Dakota','NE':'Nebraska','NH':'New Hampshire','NJ':'New Jersey',
    'NM':'New Mexico','NV':'Nevada','NY':'New York','OH':'Ohio','OK':'Oklahoma','OR':'Oregon','PA':'Pennsylvania','RI':'Rhode Island',
    'SC':'South Carolina','SD':'South Dakota','TN':'Tennessee','TX':'Texas','UT':'Utah','VA':'Virginia','VT':'Vermont','WA':'Washington',
    'WI':'Wisconsin','WV':'West Virginia','WY':'Wyoming','AA':'Armed Forces the Americas','AE':'Armed Forces the Americas','AP':'Armed Forces Pacific'}
    abbrev = x[-8:-6]
    return states[abbrev]

df['State Location'] = df['address'].apply(state)

# Adding Customer Age Group Column 
def age_demo(x):
    age = datetime.date.today().year - int(x[0:4])
    age_group = {'Child':list(range(0,15)),'Young Adult':list(range(15,25)),
       'Adult':list(range(25,63))}
    
    if age in age_group['Child']:
        return('Child (0–14 yrs old)')
    elif age in age_group['Young Adult']:
        return('Young Adult (15–24 yrs old)')
    elif age in age_group['Adult']:
        return('Adult (25–62 yrs old)')
    else:
        return('Senior (62+ yrs old)')

df['Customer Age Group'] = df['birthdate'].apply(age_demo).astype(pd.api.types.CategoricalDtype(categories=['Child (0–14 yrs old)','Young Adult (15–24 yrs old)',
                                                                                                            'Adult (25–62 yrs old)','Senior (62+ yrs old)']))

# Seperating the transaction items to different rows
df['transaction_items'] = df['transaction_items'].str.split(";")
one_df = df.explode('transaction_items',True)

# Making a quantity column for transaction items
def quant_items(x):
    charset = [
        *[str(i) for i in range(10)]
    ]
    x = ''.join([i for i in x if i in charset])
    return int(x[-1])

one_df['Quantity Per Item'] = one_df['transaction_items'].apply(quant_items)

# Removing the item quantity string in the transaction item column
def remove(x):
    return x[:len(x)-5]

one_df['transaction_items'] = one_df['transaction_items'].apply(remove)

# Formatting item name
def item(x):
    final_item = x.split(",")[1]
    return (final_item)

one_df['transaction_items'] = one_df['transaction_items'].apply(item)

# Finding the price per item 
price_list = {'Beef Chicharon': list(one_df.loc[(one_df.transaction_items == 'Beef Chicharon')].min(numeric_only=True))[0], 
              'Nutrional Milk':list(one_df.loc[(one_df.transaction_items == 'Nutrional Milk')].min(numeric_only=True))[0],
              'Gummy Vitamins': list(one_df.loc[(one_df.transaction_items == 'Gummy Vitamins')].min(numeric_only=True))[0],
              'Gummy Worms':list(one_df.loc[(one_df.transaction_items == 'Gummy Worms')].min(numeric_only=True))[0],
              'Kimchi and Seaweed':list(one_df.loc[(one_df.transaction_items == 'Kimchi and Seaweed')].min(numeric_only=True))[0],
              'Yummy Vegetables':list(one_df.loc[(one_df.transaction_items == 'Yummy Vegetables')].min(numeric_only=True))[0],
              'Orange Beans':list(one_df.loc[(one_df.transaction_items == 'Orange Beans')].min(numeric_only=True))[0]}

# Adding price per item column
def price_per_item(x):
    return price_list[x]
    
one_df['Price Per Item'] = one_df['transaction_items'].apply(price_per_item)

# Multiplying quantity per item to price per item 
one_df['Total Price Per Item'] = one_df['Quantity Per Item'] * one_df['Price Per Item']

# Renaming Columns
one_df.rename(columns = {'name':'Customer Name','transaction_items':'Item Per Transaction',
                         'transaction_value':'Total Sale Value',
                         'transaction_date':'Transaction Date','address':'Address','birthdate':'Birthdate'}, inplace=True)
# Arranging the columns
one_df = one_df[['Customer Name','Item Per Transaction','Price Per Item','Quantity Per Item','Total Price Per Item','Total Sale Value',
                 'Month of Transaction','State Location','Birthdate','Customer Age Group','sex']]

# Pivot table for the count of each item sold per month
pivot1 = pd.pivot_table(one_df, index='Month of Transaction', columns='Item Per Transaction',values='Quantity Per Item',aggfunc=sum)

# Bar graph for Pivot 1
a= pivot1.plot.line(figsize=(20,10))
a.set_xlabel('Months')
a.set_ylabel('Quantity')
a.set_title('Quantity of Items Purchased')

# Pivot table for the total sale value per item per month
pivot2 = pd.pivot_table(one_df, index='Month of Transaction', columns='Item Per Transaction',values='Total Price Per Item',aggfunc='sum')

# Bar graph for Pivot 2
a= pivot2.plot.bar(figsize=(20,10))
a.set_xlabel('Months')
a.set_ylabel('Revenue in Ten Millions')
a.set_title('Total Sale Value Per Item Per Month')

# Pivot table for number of orders per item per state location
pivot3 = pd.pivot_table(one_df, columns='Item Per Transaction',index='State Location',values='Total Price Per Item',aggfunc='count',margins=True,
                        margins_name='Grand Total')

# Pivot table for number of transactions per state per month
pivot4 = pd.pivot_table(df, columns='Month of Transaction',index='State Location',values='transaction_date',aggfunc='count')

# Pivot table for average total transaction per item per month
pivot5 = pd.pivot_table(one_df, index='Item Per Transaction',columns='Month of Transaction',values='Total Price Per Item',aggfunc='mean')

# Pivot table for average total transaction in each state location per item
pivot6 = pd.pivot_table(one_df, index='State Location',columns='Item Per Transaction',values='Total Price Per Item',aggfunc='mean')

# Pivot table for 
pivot7 = pd.pivot_table(df, columns='Customer Age Group',index='State Location',values='transaction_date',aggfunc='count')

# Pivot table for the customer age demographic of items bought
pivot8= pd.pivot_table(one_df, columns='Customer Age Group',index='Item Per Transaction',values='Customer Name',aggfunc='count')

# Bar graph for Pivot 8
a= pivot8.plot.barh(figsize=(20,10))
a.set_xlabel('Amount Purchased', fontsize=15)
a.set_ylabel('Items', fontsize=15)
a.set_title('Age Demographic Per Item', fontsize=15)

# Pivot table for monthly orders for each customer
df['bin']=1

bincheck = pd.pivot_table(df,index='name',columns='Month of Transaction',
                          values='bin',aggfunc='count')
# Repeater customers
Repeater = {'January':0, 
            'February':len(bincheck[(bincheck.January >= 1) & (bincheck.February >= 1)]),
            'March':len(bincheck[(bincheck.February >= 1) & (bincheck.March >= 1)]),
            'April':len(bincheck[(bincheck.March >= 1) & (bincheck.April >= 1)]),
            'May': len(bincheck[(bincheck.April >= 1) & (bincheck.May >= 1)]),
            'June': len(bincheck[(bincheck.May >= 1) & (bincheck.June >= 1)])}

# Inactive customers 
Inactive = {'January':0, 
            'February':len(bincheck[(bincheck.January >= 1) & (bincheck.February == 0)]),
            'March':len(bincheck[(bincheck.January >= 0) & (bincheck.February >= 0) & (bincheck.March == 0)])-len(bincheck[(bincheck.January == 0) & (bincheck.February == 0) & (bincheck.March == 0)]),
            'April':len(bincheck[(bincheck.January >= 0) & (bincheck.February >= 0) & (bincheck.March >= 0) & (bincheck.April == 0)]) - len(bincheck[(bincheck.January == 0) & (bincheck.February == 0) & (bincheck.March == 0) & (bincheck.April == 0)]),
            'May': len(bincheck[(bincheck.January >= 0) & (bincheck.February >= 0) & (bincheck.March >= 0) & (bincheck.April >= 0) & (bincheck.May == 0)]) - len(bincheck[(bincheck.January == 0) & (bincheck.February == 0) & (bincheck.March == 0) & (bincheck.April == 0) & (bincheck.May == 0)]),
            'June': len(bincheck[(bincheck.January >= 0) & (bincheck.February >= 0) & (bincheck.March >= 0) & (bincheck.April >= 0) & (bincheck.May >= 0) & (bincheck.June == 0)])-- len(bincheck[(bincheck.January == 0) & (bincheck.February == 0) & (bincheck.March == 0) & (bincheck.April == 0) & (bincheck.May == 0) & (bincheck.June == 0)])}

# Engaged customers
Engaged = {'January':New['January'], 
            'February':Repeater['February'] + New['February'],
            'March': New['March'] + Repeater['March'],
            'April': New['April'] + Repeater['April'],
            'May': New['May'] + Repeater['May'],
            'June': New['June'] + Repeater['June']}

# Returner customers (Customers that  had previous transactions that became inactive for 1 month and purchased again. This metric is 0 for January and February.)
Returner = {'January':0, 
            'February':0,
            'March':len(bincheck[(bincheck.January >= 1) & (bincheck.February == 0) & (bincheck.March >= 1)]),
            'April':len(bincheck[(bincheck.February >= 1) & (bincheck.March == 0) & (bincheck.April >= 1)]),
            'May': len(bincheck[(bincheck.March >= 1) & (bincheck.April == 0) & (bincheck.May >= 1)]),
            'June': len(bincheck[(bincheck.April >= 1) &(bincheck.May == 0) & (bincheck.June >= 1)])}


# New Customers (They ordered for the first time in 2022 and do not have any prior transactions before the month that they purchased in. This does not include transactions from previous years.)
New = {'January':len(bincheck[bincheck.January >= 1]), 
       'February':len(bincheck[(bincheck.January == 0) & (bincheck.February >= 1)]),
       'March':len(bincheck[(bincheck.January == 0) & (bincheck.February == 0) & (bincheck.March >= 1)]),
       'April':len(bincheck[(bincheck.January == 0) & (bincheck.February == 0) & (bincheck.March == 0) & (bincheck.April >= 1)]),
       'May': len(bincheck[(bincheck.January == 0) & (bincheck.February == 0) & (bincheck.March == 0) & (bincheck.April == 0) & (bincheck.May >= 1)]),
       'June': len(bincheck[(bincheck.January == 0) & (bincheck.February == 0) & (bincheck.March == 0) & (bincheck.April == 0) &(bincheck.May == 0) & (bincheck.June >= 1)])}

# Big Time Customers (They are customers who consistently purchased more than once a month since January)
Big_Time = {'January':len(bincheck[bincheck.January >= 1]), 
            'February':len(bincheck[(bincheck.January >= 1) & (bincheck.February >= 1)]),
            'March':len(bincheck[(bincheck.January >= 1) & (bincheck.February >= 1) & (bincheck.March >= 1)]),
            'April':len(bincheck[(bincheck.January >= 1) & (bincheck.February >= 1) & (bincheck.March >= 1) & (bincheck.April >= 1)]),
            'May': len(bincheck[(bincheck.January >= 1) & (bincheck.February >= 1) & (bincheck.March >= 1) & (bincheck.April >= 1) & (bincheck.May >= 1)]),
            'June': len(bincheck[(bincheck.January >= 1) & (bincheck.February >= 1) & (bincheck.March >= 1) & (bincheck.April >= 1) & (bincheck.May >= 1) & (bincheck.June >= 1)])}

# Customer Metric Table
two_df = pd.DataFrame({'Repeater':Repeater,
        'Inactive': Inactive,
        'Engaged': Engaged,
        'Returner': Returner,
        'New':New,
        'Big Time':Big_Time
       })

two_df.transpose()


#Customer Metric Line Graph
plt.plot(two_df['Repeater'], color='red', marker='o',label='Repeater')
plt.plot(two_df['Inactive'], color='blue', marker='o',label='Inactive')
plt.plot(two_df['Engaged'], color='green', marker='o',label='Engaged')
plt.plot(two_df['Returner'], color='purple', marker='o',label='Returner')
plt.plot(two_df['New'], color='orange', marker='o',label='New')
plt.plot(two_df['Big Time'], color='pink', marker='o',label='Big Time')
plt.title('Customer Metrics', fontsize=14)
plt.xlabel('Months', fontsize=14)
plt.ylabel('Number of Customers', fontsize=14)
plt.legend()
plt.grid(True)
plt.show()