#!/usr/bin/env python
from systemd import journal
import re
import pymongo
from pymongo import MongoClient
import json
import os
import subprocess
import requests
import time
from requests_futures.sessions import FuturesSession

db = MongoClient("mongodb+srv://<USERNAME>:<PASSWORD>@cluster0-2etvy.gcp.mongodb.net/GaiaBotData")
client = db.GaiaBotData
collection = client.ValAddrID

KEY="695435732:AAEAIO3cJMy85jwF7pUtUKXCo9-BX5vAF-w"
TIME="10"
URL="https://api.telegram.org/bot" + KEY + "/sendMessage"

j = journal.Reader()
j.this_boot()
j.seek_tail()
# Important! - Discard old journal entries
j.get_previous()
j.log_level(journal.LOG_INFO)
j.add_match(_SYSTEMD_UNIT="forboled.service")

chatidset = set()
start = time.time()

# if no keep track table, add a row to keep track which record has been sent
if (not "keeper" in db["GaiaBotData"].collection_names()):
    mykeeper = client["keeper"]
    newrecord = {"_id": 1, "last": 2}
    mykeeper.insert_one(newrecord)
    startrow = 2

# if no records table, create a new one
if (not "Records" in db["GaiaBotData"].collection_names()):
    myrecords = client["Records"]
    firstrecord = {"_id": 1, "content": "welcome"}
    myrecords.insert_one(firstrecord)

    # if keeper exist, update last col
    if ("keeper" in db["GaiaBotData"].collection_names()):
        newvalue = {"$set": {"last": 2}}
        client.keeper.update({"_id": 1}, newvalue, upsert = False)
    startrow = 2

# use time stamp to keep counting the running time

try:
  while True:
        for entry in j:
            # match Absent validator
            matchAbsent = re.search(r'/.*Absent validator ([0-9A-F]{40}) at height ([0-9]{1,}).*/' , str(entry))
            # match how many shares and tokens reduced
            matchReduced = re.search(r'/.*Validator ([0-9A-F]{40}) slashed by slashFactor ([0-9]{1,}\/[0-9]{1,}), burned ([0-9]{1,}\/[0-9]{1,}) tokens.*/', str(entry))
            # match revoke
            matchRevoke = re.search(r'/.*Validator ([0-9A-F]{40}) revoked.*/', str(entry))

            # get the message that will be send out
            msg = entry["MESSAGE"]

            if (matchAbsent):
                # get valaddr
                height = matchAbsent.group(2)
                id = client.Records.count() + 1
                # store valaddr and content into db
                # stringjson = '{"ValAddr": \"' + matchAbsent.group(1) + '\",height: ' + height + '}'
                stringjson = '{"_id": ' + str(id) + ', "ValAddr\": "' + matchAbsent.group(1) + '\", "content": "' + msg + '\", "type": "absent"}'

            elif (matchReduced):
                id = client.Records.count() + 1
#               stringjson = '{"ValAddr": \"' + matchReduced.group(1) + '\",height: ' + height + ',fraction: \"' + matchReduced.group(2) + '\",removed: \"' + matchReduced.group(3) + '\",burned: ' + matchedReduced.group(4) + '}'
                stringjson = '{"_id": ' + str(id) + ', "ValAddr\": "' + matchReduced.group(1) + '\", "content": "' + msg + '\", "type": "slashed"}'

            elif (matchRevoke):
                id = client.Records.count() + 1
#               stringjson = '{"ValAddr": \"' + matchRevoke.group(1) + '\", height:' + height + '}'
                stringjson = '{"_id": ' + str(id) + ', "ValAddr\": "' + matchRevoke.group(1) + '\", "content": "' + msg + '\", "type": "revoked"}'

            # store that record into db Records
            if (matchAbsent or matchReduced or matchRevoke):
                data = json.loads(stringjson)
                client.Records.insert_one(data)

        end = time.time()
        # send msg every 15 seconds (from keeper.last to current record_id)
        if (end - start > 15):
            # get the last height in collection keeper
            startrow = client.keeper.find_one({"_id": 1}).get("last")
            print("startrow: " + str(startrow) + '\n')

            # get the valAddr from that record
            # get the message that will be send out (use for loop)
            # loop from last height to latest record
            for row in range(startrow, client.Records.count()+1):
                # get the content of that record id
                queryjson = '{"_id": ' + str(row) + '}'
                query = json.loads(queryjson)
                try:
                    data = client.Records.find_one(query)
                    msg = data.get("content")
                    valAddr = data.get("ValAddr")
                    msgtype = data.get("type")
                    print("msgtype: "+msgtype)
                except:
                    break

                # check if the validator is exist in the db.
                # query the chat ID by validator
                stringjson = '{"ValAddr": \"' + valAddr + '\"}'
                for record in collection.find(json.loads(stringjson)):
                    chatid = str(record.get("chatID"))
                    mute = record.get(msgtype)
                    print(mute)
                    if (mute == False):
                        chatidset.add(chatid)
                chatids = tuple(chatidset)
                print(chatids)

                # if there are chatids, send message by API
                session = FuturesSession()
                for id in chatids:
                    session.get(URL + "?chat_id=" + id + "&text=" + msg)
                chatidset = set()

            startrow = client.Records.count()+1
            newvalue = '{"$set": {"last": ' + str(startrow) + '}}'
            try:
                client.keeper.update({"_id": 1}, json.loads(newvalue), upsert = False)
            except:
                print("bad update")
                break
            start = time.time()



except KeyboardInterrupt:
    db.close()
    print("database closed")

