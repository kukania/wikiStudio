from .databaseClass import DatabaseConnector
import json
"""[
	    {
	        "label" : "item1",
	        "children": []
	    },
	    {
	        "label": "item2",
	        "children": [
	            { "label":"subItem"},
	            { "label":"another subItem"},
	            { "label":"last subItem"}
	        ]
	    },
	    {
	        "label": "item3",
	        "children": [
	            {
	            	"label":"Hello",
	            	"link":"naver.com"
	        	},
	            {
	                "label":"Inner List",
	                "children": [
	                    { "label": "innerItem1" },
	                    { "label": "innerItem2" }
	                ]
	            },
	            { "label":"Bye"}
	        ]
	    }
	]"""
class TreeNode:
    def __init__(self):
        self.parent=None
        self.children=[]

def traversal(treeNode):
    resultData=[]
    tempData={};
    tempData["label"]=treeNode.title;
    tempData["children"]=[]
    for child in treeNode.children:
        tempData["children"].extend(traversal(child))
    resultData.append(tempData)
    return resultData

def makeTreeNav(session):
    result=session["treeNav"]["ROW"]
    for i in range(len(result)):
        result[i]["PID"]=result[i]["MID"]=result[i]["CONTENTID"]
    result=recursiveTreeNav(result)
    treeList={}

    for i in range(len(result)):
        tempTreeNode=TreeNode()
        tempTreeNode.title=result[i]["TITLE"]
        treeList[result[i]["CONTENTID"]]=tempTreeNode

    for value in result:
        if value["MID"]-1!=value["PID"]-1:
            treeList[value["PID"]].children.append(treeList[value["MID"]])
            treeList[value["MID"]].parent=treeList[value["PID"]]

    resultData=[]
    for key,value in treeList.items():
        if value.parent==None:
            resultData.extend(traversal(value))
    return json.dumps(resultData)

def recursiveTreeNav(one):
    connector=DatabaseConnector()
    returnArray=one
    param=one
    for i in range(3):
        if len(param)==0: return returnArray

        query = "select CONTENTID,TITLE,PID,MID from tree join content on tree.MID=content.CONTENTID where tree.PID in ("
        for i in range(len(param)):
            query += str(param[i]["CONTENTID"])+","
        query += "-1) and tree.PID != tree.MID and content.ISPAGE=1;"

        res = connector.query_select(query)
        returnArray.extend(res["ROW"])
        param=res["ROW"]

    return returnArray