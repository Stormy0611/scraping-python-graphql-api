import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get('URL')

mutation_query = '''
    mutation CreateAssetAndGetMatches($request: CreateAssetAndGetMatchesRequest) {
        createAssetAndGetMatches(request: $request) {
            createAssetBody {
            queryId
            status {
                cancelledWhen
                createdWhen
                deletedWhen
                expiresWhen
                isCurrentlySendingLiveMatchNotifications
                isLive
                lastModifiedWhen
                owner {
                companyId
                officeId
                userId
                groupId
                sourceApplication
                __typename
                }
                __typename
            }
            duplicateDetected
            __typename
            }
            assetMatchesBody {
            cursorPages {
                prev
                next
                __typename
            }
            matchCounts {
                blocked
                maxViewable
                normal
                preferred
                privateNetwork
                loadBoard
                totalCount
                __typename
            }
            matches {
                matchId
                availability {
                earliestWhen
                latestWhen
                __typename
                }
                brokerDataRemoved
                combinedOfficeId
                comments
                destinationDeadheadMiles {
                method
                miles
                __typename
                }
                howTrackable
                isAssurable
                isBookable
                isFactorable
                isFromPrivateNetwork
                isNegotiable
                isQuickPayable
                loadBoardRateInfo {
                bookable {
                    bookingMethod
                    bookingUrl
                    rate {
                    basis
                    rateUsd
                    __typename
                    }
                    searcher {
                    companyId
                    groupId
                    officeId
                    searcherDotNumber
                    searcherMcNumber
                    userId
                    __typename
                    }
                    __typename
                }
                nonBookable {
                    basis
                    rateUsd
                    __typename
                }
                __typename
                }
                matchingAssetInfo {
                assetType
                capacity {
                    shipment {
                    fullPartial
                    maximumLengthFeet
                    maximumWeightPounds
                    __typename
                    }
                    truck {
                    availableLengthFeet
                    availableWeightPounds
                    fullPartial
                    __typename
                    }
                    __typename
                }
                destination {
                    area {
                    states
                    zones
                    __typename
                    }
                    open
                    place {
                    city
                    county
                    latitude
                    longitude
                    postalCode
                    stateProv
                    __typename
                    }
                    __typename
                }
                equipmentType
                matchingPostingId
                origin {
                    area {
                    states
                    zones
                    __typename
                    }
                    open
                    place {
                    city
                    county
                    latitude
                    longitude
                    postalCode
                    stateProv
                    __typename
                    }
                    __typename
                }
                __typename
                }
                originDeadheadMiles {
                method
                miles
                __typename
                }
                posterInfo {
                carrierHomeState
                city
                companyId
                companyName
                contact {
                    email
                    phone
                    __typename
                }
                credit {
                    asOf
                    creditScore
                    daysToPay
                    __typename
                }
                factoring
                groupId
                hasTiaMembership
                officeId
                preferredContactMethod
                registryLookupId
                preferredBlockedStatus
                state
                userId
                __typename
                }
                postersReferenceId
                postingCancelledWhen
                postingExpiresWhen
                postingId
                privateNetworkRateInfo {
                bookable {
                    bookingMethod
                    bookingUrl
                    rate {
                    basis
                    rateUsd
                    __typename
                    }
                    searcher {
                    companyId
                    groupId
                    officeId
                    searcherDotNumber
                    searcherMcNumber
                    userId
                    __typename
                    }
                    __typename
                }
                nonBookable {
                    basis
                    rateUsd
                    __typename
                }
                __typename
                }
                ranked
                relevanceScore
                servicedWhen
                shipmentId
                status
                systemStatus
                tripLength {
                method
                miles
                __typename
                }
                bids {
                id
                postingId
                rateUsd
                brokerOfficeId
                carrierOfficeId
                status
                type
                createdOn
                legacyOfficeId
                companyPhone
                companyName
                emailAddress
                firstName
                lastName
                isInPrivateNetwork
                __typename
                }
                workList {
                id
                userStatus
                status
                computedStatus
                edited
                __typename
                }
                __typename
            }
            isCurrentlySendingLiveMatchNotifications
            __typename
            }
            __typename
        }
    }
'''

