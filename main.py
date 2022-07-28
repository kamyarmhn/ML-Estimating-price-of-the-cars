import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
from sklearn import linear_model

# In this project we search between Toyota models in truecar.com
# using ML algorithms, we provide an estimated price for models based on production year & mileage.

model_list = []
year_list = []
mileage_list = []
price_list = []

# Here we check 4 pages of Toyota Models in truecar site
print("Loading..., please wait")
for q in range(1, 5):
    r = requests.get('https://www.truecar.com/used-cars-for-sale/listings/toyota/?page=' + str(q))

    soup = BeautifulSoup(r.text, 'html.parser')
    models = soup.find_all(class_="vehicle-header-make-model text-truncate")
    years = soup.find_all(class_="vehicle-card-year font-size-1")
    mileages = soup.find_all(class_="d-flex w-100 justify-content-between")
    prices = soup.find_all(class_="heading-3 margin-y-1 font-weight-bold")

    for model in models:
        model_list.append(model.text)

    for year in years:
        year_list.append(year.text)

    for mileage in mileages:
        mileage_list.append(mileage.text)
        for j in range(0, len(mileage_list)):
            b = mileage_list[j].split()
            mileage_list[j] = b[0]
            mileage_list[j] = mileage_list[j].replace(',', '')

    for price in prices:
        price_list.append(price.text)
        for k in range(0, len(price_list)):
            price_list[k] = price_list[k].replace('$', '')
            price_list[k] = price_list[k].replace(',', '')

DB_NAME = 'Project_Jadi'

TABLES = {'Final_Project': (
    "CREATE TABLE `Final_Project` ("
    "  `Model` varchar(100),"
    "  `Year` varchar(100),"
    "  `Mileage` varchar(100),"
    "  `Price` varchar(100)"
    ") ENGINE=InnoDB")}

# username = input('insert your database user: ')
# password = input(' insert your database password: ')
cnx = mysql.connector.connect(user='root', password='*', host='localhost')
cursor = cnx.cursor()


def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

for Final_Project in TABLES:
    table_description = TABLES[Final_Project]
    try:
        print("Creating table {}: ".format(Final_Project), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK")

cnx = mysql.connector.connect(user='root', password='*', host='localhost', database=DB_NAME)
cursor = cnx.cursor()

add_car = ("INSERT IGNORE INTO Final_Project (Model, Year, Mileage, Price) VALUES (%s, %s, %s, %s)")

data_car = (model_list, year_list, mileage_list, price_list)

for i in range(0, len(model_list)):
    data_car = (model_list[i], year_list[i], mileage_list[i], price_list[i])
    cursor.execute(add_car, data_car)

cnx.commit()
cursor.close()
cnx.close()

car = []
cars = []
for z in range(0, len(model_list)):
    car.append([model_list[z], year_list[z], mileage_list[z], price_list[z]])
    if 'Toyota' in car[z][0]:
        cars.append(car[z])

for v in range(0, len(cars)):
    if 'MR2 Spyder' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota MR2 Spyder', '73')
    if '4Runner' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota 4Runner', '16')
    if 'GR86' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota GR86', '9')
    if '86' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota 86', '30')
    if 'Avalon' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota Avalon', '14')
    if 'C-HR' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota C-HR', '3')
    if 'Camry' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota Camry', '6')
    if 'Camry Solara' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota Camry Solara', '31')
    if 'Celica' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota Celica', '32')
    if 'Corolla iM' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota Corolla iM', '33')
    if 'Corolla' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota Corolla', '999')
    if 'Corolla Cross' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota Corolla Cross', '4')
    if 'Corolla Hatchback' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota Corolla Hatchback', '2')
    if 'Echo' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota Echo', '45')
    if 'FJ Cruiser' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota FJ Cruiser', '34')
    if 'GR Supra' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota GR Supra', '18')
    if 'Highlander' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota Highlander', '13')
    if 'Land Cruiser' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota Land Cruiser', '20')
    if 'Matrix' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota Matrix', '35')
    if 'Prius v' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota Prius v', '38')
    if 'Prius Prime' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota Prius Prime', '10')
    if 'Prius c' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota Prius c', '37')
    if 'Prius' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota Prius', '5')
    if 'RAV4 Prime' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota RAV4 Prime', '17')
    if 'RAV4' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota RAV4', '7')
    if 'Sequoia' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota Sequoia', '19')
    if 'Sienna' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota Sienna', '12')
    if 'T100' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota T100', '40')
    if 'Tacoma' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota Tacoma', '8')
    if 'Tundra' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota Tundra', '15')
    if 'Venza' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota Venza', '11')
    if 'Yaris iA' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota Yaris iA ', '42')
    if 'Yaris' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota Yaris', '50')
    if 'Mirai' in cars[v][0]:
        cars[v][0] = cars[v][0].replace('Toyota Mirai', '12')

x = []
y = []

for u in range(0, len(cars)):
    x.append((cars[u][:3]))
    y.append(cars[u][3])

    for ozv in x:
        for adad in range(0, 3):
            ozv[adad] = float(ozv[adad])

y = [float(ozv2) for ozv2 in y]

model_of_car = (input('What model of Toyota to check?: (Corolla or Camry for example) ')).title()
if model_of_car == 'MR2 Spyder':
    model_of_car = 73
if model_of_car == '4Runner':
    model_of_car = 16
if model_of_car == 'Avalon':
    model_of_car = 14
if model_of_car == 'C-HR':
    model_of_car = 3
if model_of_car == 'Camry':
    model_of_car = 6
if model_of_car == 'Corolla iM':
    model_of_car = 33
if model_of_car == 'Corolla':
    model_of_car = 999
if model_of_car == 'Corolla Cross':
    model_of_car = 4
if model_of_car == 'Corolla Hatchback':
    model_of_car = 2
if model_of_car == 'GR Supra':
    model_of_car = 18
if model_of_car == 'GR86':
    model_of_car = 9
if model_of_car == 'Highlander':
    model_of_car = 13
if model_of_car == 'Land Cruiser':
    model_of_car = 20
if model_of_car == 'Prius':
    model_of_car = 5
if model_of_car == 'Prius Prime':
    model_of_car = 10
if model_of_car == 'RAV4':
    model_of_car = 7
if model_of_car == 'RAV4 Prime':
    model_of_car = 17
if model_of_car == 'Sequoia':
    model_of_car = 19
if model_of_car == 'Sienna':
    model_of_car = 12
if model_of_car == 'Tacoma':
    model_of_car = 8
if model_of_car == 'Tundra':
    model_of_car = 15
if model_of_car == 'Venza':
    model_of_car = 11
if model_of_car == 'Mirai':
    model_of_car = 12
if model_of_car == '86':
    model_of_car = 30
if model_of_car == 'Camry Solara':
    model_of_car = 31
if model_of_car == 'Celica':
    model_of_car = 32
if model_of_car == 'Echo':
    model_of_car = 45
if model_of_car == 'FJ Cruiser':
    model_of_car = 34
if model_of_car == 'Matrix':
    model_of_car = 35
if model_of_car == 'Prius c':
    model_of_car = 37
if model_of_car == 'Prius v':
    model_of_car = 38
if model_of_car == 'Yaris':
    model_of_car = 50
if model_of_car == 'Yaris iA':
    model_of_car = 42

che_sali = int(input('Year of car production: '))
che_mileagi = int(input('Mileage of car: '))

regr = linear_model.LinearRegression()

regr.fit(x, y)
answer = regr.predict([[model_of_car, che_sali, che_mileagi]])

print('The approximate price of your car:', int(answer[0]), '$')
