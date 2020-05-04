import falcon, json, os
from ERMS_Falcon_API.dbconfig import session
from ERMS_Falcon_API.models import Admin_model as Admin


class Token_class(object):

    def __init__(self):
        self.admin=None

    def on_get(self,req,resp):
        data=req.params
        if not data:
            msg={"message":"NoData"}
            resp.body=json.dumps(msg)
            resp.status=falcon.HTTP_OK
        else:
            admin=session.query(Admin).filter_by(username=data["username"]).first()
            if admin and admin.check_password(data['password']):
                token=admin.get_token()
                session.commit()
                self.admin=admin
                msg={"token":token,"message":"ValidUser"}
                resp.body=json.dumps(msg)
                resp.status=falcon.HTTP_OK
            else:
                msg={"message":"InvalidUser"}
                resp.body=json.dumps(msg)
                resp.status=falcon.HTTP_OK

    def on_put(self,req,resp):
        if self.admin!=None:
            self.admin.invalidate_token()
            session.commit()
            self.admin=None
        msg={"message":"LoggedOut"}
        resp.body=json.dumps(msg)
        resp.status=falcon.HTTP_OK
