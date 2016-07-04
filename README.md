## Installation 
``` pip install vtjp ```

### CLI usage
```
usage: vtjp [-h] key secret {location,arrivalboard,departureboard,trip} ...

Västtrafik journy planner (vtjp)

positional arguments:
  key
  secret
  {location,arrivalboard,departureboard,trip}
                        service

optional arguments:
  -h, --help            show this help message and exit

```



## API credentials
The new API uses OAuth2 as authorization and in order to acquire CONSUMER_KEY and CONSUMER_SECRET from the API, one needs to subscribe to it. Please refer to [Västtrafik](https://labs.vasttrafik.se) in to get your API credentials. When they are acquired, update ```credentials.txt``` and the wrapper will work.


This software is a fork of https://github.com/axelniklasson/vasttrafik-api-wrapper
