import falcon, json, os
from ERMS_Falcon_API.dbconfig import session
from ERMS_Falcon_API.models import Admin_model as Admin

class Admin_class(object):

    def on_post(self,req,resp):
        admin=session.query(Admin).all()
        if admin:
            msg={"message":"AdminExists"}
            resp.body=json.dumps(msg)
            resp.status=falcon.HTTP_OK
        else:
            data=req.media
            if not data:
                msg={"message":"NoData"}
                resp.body=json.dumps(msg)
                resp.status=falcon.HTTP_OK
            else:
                un=data['username']
                admin=Admin(username=un)
                admin.set_password(data['password'])
                session.add(admin)
                session.commit()
                msg={"message":"AdminAdded"}
                resp.body=json.dumps(msg)
                resp.status=falcon.HTTP_OK
