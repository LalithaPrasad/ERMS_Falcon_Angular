import falcon
from falcon_cors import CORS
from ERMS_Falcon_API.admin import Admin_class
from ERMS_Falcon_API.token import Token_class
from ERMS_Falcon_API.employee import Emp_class

cors=CORS(allow_all_origins=True,
        allow_all_headers=True,
        allow_all_methods=True)
api=application=falcon.API(middleware=[cors.middleware])
admin_obj=Admin_class()
api.add_route("/admin", admin_obj)
token_obj=Token_class()
api.add_route("/token", token_obj)
emp_obj=Emp_class()
api.add_route("/employee", emp_obj)
