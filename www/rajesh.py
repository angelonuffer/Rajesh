from mod_python import apache

def handler(req):
    req.content_type = "text/plain"
    req.write("It works!")
    return apache.OK
