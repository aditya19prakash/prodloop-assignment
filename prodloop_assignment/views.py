from rest_framework.views import APIView
from rest_framework.response import Response
from prodloop_assignment.ai_service import summarize
import datetime
tasks = dict()
task_id = 1

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
        print(summary)
        if summary is not None:
            tasks[task_id-1]["summary"] = summary
        return Response({"Task_id":task_id-1,"Timestamp":datetime.datetime.now()},status=201)
    
    def get(self,request):
        global tasks
        if len(tasks) == 0:
            return Response({"message":"No task assigned"},status=401)
        priority = request.query_params.get("priority")
        status = request.query_params.get("status")
        temp = dict()
        if priority is not None or status is not None:
            for key,val in tasks.items():
                if priority is not None and val["priority"] != priority:
                    continue
                if status is not None and val.get("status") !=status:
                    continue
                temp[key]=val
            return Response(temp,status=200)
        return Response(tasks,status=200)
    
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
        
        tasks[id]["status"] = status.lower()
        return Response({"message":"status is updated"},status=200)
    
    def delete(self,request,id):
        global tasks
        if not id in tasks:
            return Response({"message":f"This Tasks {id} is not available "},status=404)
        tasks.pop(id,None)
        return  Response({"message":"Deleted Successfully"},status=204)
        
               


                 
        


