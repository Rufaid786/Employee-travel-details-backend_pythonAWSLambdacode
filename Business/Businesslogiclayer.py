from Data.Dataaccesslayer import DataLayer
from Exceptions.Exceptionhandler import Exception
from boto3.dynamodb.conditions import Attr

#creating an object of DataLayer in order to interact with data accesslayer
datalayer_object = DataLayer()

#creating an object of exceptionhandler in order to handle our exceptions
exception=Exception()


class BusinessLayer:

    def add_employee(self,employee):
        # insert the user into the DynamoDB table using the data access layer
        datalayer_object.put_employee(employee)
        
    def get_individualemployee(self,parameter):
        # retrieve a user from the DynamoDB table by its primary key using the data access layer
        try:
            employee = datalayer_object.get_individualemployee(parameter['id'])
            return employee
        except:
            error=exception.getemployee_exception(parameter['id'])
            return error
            
    def getall_employees(self):
            return datalayer_object.getallemployees()
        
            
            
    def getusers_basedon_date(self,dateparameter):
        #dateparameter consists of both starting and ending date for filtering operation.
        #Here we extract both these dates and store it in 2 variables for filtering operation
        starting_date=dateparameter['startdate']
        ending_date=dateparameter['enddate']
        #expression used for filtering
        filtering_expression=Attr('Date from').between(starting_date,ending_date)
        return datalayer_object.filterdatas_basedondate(filtering_expression)
        
        
    def deleteEmployee(self,parameter):
        #First we will check whether the booking id is there in the table
        #if the bookingid is there in table we will get Item attribute in response
        response=datalayer_object.findanEmployee(parameter['id'])
        if 'Item' in response:
            response_delete=datalayer_object.delete_employee(parameter['id'])
            return response_delete
        else:
            error=exception.getemployee_exception(parameter['id'])
            return error
                
                
    def pmologindetails(self,login_details):
        #first we will extract email and password from login_details parameter and assign it two variables
        #Then we create an expression to check with email and password existing in the table
        email=login_details['email']
        password=login_details['password']
        expression=Attr('Email').eq(email) & Attr('Password').eq(password)
        return datalayer_object.logindetails_validation(expression)    
            
        
    def getEmployee_by_empid(self,parameter):
        #This method is for finding employees based on their employeeid.
        #An exception is thrown if the employee id is not in the table
        try:
            employee_id=parameter['empid']
            expression=Attr('Emp ID').eq(employee_id)
            employee = datalayer_object.getEmployeedetails_byempid(expression)
            return employee
        except:
            error=exception.getemployee_exception(parameter['empid'])
            return error
        
        