from rest_framework.views import APIView
from rest_framework.response import Response
from prodloop_assignment.ai_service import summarize
import datetime
import os
import numpy as np
import pandas as pd
tasks = dict()
task_id = 1

from django.conf import settings

file_path = os.path.join(settings.BASE_DIR, "data", "data.csv")

class Tasks(APIView):
    def post(self, request):
        global tasks
        global task_id
        title = request.data.get("title")
        description = request.data.get("description")
        priority = request.data.get("priority")
        if title is None or description is None or priority is None:
            temp = dict()
            if title is None:
                temp["title"] = "Field is missing"
            if description is None:
                temp["description"] = "Field is missing"
            if priority is None:
               temp["priority"] = "Field is missing"
            return Response({"Tasks":temp},status=404)
        
        if not title.strip() or not description.strip():
            return  Response({"",""},status=404)
        
        if not priority.lower() in ["low","medium","high"]:
            return  Response({"priority":"use one of the value in this list [low, medium, high]"},status=400)
        
        tasks[task_id] = {"title":title,"description":description,"priority":priority.lower()}
        task_id+=1
        summary  = summarize(tasks[task_id-1])
        if summary is not None:
            tasks[task_id-1]["summary"] = summary
        df = pd.read_csv(file_path)
        df.loc[len(df)+1]=[task_id,title,description,priority,summary,0]
        df.to_csv(file_path,index=False)
        return Response({"Task_id":task_id-1,"Timestamp":datetime.datetime.now()},status=201)
    
    def get(self,request):
        global tasks
       
        priority = request.query_params.get("priority")
        status = request.query_params.get("status")
        df = pd.read_csv(file_path)
        if len(df) == 0:
            return Response({"message":"No task assigned"},status=401)
        df = pd.read_csv(file_path)
        df = df.astype(object)
        df = df.replace({np.nan: None})
        if df.empty:
              return Response({"message": "No task assigned"}, status=200)

        if priority is not None:
           df = df[df["priority"] == priority]

        if status is not None:
           df = df[df["status"] == status]

        return Response(df.to_dict(orient="records"), status=200)
    
class Tasks_id(APIView):
    def get(self,request,id):
        global tasks
        if not id in tasks:
            return Response({"message":f"This Task {id} is not available "},status=404)
        return Response(tasks[id],status=200)
    

    def put(self,request,id):
        global tasks
        if not id in tasks:
            return Response({"message":f"This Tasks {id} is not available "},status=404)
        status = request.data.get("status")

        if status is None:
            return Response({"status":"Field is missing"},status=404)
        
        if not status.lower() in ["pending","in_progress","completed"]:
            return  Response({"status":"use one of the value in this list [pending, in_progress, completed]"},status=400)
        df = pd.read_csv(file_path)
        df.loc[df["task_id"] == task_id, "status"] = status.lower()
        df.to_csv(file_path,index=False)
        tasks[id]["status"] = status.lower()
        return Response({"message":"status is updated"},status=200)
    
    def delete(self,request,id):
        global tasks
        if not id in tasks:
            return Response({"message":f"This Tasks {id} is not available "},status=404)
        df = pd.read_csv(file_path)

        df = df[df["task_id"] != id]

        df.to_csv(file_path, index=False)
        tasks.pop(id,None)
        return  Response({"message":"Deleted Successfully"},status=204)
        
               


                 
        


