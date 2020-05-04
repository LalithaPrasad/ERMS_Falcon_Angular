import falcon, json
from ERMS_Falcon_API.dbconfig import session
from ERMS_Falcon_API.models import Admin_model as Admin
from ERMS_Falcon_API.models import Emp_model as Employee

def verify_token(req,resp,resource,params):
    admin=session.query(Admin).get(1)
    token=req.get_header("token")
    if not (admin and  token==admin.token and admin.validate_token()):
        msg={"message":"InvalidToken"}
        resp.body=json.dumps(msg)
        resp.status=falcon.HTTP_OK

class Emp_class(object):

    @falcon.before(verify_token)
    def on_get(self,req,resp):
        emps=session.query(Employee).all()
        if emps:
            result=[]
            att_list=["id","name","age","ed","role"]
            for emp in emps:
                result.append(dict(zip(att_list,
                    [emp.id,emp.name,emp.age,emp.ed,emp.role])))
            resp.body=json.dumps(result)
            resp.status=falcon.HTTP_OK
        else:
            msg={"message":"EmployeeDBEmpty"}
            resp.body=json.dumps(msg)
            resp.status=falcon.HTTP_OK

    @falcon.before(verify_token)
    def on_post(self,req,resp):
        data=req.media
        if not data:
            msg={"message":"NoData"}
            resp.body=json.dumps(msg)
            resp.status=falcon.HTTP_OK
        else:
            n=data["name"]
            a=data["age"]
            e=data["ed"]
            r=data["role"]
            emp=Employee(name=n,age=a,ed=e,role=r)
            session.add(emp)
            session.commit()
            msg={"message":"EmployeeAdded"}
            resp.body=json.dumps(msg)
            resp.status=falcon.HTTP_OK


    @falcon.before(verify_token)
    def on_put(self,req,resp):
        data=req.media
        if not data:
            msg={"message":"NoData"}
            resp.body=json.dumps(msg)
            resp.status=falcon.HTTP_OK
        else:
            emp=session.query(Employee).get(int(data["id"]))
            if "ed" in data: emp.ed=data["ed"]
            if "role" in data: emp.role=data["role"]
            session.commit()
            msg={"message":"EmployeeUpdated"}
            resp.body=json.dumps(msg)
            resp.status=falcon.HTTP_OK

    @falcon.before(verify_token)
    def on_delete(self,req,resp):
        data=req.params
        if not data:
            msg={"message":"NoData"}
            resp.body=json.dumps(msg)
            resp.status=falcon.HTTP_OK
        else:
            emp=session.query(Employee).get(int(data["id"]))
            session.delete(emp)
            session.commit()
            msg={"message":"EmployeeDeleted"}
            resp.body=json.dumps(msg)
            resp.status=falcon.HTTP_OK
