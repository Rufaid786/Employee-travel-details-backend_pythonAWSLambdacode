import json
from Business.Businesslogiclayer import BusinessLayer
from decimal import * 

#creating an object of business logic layer to interact with it
business_layer = BusinessLayer()

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
        
        
def controller_handler(event, context):
    #event['httpMethod'] is used for detecting whether incoming method is get or post
    if event['httpMethod']=='GET':
        #event['queryStringParameters'] will detect the parameters coming from the api.
        #Here we are storing the parameters inside a variable.
        query_string_parameters=event['queryStringParameters']
    
        #if query_string_parameters is none means we are not passing any parameter through api.
        if query_string_parameters is None:
            response = business_layer.getall_employees()
            return {
                'statusCode': 200,
                'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(response,cls=DecimalEncoder)
            }
            
        #len>1 means we are passing more than one parameters through api.
        #i.e.,here 2 paramters(starting and ending date)in the PMO section is passed for filtering purpose
        elif len(query_string_parameters)>1:
            try:
                response=business_layer.getusers_basedon_date(query_string_parameters)
                return {
                    'statusCode': 200,
                    'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps(response,cls=DecimalEncoder)
                }
            except:
                response=business_layer.pmologindetails(query_string_parameters)
                return {
                    'statusCode': 200,
                    'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                    },
                    'body': response
                }
        
        #Here,len(query_string_parameters)=1.So,first two conditions will not satisfy.
        #The querystringparameter can be the bookingid  which is passed through api for  update operation 
        #or it can be employeeid for getting employeedetails 
        elif len(query_string_parameters)==1:
            try:
                response=business_layer.get_individualemployee(query_string_parameters)
                return {
                    'statusCode': 200,
                    'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps(response,cls=DecimalEncoder)
                }
            except:
                response=business_layer.getEmployee_by_empid(query_string_parameters)
                return {
                    'statusCode': 200,
                    'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps(response,cls=DecimalEncoder)
                }
            
    #For delete oeration.Here parameter is the bookingid and delete operation takes place based on bookingid        
    elif event['httpMethod']=='DELETE':
        query_string_parameters=event['queryStringParameters']
        response=business_layer.deleteEmployee(query_string_parameters)
        return {
            'statusCode': 200,
            'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
            },
            'body': response
        }
        
    else:
        #if httpmethod is not get and delete then we are having the post method for adding an employee
        data=json.loads(event['body'])
        # client=boto3.client("sns")
        # resp=client.publish(TopicArn="arn:aws:sns:ap-south-1:025051377485:employeenotification",Message=json.dumps({"event":"employeenotification","body":"booking id :"+data['id']+" is either updated or added"}))
        action=business_layer.add_employee(data)
        return {
            'statusCode': 200,
            'body': 'successfully Added Employee!',
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        }
    
   

