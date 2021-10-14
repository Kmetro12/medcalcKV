'''
Created on Oct 8, 2021

@author: Silvermoon
'''
import json

settings_json = json.dumps([
    {
        'type': 'options',
        'title': 'Day/Night Mode',
        'desc': 'change between day and night mode',
        'section': 'medCalcSett',
        'key': 'color',
        'options':['Night_Mode','Day_Mode']
    }])