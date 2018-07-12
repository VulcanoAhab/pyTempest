def iterModules(baseObj, dotString):
    """
    """
    obj=None
    dotList=dotString.split(".")
    if not dotList:
        raise Exception("[-] Empty dotString")
    print(dotList)
    obj=getattr(baseObj,dotList[0])
    for objName in  dotList[1:]:
        obj=getattr(obj, objName)
    return obj
