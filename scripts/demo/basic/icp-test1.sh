#!/bin/bash

#
# vLEI-server -p 7723 -s schema/acdc -c samples/acdc -o samples/oobis
# kli witness demo
# kli agent demo --config-file demo-witness-oobis-schema
#

set -e

wan=BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha
wil=BLskRTInXnMxWaGqcpSyMgo0nYbalW99cGZESrz3zapM
wes=BIKKuvBwpmDVA4Ds-EpL5bt9OqPzWPja2LigFYZN2YfX
wits="\"${wan}\",\"${wil}\",\"${wes}\""

toad=3

passcode=0000-00000-00000-00000-0000

agent5623=EI_o5FuHDa6F9iM4ZkxiNHqZcU6uHwj0tUjof9NsE_5u
agent5723=EK1N4IgaDirnoCOGnLMsoIzP1mSclmmaXzUu1AdfzKCG

group1=ENR6Mra4QWZ5LhEE5EaQ9JM0YZ_GNcHOdjKRnPRbh18O

sith="[\"1/2\",\"1/2\"]"

function wait_status_ok { 
    retries=10
    while [ $((retries--)) -gt 0 ]; do
        curl -s -f -m 2 $1 > /dev/null && return 0
        sleep 0.5
    done
    return 1
}

function wait_receipts { 
    retries=5
    while [ $((retries--)) -gt 0 ]; do
        response=$(curl -s -f -m 2 $1) || return 1
        receipts=$(echo "$response" | jq -r .receipts)
        if [ $receipts != "null" ]; then
            if [ $receipts -ge $2 ]; then return 0; fi
        fi
        sleep 0.5
    done
    return 1
}

function wait_notification { 
    retries=10
    while [ $((retries--)) -gt 0 ]; do
        response=$(curl -s -f -m 2 $1) || return 1
        r=$(echo "$response" | jq -r '.[-1].a.r')
        if [ $r = "$2" ]; then 
            i=$(echo "$response" | jq -r '.[-1].i')
            curl -s -f -m 2 -X DELETE "$1/$i" > /dev/null
            return 0
        fi
        sleep 0.5
    done
    return 1
}

# boot
curl -s -X POST "http://localhost:5623/boot" -H "accept: */*" -H "Content-Type: application/json" -d "{\"name\":\"agent-5623\",\"passcode\":\"${passcode}\",\"salt\":\"0ACmJXnkY9UTam2hA_wOjvRa\"}" | jq
curl -s -X POST "http://localhost:5723/boot" -H "accept: */*" -H "Content-Type: application/json" -d "{\"name\":\"agent-5723\",\"passcode\":\"${passcode}\", \"salt\":\"0ADaR9d4jdS9hupegNbqxWWm\"}" | jq

# unlock
curl -s -X PUT "http://localhost:5623/boot" -H "accept: */*" -H "Content-Type: application/json" -d "{\"name\":\"agent-5623\",\"passcode\":\"${passcode}\"}" | jq
wait_status_ok "http://localhost:5623/ids"

# unlock
curl -s -X PUT "http://localhost:5723/boot" -H "accept: */*" -H "Content-Type: application/json" -d "{\"name\":\"agent-5723\",\"passcode\":\"${passcode}\"}" | jq
wait_status_ok "http://localhost:5723/ids"

# agent-5623 
curl -s -X POST "http://localhost:5623/ids/agent-5623" -H "accept: */*" -H "Content-Type: application/json" -d "{\"transferable\":true,\"wits\":[${wits}],\"toad\":${toad},\"icount\":1,\"ncount\":1,\"isith\":1,\"nsith\":1}" | jq
wait_receipts "http://localhost:5623/ids/agent-5623" $toad
wait_status_ok "http://127.0.0.1:5642/oobi/${agent5623}/witness/${wan}"

# agent-5723 
curl -s -X POST "http://localhost:5723/ids/agent-5723" -H "accept: */*" -H "Content-Type: application/json" -d "{\"transferable\":true,\"wits\":[${wits}],\"toad\":${toad},\"icount\":1,\"ncount\":1,\"isith\":1,\"nsith\":1}" | jq
wait_receipts "http://localhost:5723/ids/agent-5723" $toad
wait_status_ok "http://127.0.0.1:5642/oobi/${agent5723}/witness/${wan}"

#sleep 0.5

# oobi
curl -s -X POST "http://localhost:5623/oobi" -H "accept: */*" -H "Content-Type: application/json" -d "{\"oobialias\": \"agent-5723\", \"url\":\"http://127.0.0.1:5642/oobi/${agent5723}/witness/${wan}\"}" | jq
wait_status_ok "http://localhost:5623/contacts/${agent5723}"

# oobi
curl -s -X POST "http://localhost:5723/oobi" -H "accept: */*" -H "Content-Type: application/json" -d "{\"oobialias\": \"agent-5623\", \"url\":\"http://127.0.0.1:5642/oobi/${agent5623}/witness/${wan}\"}" | jq
wait_status_ok "http://localhost:5723/contacts/${agent5623}"

# group1
curl -s -X POST "http://localhost:5623/groups/group1/icp" -H "accept: */*" -H "Content-Type: application/json" -d "{\"aids\":[\"${agent5623}\",\"${agent5723}\"], \"transferable\":true,\"wits\":[${wits}],\"toad\":${toad}, \"isith\":${sith},\"nsith\":${sith}}" | jq

# group1
wait_notification "http://localhost:5723/notifications" "/multisig/icp/init"
curl -s -X PUT "http://localhost:5723/groups/group1/icp" -H "accept: */*" -H "Content-Type: application/json" -d "{\"aids\":[\"${agent5623}\",\"${agent5723}\"], \"transferable\":true,\"wits\":[${wits}],\"toad\":${toad}, \"isith\":${sith},\"nsith\":${sith}}" | jq

# group1
wait_notification "http://localhost:5623/notifications" "/multisig/icp/complete"
wait_notification "http://localhost:5723/notifications" "/multisig/icp/complete"

# group1
wait_receipts "http://localhost:5623/ids/group1" $toad
wait_receipts "http://localhost:5723/ids/group1" $toad
