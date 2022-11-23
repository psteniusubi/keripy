#!/bin/bash
# To run this script you need to run the following 2 commands in separate terminals:
#   > kli agent demo --config-file demo-witness-oobis-schema
#   > kli witness demo
# and from the vLEI repo run:
#   > vLEI-server -s ./schema/acdc -c ./samples/acdc/ -o ./samples/oobis/

# curl -s http://localhost:5623/notifications | jq
# curl -s http://localhost:5723/notifications | jq

wan=BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha
wil=BLskRTInXnMxWaGqcpSyMgo0nYbalW99cGZESrz3zapM
wes=BIKKuvBwpmDVA4Ds-EpL5bt9OqPzWPja2LigFYZN2YfX
wits="\"${wan}\",\"${wil}\",\"${wes}\""
schema=EBfdlu8R27Fbx-ehrqwImnK-8Cm79sqbAQ4MmvEAYqao

issuer=EKxICWTx5Ph4EKq5xie2znZf7amggUn4Sd-2-46MIQTg
holder=EH2XI0_WVqxqrxsUUUmDmhMO97HJ4Y6GzmoQS7UBGtUV

# DoB26Fj4x9LboAFWJra17O
curl -s -X POST "http://localhost:5623/boot" -H "accept: */*" -H "Content-Type: application/json" -d "{\"name\":\"issuer\",\"passcode\":\"DoB2-6Fj4x-9Lbo-AFWJr-a17O\",\"salt\":\"0ACDEyMzQ1Njc4OWxtbm9aBc\"}" | jq
curl -s -X POST "http://localhost:5723/boot" -H "accept: */*" -H "Content-Type: application/json" -d "{\"name\":\"holder\",\"passcode\":\"DoB2-6Fj4x-9Lbo-AFWJr-a17O\",\"salt\":\"0ACDEyMzQ1Njc4OWxtbm9abc\"}" | jq
sleep 3

curl -s -X PUT "http://localhost:5623/boot" -H "accept: */*" -H "Content-Type: application/json" -d "{\"name\":\"issuer\",\"passcode\":\"DoB2-6Fj4x-9Lbo-AFWJr-a17O\"}" | jq
curl -s -X PUT "http://localhost:5723/boot" -H "accept: */*" -H "Content-Type: application/json" -d "{\"name\":\"holder\",\"passcode\":\"DoB2-6Fj4x-9Lbo-AFWJr-a17O\"}" | jq
sleep 3

curl -s -X POST "http://localhost:5623/ids/issuer" -H "accept: */*" -H "Content-Type: application/json" -d "{\"transferable\":true,\"wits\":[${wits}],\"toad\":3, \"icount\":1,\"ncount\":1,\"isith\":1,\"nsith\":1}" | jq
curl -s -X POST "http://localhost:5723/ids/holder" -H "accept: */*" -H "Content-Type: application/json" -d "{\"transferable\":true,\"wits\":[${wits}],\"toad\":3, \"icount\":1,\"ncount\":1,\"isith\":1,\"nsith\":1}" | jq
sleep 3

curl -s -X POST "http://localhost:5623/registries" -H "accept: */*" -H "Content-Type: application/json" -d "{\"alias\":\"issuer\",\"baks\":[],\"estOnly\":false,\"name\":\"vLEI\",\"noBackers\":true,\"toad\":0}" | jq
sleep 3

curl -s -X POST "http://localhost:5623/oobi" -H "accept: */*" -H "Content-Type: application/json" -d "{\"oobialias\": \"holder\", \"url\":\"http://127.0.0.1:5643/oobi/${holder}/witness/${wan}\"}" | jq
curl -s -X POST "http://localhost:5723/oobi" -H "accept: */*" -H "Content-Type: application/json" -d "{\"oobialias\": \"issuer\", \"url\":\"http://127.0.0.1:5644/oobi/${issuer}/witness/${wan}\"}" | jq
sleep 2

curl -s -X POST "http://localhost:5623/credentials/issuer" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"credentialData\":{\"LEI\":\"5493001KJTIIGC8Y1R17\"},\"recipient\":\"${holder}\",\"registry\":\"vLEI\",\"schema\":\"${schema}\"}" | jq

sleep 3
echo "Holders Received Credentials..."
curl -s -X GET "http://localhost:5723/credentials/holder?type=received" -H "accept: application/json" | jq
