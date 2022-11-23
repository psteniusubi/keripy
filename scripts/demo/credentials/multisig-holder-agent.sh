#!/bin/bash

wan=BBilc4-L3tFUnfM_wJr4S4OJanAv_VmF_dJNN6vkf2Ha
wil=BLskRTInXnMxWaGqcpSyMgo0nYbalW99cGZESrz3zapM
wes=BIKKuvBwpmDVA4Ds-EpL5bt9OqPzWPja2LigFYZN2YfX
wits="\"${wan}\",\"${wil}\",\"${wes}\""
schema=EBfdlu8R27Fbx-ehrqwImnK-8Cm79sqbAQ4MmvEAYqao

multisig1=EKYLUMmNPZeEs77Zvclf0bSN5IN-mLfLpx2ySb-HDlk4
multisig2=EJccSRTfXYF6wrUVuenAIHzwcx3hJugeiJsEKmndi5q1
issuer=EKhW9MhMoy4ZzAdw9D5Kvtk7-mn75SSDDv1BdMro1av-
holder=EM1BxzJgtrOl9f66zodu0YQpWcTabhSAiQy9r0xHtV6r

# DoB26Fj4x9LboAFWJra17O
curl -s -X POST "http://localhost:5623/boot" -H "accept: */*" -H "Content-Type: application/json" -d "{\"name\":\"multisig1\",\"passcode\":\"DoB2-6Fj4x-9Lbo-AFWJr-a17O\",\"salt\":\"0ACDEyMzQ1Njc4OWxtbm9aBc\"}" | jq
curl -s -X POST "http://localhost:5723/boot" -H "accept: */*" -H "Content-Type: application/json" -d "{\"name\":\"multisig2\",\"passcode\":\"DoB2-6Fj4x-9Lbo-AFWJr-a17O\", \"salt\":\"0ACDEyMzQ1Njc4OWdoaWpsaw\"}" | jq
curl -s -X POST "http://localhost:5823/boot" -H "accept: */*" -H "Content-Type: application/json" -d "{\"name\":\"issuer\",\"passcode\":\"DoB2-6Fj4x-9Lbo-AFWJr-a17O\",\"salt\":\"0ACDEyMzQ1Njc4OWxtbm9abc\"}" | jq

sleep 3
curl -s -X PUT "http://localhost:5623/boot" -H "accept: */*" -H "Content-Type: application/json" -d "{\"name\":\"multisig1\",\"passcode\":\"DoB2-6Fj4x-9Lbo-AFWJr-a17O\"}" | jq
curl -s -X PUT "http://localhost:5723/boot" -H "accept: */*" -H "Content-Type: application/json" -d "{\"name\":\"multisig2\",\"passcode\":\"DoB2-6Fj4x-9Lbo-AFWJr-a17O\"}" | jq
curl -s -X PUT "http://localhost:5823/boot" -H "accept: */*" -H "Content-Type: application/json" -d "{\"name\":\"issuer\",\"passcode\":\"DoB2-6Fj4x-9Lbo-AFWJr-a17O\"}" | jq

sleep 4
curl -s -X POST "http://localhost:5623/ids/multisig1" -H "accept: */*" -H "Content-Type: application/json" -d "{\"transferable\":true,\"wits\":[${wits}],\"toad\":2,\"icount\":1,\"ncount\":1,\"isith\":1,\"nsith\":1}" | jq
curl -s -X POST "http://localhost:5723/ids/multisig2" -H "accept: */*" -H "Content-Type: application/json" -d "{\"transferable\":true,\"wits\":[${wits}],\"toad\":2,\"icount\":1,\"ncount\":1,\"isith\":1,\"nsith\":1}" | jq
curl -s -X POST "http://localhost:5823/ids/issuer" -H "accept: */*" -H "Content-Type: application/json" -d "{\"transferable\":true,\"wits\":[${wits}],\"toad\":3, \"icount\":1,\"ncount\":1,\"isith\":1,\"nsith\":1}" | jq

sleep 4
curl -s -X POST "http://localhost:5623/oobi" -H "accept: */*" -H "Content-Type: application/json" -d "{\"oobialias\": \"multisig2\", \"url\":\"http://127.0.0.1:5642/oobi/${multisig2}/witness/${wan}\"}" | jq
curl -s -X POST "http://localhost:5723/oobi" -H "accept: */*" -H "Content-Type: application/json" -d "{\"oobialias\": \"multisig1\", \"url\":\"http://127.0.0.1:5642/oobi/${multisig1}/witness/${wan}\"}" | jq
curl -s -X POST "http://localhost:5623/oobi" -H "accept: */*" -H "Content-Type: application/json" -d "{\"oobialias\": \"issuer\", \"url\":\"http://127.0.0.1:5643/oobi/${issuer}/witness/${wan}\"}" | jq
curl -s -X POST "http://localhost:5723/oobi" -H "accept: */*" -H "Content-Type: application/json" -d "{\"oobialias\": \"issuer\", \"url\":\"http://127.0.0.1:5643/oobi/${issuer}/witness/${wan}\"}" | jq

