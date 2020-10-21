__author__ = 'Meir Davis'

import json
import re
import requests
from datetime import datetime


parentEmail = "your@email.com"

proxies = {
  "http": "",
  #"https": "127.0.0.1:8888",
}

initialUrl = 'https://govforms.gov.il/mw/forms/ChildHealthDeclaration@molsa.gov.il'
declarationUrl = 'https://govforms.gov.il/MW/Process/Data/'

#Go to initial page to get issued a request ID
resp = requests.get(url=initialUrl,  proxies=proxies, verify=False)
pageText = resp.text
searchResult = re.search('requestID..\"(.{36})', pageText)
requestId = searchResult.group(1)
print(requestId)

now = datetime.now()
date_time = now.strftime("%d/%m/%Y")
print("date and time:",date_time)

healthDeclarationRequest = '{"requestID":"111","processID":null,"formData":{' \
                           '"declarationProperties":{"childInformation":{"idNum":"","lastName":"",' \
                           '"firstName":""},"parentInformation":{"idNum":"","lastName":"",' \
                           '"firstName":""},"childBirthDate":"","daycareManager":"","dayCareCity":{' \
                           '"dataCode":"","dataText":""},"dayCareName":{"dataCode":"","dataText":"שם ' \
                           'מסגרת: , סמל מעון: , "},"parentMobile":"054-00000000",' \
                           '"parentEmail":"blank@gmail.com","parentFirstDeclaration":true,' \
                           '"parentSecondDeclaration":true,"parentDeclaration3":true,"declarationDate":"18/10/2020",' \
                           '"name":"declarationProperties","state":"completed","next":"","prev":"","isClosed":true},' \
                           '"containersViewModel":{"showPrintButton":false,' \
                           '"currentContainerName":"declarationProperties","validatedStatus":true},' \
                           '"formInformation":{"isFormSent":false,"loadingDate":"19/10/2020","firstLoadingDate":"",' \
                           '"isMobile":false,"language":"hebrew"}},"language":"he","attachments":[]} '

healthDeclarationJson = json.loads(healthDeclarationRequest)
healthDeclarationJson["requestID"] = requestId
healthDeclarationJson["formData"]["declarationProperties"]["declarationDate"] = date_time
healthDeclarationJson["formData"]["declarationProperties"]["parentEmail"] = parentEmail

print(healthDeclarationJson)

headers = {'content-type': 'application/json', 'Accept': 'application/json, text/javascript, */*; q=0.01'}

resp = requests.post(url=declarationUrl,  proxies=proxies, headers=headers,verify=False, data=json.dumps(healthDeclarationJson, ensure_ascii=False).encode("utf-8"))
pageText = resp.text
print(pageText)
