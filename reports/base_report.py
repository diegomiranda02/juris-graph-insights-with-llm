import pandas as pd
import json

from typing import Dict

class BaseJSONReport():

    def __init__(self, title:str, subtitle:str):
        self.data_dict = {}
        self.keySuffix = 0

        self.addTitleData(title)
        self.addSubtitleData(subtitle)
   
    def addTitleData(self, description: str) -> None:
        self.data_dict["title" + str(self.keySuffix)] = description
        self.keySuffix += 1

    def addSubtitleData(self, description: str) -> None:
        self.data_dict["subtitle" + str(self.keySuffix)] = description
        self.keySuffix += 1

    def addMapData(self, description: str, data: Dict[str, Dict]) -> None:
        self.data_dict["mapDescription" + str(self.keySuffix)] = description
        self.data_dict["mapData" + str(self.keySuffix)] = data
        self.keySuffix += 1

    def addTableData(self, description: str, data: Dict[str, Dict]) -> None:
        self.data_dict["tableDescription" + str(self.keySuffix)] = description
        self.data_dict["tableData" + str(self.keySuffix)] = data
        self.keySuffix += 1
    
    def addBarChartData(self, description: str, data: Dict[str, Dict]) -> None:
        self.data_dict["barchartDescription" + str(self.keySuffix)] = description
        self.data_dict["barchartData" + str(self.keySuffix)] = data
        self.keySuffix += 1

    def generateJSONReport(self) -> Dict:
        json_object = json.dumps(self.data_dict)
        return json_object