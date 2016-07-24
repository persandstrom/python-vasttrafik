## Installation 
``` pip install vtjp ```

## CLI usage
```
usage: vtjp [-h] [-k [KEY]] [-s [SECRET]]
            {store,location,arrival,departure,trip} ...

Västtrafik journy planner (vtjp)

positional arguments:
  {store,location,arrival,departure,trip}
                        service to call
    store               Store credentials to configuration file
    location            Get location information, e.g. stops, addresses
    arrival             Get arrival board for stop
    departure           Get departure board for stop
    trip                Get trip suggestions

optional arguments:
  -h, --help            show this help message and exit
  -k [KEY], --key [KEY]
                        API key, required argument if credentials not stored
  -s [SECRET], --secret [SECRET]
                        API secret, required argument if credentials not
                        stored

```

## Module usage

### Get departures from brunnsparken
```
import vasttrafik

jp = vasttrafik.JournyPlanner(
    key='my_key',
    secret='my_secret')

brunnsparken_id = jp.location_name('Brunnsparken')[0]['id']
print(jp.departureboard(brunnsparken_id))
```

## API credentials
The new API uses OAuth2 as authorization and in order to acquire CONSUMER_KEY and CONSUMER_SECRET from the API, one needs to subscribe to it. Please refer to [Västtrafik](https://labs.vasttrafik.se) in to get your API credentials.


This software is a fork of https://github.com/axelniklasson/vasttrafik-api-wrapper
