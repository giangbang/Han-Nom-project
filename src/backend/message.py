def success(data='Done'):
  return {"success":True, "data":data}
  
def error(e):
  return {"success":False, "data": str(e)}