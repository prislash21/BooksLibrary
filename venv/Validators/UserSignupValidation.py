from kanpai import Kanpai
schema=Kanpai.Object({
        "userName":Kanpai.String().max(30).trim().required("username required"),
         "email": Kanpai.Email().required("email required"),
         "password": Kanpai.String().max(5).trim().required("pass required"),
        "phone_number": Kanpai.String()

})

