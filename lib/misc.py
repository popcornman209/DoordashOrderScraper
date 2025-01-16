import pickle, time, json, pandas
from datetime import datetime, timedelta
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QStackedWidget, QWidget, QVBoxLayout, QLabel, QPushButton

class BasePage: #base page for all gui pages
    def __init__(self, container_widget: QStackedWidget):
        self.page = QWidget() #main page
        self.container_widget = container_widget #container that stores all pages

    def show(self): # Switch to this page in the stacked widget.
        self.container_widget.setCurrentWidget(self.page)

class basicMessage(BasePage):
    def __init__(self, container_widget: QStackedWidget):
        super().__init__(container_widget)

        self.buttonMethod = None #method that button runs when pressed
        self.layout = QVBoxLayout(self.page)

        self.message = QLabel("<text here lol>") #text that can be changed
        self.message.setAlignment(Qt.AlignCenter) #alignment
        self.layout.addWidget(self.message)

        self.layout.addStretch() #put buttons and labels at bottom
        self.bottomMessage = QLabel("working...") #bottom text
        self.bottomMessage.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.bottomMessage)

        self.continueButton = QPushButton("continue") #buttom button
        self.layout.addWidget(self.continueButton)
    def dispMessage(self,text,method = None):
        self.message.setText(text) #set top text
        if self.buttonMethod: #if button had a method previously
            self.continueButton.clicked.disconnect(self.buttonMethod)
            self.buttonMethod = None #remove and disconnect it
        if method: #if button should be used
            self.continueButton.setVisible(True) #show the button
            self.bottomMessage.setVisible(False) #and hide the bottom text
            self.continueButton.clicked.connect(method) #connect the button to method
            self.buttonMethod = method #set current method, used for deleting it later
            log('showed basic button menu "{}"'.format(text))
        else: #if button shouldnt be used
            self.continueButton.setVisible(False) #hide button
            self.bottomMessage.setVisible(True) #show "working..." text
            log('showed basic menu "{}"'.format(text))
        self.show() #display page

def getDate(order): #gets the date from the order
    parsed = order["info"].split(" • ")
    return parsed[0]

def isDateInRange(date_str, days): #checks if date is within a rangw
    current_date = datetime.now()

    date_str_with_year = f"{current_date.year}, {date_str}" # Add the current year to the date string

    date_format = "%Y, %a, %b %d" # Parse the date string into a datetime object, including the year
    date_obj = datetime.strptime(date_str_with_year, date_format)

    if date_obj > current_date: # If the date is after today, adjust it to the previous year
        date_obj = date_obj.replace(year=current_date.year - 1)

    past_date = current_date - timedelta(days=days) # Calculate the date x days ago

    return past_date <= date_obj <= current_date # Check if the date is within the last x days

def selectOrders(headless, days, orders, loadMoreMethod, driver, selectOrdersMethod, getOrdersMethod):
    if days == -1:
        if headless:
            print("\n\norders:") 
            for i in range(len(orders)-1): print("{}: {}, {} ({})".format(i+1,orders[i]["name"],orders[i]["info"],orders[i]["link"])) #prints orders
            usedOrders = input('\nwhich orders would you like to count? (seperated by ",", or type "load" to load more)\n: ') #gets list of orders
            if usedOrders == "load":
                loadMoreMethod(driver) #load more
                return True, []
            else:
                selectedOrders = []
                for order in usedOrders.split(","): #get all selected orders
                    selectedOrders.append(orders[int(order)-1]) #add them to the list
                return False, selectedOrders
        else:
            selectOrdersMethod(orders) #display get orders page
            selecting = True
            while selecting: #while still waiting for input
                selecting, loadMore, selectedOrders = getOrdersMethod() #check if buttons where pressed
                time.sleep(0.05) #wait a bit
            if loadMore: loadMoreMethod(driver) #if should load more, do so
            return loadMore,selectedOrders #return the rest
    else:
        if isDateInRange(getDate(orders[-1]),days): #if last order loaded is within range
            loadMoreMethod(driver) #load more
            return True, []
        else: #if last order loaded isnt within the range selectde
            selectedOrders = []
            for order in orders: #loop through loaded orders
                if isDateInRange(getDate(order),days): selectedOrders.append(order) #select them if within range
            return False, selectedOrders #return that ^

def export(data,type,path): #exports file
    if type == "json": #if json file
        with open(path,"w") as f:
            json.dump(data,f) #just dump the data
        log("outputted json to {}".format(path))
    elif type == "csv": #if csv...
        output = [ #start csv off with totals
            pandas.DataFrame({
                "people": list(data["spendings"].keys()),
                "money spent": [round(value, 2) for value in data["spendings"].values()],
                "store name": "TOTAL"
            })
        ]
        for order in data["orders"]: #loop through each detailed order
            orderData = data["orders"][order]

            numPeople = len(orderData["spending"]) #number of people, for formatting stuff

            outputData = { #create data
                "people": list(orderData["spending"].keys()), #list of people
                "money spent": [round(value, 2) for value in orderData["spending"].values()], #how much they spent

                "store name": [orderData["name"]] *numPeople, #store name
                "order date": [orderData["date"]] *numPeople, #date of order
                "order num of items": [orderData["numberOfItems"]] *numPeople, #number of items
                "receipt link": [order]*len(orderData["spending"]) #receipt link
            }
            for key in orderData["financial"]: #for data in detailed financial (the subtotals list)
                outputData[f"Order {key}"] = [orderData["financial"][key]] *numPeople #add it to the spreadsheet

            currentOrderOutput = pandas.DataFrame(outputData)
            output.append(currentOrderOutput) #append to the output

        combined_df = pandas.concat(output, ignore_index=True) #do whatever this does
        combined_df.to_csv(path, index=False) #save to file

        log("outputted csv to {}".format(path))
    else: raise TypeError("{} not recognized, only json and csv are supported".format(type))

def log(string): #basic log function
    time = datetime.now()
    print("{}:{}:{} ; {}".format(time.hour,time.minute,time.second,string))