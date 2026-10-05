class SemanticError(BaseException):
    def __init__(self,errormessage:str):
        self.errormessage=errormessage