variables = {
    "request": {
        "createAssetRequest": {
            "criteria": {
                "maxDestinationDeadheadMiles": int(os.environ.get('DH_D')),
                "maxOriginDeadheadMiles": int(os.environ.get('DH_O')),
                "maxAgeMinutes": 1440,
                "includeRanked": False,
                "includeTrackableTypes": [
                    "DONT_CARE"
                ],
                "includeOnlyBookable": False,
                "audience": {
                    "includePrivateNetwork": True,
                    "includeLoadBoard": True,
                    "includeExtendedNetwork": True
                },
                "availability": {
                    "earliestWhen": os.environ.get('EARLIEST'),
                    "latestWhen": os.environ.get('LATEST')
                },
                "capacity": {
                    "shipment": {
                        "fullPartial": "BOTH"
                    }
                },
                "lane": {
                    "assetType": "SHIPMENT",
                    "equipment": {
                        "classes": os.environ.get('EQUIPMENTS').split(',')
                    },
                    "destination": {
                        "place": {
                            "city": os.environ.get('DESTINATION'),
                            "stateProv": "NY",
                            "longitude": -74,
                            "latitude": 40.7,
                            "postalCode": "11202"
                        }
                    },
                    "origin": {
                        "place": {
                            "city": os.environ.get('ORIGIN'),
                            "stateProv": "AZ",
                            "longitude": -111.67028,
                            "latitude": 32.75583,
                            "postalCode": "85123"
                        }
                    }
                }
            },
            "delivery": {
                "notify": True
            }
        },
        "assetMatchesParams": {
            "orderBy": "AscAge",
            "limit": 150,
            "excludePostingIds": []
        }
    }
}

