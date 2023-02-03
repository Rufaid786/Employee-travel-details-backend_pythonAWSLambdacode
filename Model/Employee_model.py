class Employee:
    def __init__(self,*employeevalues):
        self.id=employeevalues[0]
        self.account=employeevalues[1]
        self.project=employeevalues[2]
        self.empid=employeevalues[3]
        self.empname=employeevalues[4]
        self.purposeoftravel=employeevalues[5]
        self.travelfrom=employeevalues[6]
        self.travelto=employeevalues[7]
        self.datefrom=employeevalues[8]
        self.dateto=employeevalues[9]
        self.currency=employeevalues[10]
        self.flight=employeevalues[11]
        self.hotac=employeevalues[12]
        self.perdiem=employeevalues[13]
        self.othercost=employeevalues[14]
        self.totalcost=employeevalues[15]
        self.commentsifany=employeevalues[16]
        self.status=employeevalues[17]
        self.timeofadding=employeevalues[18]
    def __dict__(self):
        return{'id':self.id,'Account': self.account,'Project/Contract': self.project,'Emp ID': self.empid,'Emp Name': self.empname,'Purpose of Travel': self.purposeoftravel,'Travel from': self.travelfrom,'Travel to':self.travelto,'Date from':self.datefrom,'Date To':self.dateto,'Currency':self.currency,'Flight':self.flight,'Hotac':self.hotac,'Perdiem':self.perdiem,'Other cost':self.othercost,'Total Cost':self.totalcost,'Comments if Any':self.commentsifany,'Status':self.status,'Time of Adding':self.timeofadding}

#id,account,project,empid,empname,purposeoftravel,travelfrom,travelto,datefrom,dateto,flight,hotac,perdiem,othercost,totalcost,commentsifany,status