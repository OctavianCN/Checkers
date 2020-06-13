def singleton(singletonClass):
    instances = {}
    def getInstance(*args,**kwargs):
        if singletonClass not in instances:
            instances[singletonClass] = singletonClass(*args,**kwargs)
        return  instances[singletonClass]
    return getInstance