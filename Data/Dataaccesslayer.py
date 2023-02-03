from Model.Employee_model import Employee
#for interacting with dynamodb we use a package called boto3
import boto3
#Package for date and time
import datetime
#For getting timezones and date time
import dateutil.tz


class DataLayer:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')

    def put_employee(self,data):
        # Insert an item into the DynamoDB table
        #We set the timezone to Asia/Kolkata so that there will not be any conflict in accessing data from different timezone
        #when adding data from different countries,the local time in their system will be converted to Asia/kolkata timezone
        desired_timezone = dateutil.tz.gettz("Asia/Kolkata")
        #iso format is a standard date and time format
        current_datetime = str(datetime.datetime.now(tz=desired_timezone))
        
        #Here Employee is an object and we are passing data as a parameter.
        employee=Employee(data['id'],data['account'],data['project'],data['empid'],data['empname'],data['purposeoftravel'],data['travelfrom'],data['travelto'],data['datefrom'],data['dateto'],data['currency'],data['flightinDollar'],data['hotacinDollar'],data['perdiuminDollar'],data['othercostinDollar'],data['totalCostindollar'],data['commentsifany'],data['approved'],current_datetime)
        self.dynamodb.Table("employeedetails1").put_item(Item=employee.__dict__())

    def get_individualemployee(self,booking_id):
        # Retrieve an item from the given DynamoDB table by its primary key
        response = self.dynamodb.Table("employeedetails1").get_item(Key={'id':booking_id})
        return response['Item']
        
    def getallemployees(self):
        # Retrieve all items from the DynamoDB table
        response = self.dynamodb.Table("employeedetails1").scan()
        return response['Items']

    #Method for filtering the data for PMO requirement
    def filterdatas_basedondate(self,expression):
        #Filter the data in the table based on the expression given and store in the variable response.
        response=self.dynamodb.Table("employeedetails1").scan(FilterExpression=expression)
        print("response",response)
        #response contains both approved and unapproved datas.PMO requires only unapproved datas.
        #For that we iterate through each response and append the unapproved datas to a new list and return it.
        #if the required unapproved datas are obtained it will return the appended list,else it will return an empty list 
        employeelist=[]
        if response:
            for i in range(0,len(response['Items'])):
                if response['Items'][i]['Status']=='unapproved':
                    employeelist.append(response['Items'][i])
                    #After the unapproved data is appended,we want to make the status of that particular record as approved
                    emp=Employee(response['Items'][i]['id'],response['Items'][i]['Account'],response['Items'][i]['Project/Contract'],response['Items'][i]['Emp ID'],response['Items'][i]['Emp Name'],response['Items'][i]['Purpose of Travel'],response['Items'][i]['Travel from'],response['Items'][i]['Travel to'],response['Items'][i]['Date from'],response['Items'][i]['Date To'],response['Items'][i]['Currency'],response['Items'][i]['Flight'],response['Items'][i]['Hotac'],response['Items'][i]['Perdiem'],response['Items'][i]['Other cost'],response['Items'][i]['Total Cost'],response['Items'][i]['Comments if Any'],'approved',response['Items'][i]['Time of Adding'])
                    self.dynamodb.Table("employeedetails1").put_item(Item=emp.__dict__())
        return employeelist            
        
        
    #Method to find whether a booking id exists in the table    
    def findanEmployee(self,booking_id):
        response=self.dynamodb.Table("employeedetails1").get_item(Key={'id':booking_id})
        return response
        
        
    #Method for deleting an employee    
    def delete_employee(self,booking_id):
        self.dynamodb.Table("employeedetails1").delete_item(Key={'id':booking_id})
        return "successfully Deleted Employee"
        
        
    #Method for validating PMO logindetails
    def logindetails_validation(self,logindetails):
        response=self.dynamodb.Table("Pmologindetails").scan(FilterExpression=logindetails)
        #if no response is found on scanning,our login is failed.Else login is success
        if response['Count']==0:
            return "Login Failed"
        else:
            return "Login Success"
            
    
    #Method for populating employeedetails in the form whenever we type Employee ID
    def getEmployeedetails_byempid(self,employeeid_filterexpression):
        #By applying scan with the help of filter expression we will get all records of the employee with a particular id
        response = self.dynamodb.Table("employeedetails1").scan(FilterExpression=employeeid_filterexpression)
        items=response['Items']
        
        #we need the latest added record under a particular employee id in order to populate.
        #For that we have to sort the record based on their time of addition in descending order and fetch the first record among them
        sorted_items=sorted(items,key=lambda x:x['Time of Adding'],reverse=True)
        return sorted_items[0]
       