echo "Adding oobis"
echo "--issuer resolving oobis from multisig1 & multisig2"
curl -s -X POST "http://localhost:5823/oobi" -H "accept: */*" -H "Content-Type: application/json" -d "{\"oobialias\": \"multisig2\", \"url\":\"http://127.0.0.1:5642/oobi/${multisig2}/witness/${wan}\"}" | jq
curl -s -X POST "http://localhost:5823/oobi" -H "accept: */*" -H "Content-Type: application/json" -d "{\"oobialias\": \"multisig1\", \"url\":\"http://127.0.0.1:5642/oobi/${multisig1}/witness/${wan}\"}" | jq

#echo "--schema oobis"
#curl -s -X POST "http://localhost:5623/oobi/multisig1" -H "accept: */*" -H "Content-Type: application/json" -d "{\"oobialias\": \"multisig1\", \"url\":\"http://127.0.0.1:7723/oobi/EBfdlu8R27Fbx-ehrqwImnK-8Cm79sqbAQ4MmvEAYqao\"}" | jq
#curl -s -X POST "http://localhost:5723/oobi/multisig2" -H "accept: */*" -H "Content-Type: application/json" -d "{\"oobialias\": \"multisig2\", \"url\":\"http://127.0.0.1:7723/oobi/EBfdlu8R27Fbx-ehrqwImnK-8Cm79sqbAQ4MmvEAYqao\"}" | jq
#curl -s -X POST "http://localhost:5823/oobi/issuer" -H "accept: */*" -H "Content-Type: application/json" -d "{\"oobialias\": \"issuer\", \"url\":\"http://127.0.0.1:7723/oobi/EBfdlu8R27Fbx-ehrqwImnK-8Cm79sqbAQ4MmvEAYqao\"}" | jq
#echo "finished adding oobis"

echo "inception event for multisig holder"
sleep 3
curl -s -X POST "http://localhost:5623/groups/holder/icp" -H "accept: */*" -H "Content-Type: application/json" -d "{\"aids\":[\"${multisig1}\",\"${multisig2}\"], \"transferable\":true,\"wits\":[${wits}],\"toad\":3, \"isith\":2,\"nsith\":2}" | jq
curl -s -X PUT "http://localhost:5723/groups/holder/icp" -H "accept: */*" -H "Content-Type: application/json" -d "{\"aids\":[\"${multisig1}\",\"${multisig2}\"], \"transferable\":true,\"wits\":[${wits}],\"toad\":3, \"isith\":2,\"nsith\":2}" | jq

sleep 3
echo oobi holder to issuer
curl -s -X POST "http://localhost:5823/oobi" -H "accept: */*" -H "Content-Type: application/json" -d "{\"oobialias\": \"holder\", \"url\":\"http://127.0.0.1:5642/oobi/${holder}/witness/${wan}\"}" | jq

echo "post registries"
curl -s -X POST "http://localhost:5823/registries" -H "accept: */*" -H "Content-Type: application/json" -d "{\"alias\":\"issuer\",\"baks\":[],\"estOnly\":false,\"name\":\"vLEI\",\"noBackers\":true,\"toad\":0}" | jq

#curl -s -X POST "http://localhost:5823/registries" -H "accept: */*" -H "Content-Type: application/json" -d "{\"alias\":\"issuer\",\"nonce\":\"AHSNDV3ABI6U8OIgKaj3aky91ZpNL54I5_7-qwtC6q2s\",\"baks\":[],\"estOnly\":false,\"name\":\"vLEI\",\"noBackers\":true,\"toad\":0}" | jq

# sleep 3
# curl -s -X POST "http://localhost:5623/groups/issuer/rot" -H "accept: */*" -H "Content-Type: application/json" -d "{\"adds\":[],\"aids\":[\"EJccSRTfXYF6wrUVuenAIHzwcx3hJugeiJsEKmndi5q1\", \"EKYLUMmNPZeEs77Zvclf0bSN5IN-mLfLpx2ySb-HDlk4\"],\"count\":2,\"cuts\":[],\"data\":[],\"isith\":\"2\",\"toad\":2, \"wits\":[]}" | jq
# curl -s -X PUT "http://localhost:5723/groups/issuer/rot" -H "accept: */*" -H "Content-Type: application/json" -d "{\"adds\":[],\"aids\":[\"EJccSRTfXYF6wrUVuenAIHzwcx3hJugeiJsEKmndi5q1\", \"EKYLUMmNPZeEs77Zvclf0bSN5IN-mLfLpx2ySb-HDlk4\"],\"count\":2,\"cuts\":[],\"data\":[],\"isith\":\"2\",\"toad\":2, \"wits\":[]}" | jq

sleep 3
echo "Issue Credential"
curl -X POST "http://localhost:5823/credentials/issuer" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"credentialData\":{\"LEI\":\"5493001KJTIIGC8Y1R17\"},\"recipient\":\"${holder}\",\"registry\":\"vLEI\",\"schema\":\"${schema}\"}" | jq

sleep 3
echo "Holders Received Credentials..."
curl -s -X GET "http://localhost:5623/credentials/holder?type=received" -H "accept: application/json" | jq
