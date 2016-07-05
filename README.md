## Installation 
``` pip install vtjp ```

### CLI usage
```
usage: vtjp.py [-h] [-k [KEY]] [-s [SECRET]]
               {storecredentials,location,arrivalboard,departureboard,trip}
               ...

Västtrafik journy planner (vtjp)

positional arguments:
  {storecredentials,location,arrivalboard,departureboard,trip}
                        service to call
    storecredentials    Store credentials to configuration file
    location            Get location information, e.g. stops, addresses
    arrivalboard        Get arrival board for stop
    departureboard      Get departure board for stop
    trip                Get trip suggestions

optional arguments:
  -h, --help            show this help message and exit
  -k [KEY], --key [KEY]
                        API key, required argument if credentials not stored
  -s [SECRET], --secret [SECRET]
                        API secret, required argument if credentials not
                        stored

```



## API credentials
The new API uses OAuth2 as authorization and in order to acquire CONSUMER_KEY and CONSUMER_SECRET from the API, one needs to subscribe to it. Please refer to [Västtrafik](https://labs.vasttrafik.se) in to get your API credentials. When they are acquired, update ```credentials.txt``` and the wrapper will work.


This software is a fork of https://github.com/axelniklasson/vasttrafik-api-wrapper
