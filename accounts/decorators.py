
def roles(response):
    def decorator(func="x"):
        if func == "x":
            return response({"Error":"Yea"})
        return func
    return decorator
