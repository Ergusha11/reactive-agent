class Item():
    def __init__(self,numItem: int):
        self.numItem = numItem

    def getNumItem(self) -> int:
        return self.numItem
    
    def setNumItem(self,num) -> None:
        self.numItem = num


class crumbItem():
    def __init__(self,numCrumb: int):
        self.numCrumb = numCrumb

    def getNumCrumb(self) -> int:
        return self.numCrumb

    def setNumCrumb(self,num) -> None:
        self.numCrumb = num
