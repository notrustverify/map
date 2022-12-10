# Nym nodes geo

There's no visual way to know where the gateway in the world, this repo aims to solve this by giving an API where the coordinates are retrieved from the public IP and return the country too


## Endpoints

### Gateways

[https://map.notrustverify.ch/map/gateways](https://map.notrustverify.ch/map/gateways)

```json
{
  "gateways": [
    {
      "country": "CH",
      "created_on": "Fri, 09 Dec 2022 09:46:05 GMT",
      "identityKey": "2BuMSfMW3zpeAjKXyKLhmY4QW1DXurrtSPEJ6CjX3SEh",
      "latitude": 47.3667,
      "longitude": 8.55,
      "updated_on": "Fri, 09 Dec 2022 09:46:05 GMT"
    },
      ...
    ],
    "num_gateways": 55,
    "last_update": "Fri, 09 Dec 2022 09:46:13 GMT"
}
```

### Gateways countries

[https://map.notrustverify.ch/map/gateways/countries](https://map.notrustverify.ch/map/gateways/countries)

### Gateways Organisation

[https://map.notrustverify.ch/map/gateways/organisation](https://map.notrustverify.ch/map/gateways/organisation)

### Gateways AS

[https://map.notrustverify.ch/map/gateways/asn](https://map.notrustverify.ch/map/gateways/asn)
