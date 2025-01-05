import types

def changeReference(command, old, new, deep = False):
    """Copys command function/method and changes all references
    from old object instance to new object instance"""

    if type(old) is not type(new):
        print("The given instanzes are not of the same Type!")
        print("old:", type(old))
        print("new:", type(new))
        return command

    def changeFunction():
        def createCell(ref):
            return (lambda: ref).__closure__[0]

        if not command.__closure__:
            print("__closure__ of '"+ command.__name__ +"' is empty")
            return command
        newCells = []
        for cell in command.__closure__:
            #print(type(cell.cell_contents))
            if cell.cell_contents is old:
                newCells.append(createCell(new))
            else:
                if isinstance(cell.cell_contents, types.FunctionType) and deep:
                    func = changeReference(cell.cell_contents, old, new, deep)
                    newCells.append(createCell(func))
                else:
                    newCells.append(cell)
        newClosure = tuple(newCells)
        return types.FunctionType(command.__code__, command.__globals__, command.__name__,
        command.__defaults__, newClosure)

    def changeMethod():
        def searchAttributes(instance, command, processed=None):
            if processed == None:
                processed = []
            if instance in processed:
                return
            else:
                processed.append(instance)
            #print(type(instance))
            try:
                attributes = vars(instance)
            except:
                return

            for a in attributes:
                if command.__self__ is attributes[a]:
                    return [a]
                result = searchAttributes(attributes[a], command, processed)
                if result != None:
                    result.append(a)
                    return result

        result = searchAttributes(old, command)
        if result == None:
            print("Method '" + command.__name__ + "' not found in '" + str(old) + "'")
            return command
        handle = new
        for obj in reversed(result):
            handle = getattr(handle, obj)
        return getattr(handle, command.__name__)


    if isinstance(command, types.FunctionType):
        return changeFunction()
    elif isinstance(command, types.MethodType) or (isinstance(command, types.BuiltinFunctionType) and isinstance(command, types.BuiltinMethodType)):
        return changeMethod()
    else:
        print("WARNING: Reference change functionality for '" + str(type(command)) +"' not implemented. Unchanged command used instead.")
        return command

def demo():
    print("Hello World")

if __name__ == "__main__":
    demo()