headers = {
    'Content-Type': 'application/json',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik16Y3dSa1k1TkRZME5ESTVNekF4TWpnMk5UZzBOa0ZHUlRjMVFqWkNNamxGT1RsR05FVTRNZyJ9.eyJodHRwczovL2RhdC5jb20vY3NiU291cmNlQXBwIjoiZGF0b25lLndlYiIsImh0dHBzOi8vbGVnYWN5LWF1dGguZGF0LmNvbS9jYXBhYmlsaXRpZXMiOiJBQkk0eXpnQVZRYkNBeUFBQUFnQUFBQUM0QUFBQUFBQUFBQUFBUT09IiwiaHR0cHM6Ly9sZWdhY3ktYXV0aC5kYXQuY29tL3Nlc3Npb24iOiJINHNJQUFBQUFBQUFBSTFSd1dxRFFCRDlsV1Y2ckN6dXJycnFxYUVVY2hBS1RTaUZrSU5SYTdjWWxWWGJwaUgvM3JmYUhBczl5TXk0NzcxNU0zT21ZVG9NbE83b1BmL0krVFNhaHErc3pVK1pHVWJ5ZHJSOTRDdkZZNjFFRWlhMDMzdFVVVXE5TFEva1VXRktTb1hRV3F2RW8yNnVaQkw1VWVCUjdTb2ZtUHlhRkwvSjVLS01ZcUZENEJySWRXM2RtYlp1dWhwZFRURkFlbWFwUkFRU3lvTXJpREg4SHc3U0ZhR1VLbFlRblpzR1VlQXJWTGFaZ1J1K0VQbUNja2JMdng0bWpKa0tKQWdhM2hBa3VyZEFQeTZ1V0hhMTViRXN1d2VwN3lrOVk1NlptQ05vSHh4UUFxbENvVUxzNkF2RkJZLy9SbFpIZEJSUzNlSGpSWGQwM2haYWovUEVNVmhIcDJWYUErQ3phWXVxeFlIbzFUbDlNc1ZiYmt0eUhVdUhja09SMENyMDJXYk14NHF0UDA5TUJzbnRCcm1VUHJzSm9qQ21aV3hhZDloQzE3cnR3aTl0WDVCOUk5RWFsN3dhZ2ZiWW0vbUF0bGlDUmVEKzVRZkNzQnJwUkFJQUFBPT0iLCJodHRwczovL2xlZ2FjeS1hdXRoLmRhdC5jb20vdXNlcm9yZyI6IjI2ODE3NTR8fDEyOTYwNjR8MTE3NzczOXw0NjQwMzMiLCJodHRwczovL2RhdC5jb20vcGVybWlzc2lvbnMiOlsiRnJlaWdodDpMb2FkU2VhcmNoZXM6TWFuYWdlIiwiVmlzaWJpbGl0eTpTaGlwbWVudFJlcXVlc3RSZXNwb25zZTpDcmVhdGUiLCJWaXNpYmlsaXR5OkFzc2lnbmVkU2hpcG1lbnRzOlJlYWQiLCJWaXNpYmlsaXR5OlNoaXBtZW50VHJhY2tpbmdSZWNvcmQ6Q3JlYXRlIiwiRnJlaWdodDpQcml2YXRlTmV0d29ya1F1ZXJ5TWF0Y2hlczpSZWFkIiwiRnJlaWdodDpQcml2YXRlTmV0d29ya1F1ZXJ5TG9hZE1hdGNoZXM6UmVhZCJdLCJodHRwczovL2RhdC5jb20vcm9sZXMiOltdLCJodHRwczovL2RhdC5jb20vdXNlcm9yZyI6ImNkZmEzY2Q4LTMyMDUtNDRmOC1hOTQzLWI4M2YzMzExYmRhMnw3MzQ4YzkxZC0xMTUyLTQwYWItYmM4Mi02YmI3MTlkN2ZkNjN8NzM0OGM5MWQtMTE1Mi00MGFiLWJjODItNmJiNzE5ZDdmZDYzfCIsImlzcyI6Imh0dHBzOi8vbG9naW4uZGF0LmNvbS8iLCJzdWIiOiJhdXRoMHw2MDdiMzI3NWY0MGM4ODAwNjgyODYxZjAiLCJhdWQiOlsiaHR0cHM6Ly9wcm9kLWFwaS5kYXQuY29tIiwiaHR0cHM6Ly9kYXQuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY4NTY0NjU4MiwiZXhwIjoxNjg1NjYwOTgyLCJhenAiOiJlOWx6TVhibldOSjBENTBDMmhhYWRvN0RpVzFha3dhQyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwifQ.rDfI1kwxVnHDOSB1uPRHlHbSb5zsJBFgW_GoilaXRVYdBrOgX6NGjVH3wmNfSbmqKmJ4J3SX8Bqw6yYadiH3FPZkhMsALx3fz5_euenESngRy8QIr3VqiQQUUXddbnA5t6Mvdxa-VwKvz7A4AN3niqqZjAcNIn-JmT-p4syyHix6mRQ3CIcEc4lZ_4CHIZSl_hkYEexQNbUS6OSodKs8eJ7cVHuebJaDJ-bUmjoYQ9bBTI2y_aDsH0cpFWPdvPNg0VM_uk3Kmgmrfo0gIiw2_-HKZNDWhFLulEXmpLhas9-2HcVfC5d9J6iDD4v04eImFOP1nRgUNzEOkX-POkx0hg"
}

response = requests.post(url, headers=headers, json={
    'query': mutation_query,
    'variables': variables
})

# file path of the JSON file to be saved
file_path = "result.json"

# open file for writing
with open(file_path, 'w') as f:
    # convert dictionary to JSON format and write to file
    json.dump(response.json(), f)

print("JSON file saved")