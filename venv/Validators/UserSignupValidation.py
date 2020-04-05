from kanpai import Kanpai
import  Properties.DbConfiguration
schema=Kanpai.Object({
        "firstName":Kanpai.String().max(20).trim().required("First Name required"),
        "lastName":Kanpai.String().max(20).trim().required("Last Name required"),
         "email": Kanpai.Email().required("email required"),
         "password": Kanpai.String().max(20).trim().required("pass required")
})


