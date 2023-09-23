# Drug Prescription Home Assignment

## Assumptions:

Each medicine is has a unique name and relates to one or multiple codes.
In the interaction section when closing the prescription - each group of codes is validated against the interaction drugs api.

For example: 

ADVIL (Oral Liquid) has 2 RXCUIS codes: "731531", "206878"
https://clinicaltables.nlm.nih.gov/api/rxterms/v3/search?terms=ADVIL%20(Oral%20Liquid)&ef=RXCUIS

Simvastatin (Oral Liquid) has 2 RXCUIS codes as well: "1790679", "1944264"
https://clinicaltables.nlm.nih.gov/api/rxterms/v3/search?terms=Simvastatin%20(Oral%20Liquid)&ef=RXCUIS

The close prescription route will check the product of the code lists as follows:
 "731531" with "1790679"
 "206878" with "1790679"
 "731531" with "1944264"
 "206878" with "1944264"


## Running Instructions:
Make sure docker (Docker version 23.0.5) and docker compose are installed on your machine and that docker deamon is running. <br>
This app is created with docker-compose which builds the Dockerfile inside prescription_app directory.
<br>
Go the root folder and run: 
```
make
```
You can see the backend app logs by running:
<br>
```
docker logs -f prescription-app
```

The drug prescription app is running on port 3001 and the available routes are as follows:

### Health Check 
GET http://localhost:3001<br>
response: "Alive!"

### Open Prescription:
example: POST http://localhost:3001/open_prescription/1 <br>
response: 
```json
{
    "prescription_id": "735d9da3-d445-40e2-b227-936c954a04ad"
}
```

### Add Medication:
example: POST http://localhost:3001/add_medication/735d9da3-d445-40e2-b227-936c954a04ad<br>
payload: 
```json
{
    "name":"ADVIL (Oral Liquid)",
    "dosage":20,
    "frequency":"twice a day"
}
```
<br>
response:

```json
{
    "message": "ADVIL (Oral Liquid)"
}
```

### Close Prescription: (Success)
example: POST http://localhost:3001/close_prescription/735d9da3-d445-40e2-b227-936c954a04ad<br>
response:
```json
{
    "message": "Prescription closed successfully!"
}
```
### Close Prescription: (Failure - Warnings)
if you add this medications together (Making two different POST requests to add_medication route):<br>
```json
{
    "name":"Simvastatin (Oral Liquid)",
    "dosage":20,
    "frequency":"twice a day"
}
```
```json
{
    "name":"ADVIL (Oral Liquid)",
    "dosage":20,
    "frequency":"twice a day"
}
```
<br><br>
When you will try to close the prescription you will get the following response:
<br><br>
example: POST http://localhost:3001/close_prescription/4ef39ad1-0db9-4f1c-870d-3428791dc3ee<br>
response:<br>
```json
{
    "warnings": [
        {
            "codes": [
                "731531",
                "1790679"
            ],
            "warning": [
                "Drug1 (rxcui = 1790679, name = simvastatin 4 MG/ML Oral Suspension, tty = SCD). Drug2 (rxcui = 731531, name = ibuprofen 40 MG/ML Oral Suspension [Advil], tty = SBD). Drug1 is resolved to simvastatin, Drug2 is resolved to ibuprofen and interaction asserted in DrugBank between Simvastatin and Ibuprofen."
            ]
        },
        {
            "codes": [
                "731531",
                "1944264"
            ],
            "warning": [
                "Drug1 (rxcui = 1944264, name = simvastatin 8 MG/ML Oral Suspension, tty = SCD). Drug2 (rxcui = 731531, name = ibuprofen 40 MG/ML Oral Suspension [Advil], tty = SBD). Drug1 is resolved to simvastatin, Drug2 is resolved to ibuprofen and interaction asserted in DrugBank between Simvastatin and Ibuprofen."
            ]
        },
        {
            "codes": [
                "206878",
                "1790679"
            ],
            "warning": [
                "Drug1 (rxcui = 1790679, name = simvastatin 4 MG/ML Oral Suspension, tty = SCD). Drug2 (rxcui = 206878, name = ibuprofen 20 MG/ML Oral Suspension [Advil], tty = SBD). Drug1 is resolved to simvastatin, Drug2 is resolved to ibuprofen and interaction asserted in DrugBank between Simvastatin and Ibuprofen."
            ]
        },
        {
            "codes": [
                "206878",
                "1944264"
            ],
            "warning": [
                "Drug1 (rxcui = 1944264, name = simvastatin 8 MG/ML Oral Suspension, tty = SCD). Drug2 (rxcui = 206878, name = ibuprofen 20 MG/ML Oral Suspension [Advil], tty = SBD). Drug1 is resolved to simvastatin, Drug2 is resolved to ibuprofen and interaction asserted in DrugBank between Simvastatin and Ibuprofen."
            ]
        }
    ]
}
```


### Tests
Tests are implemented with Pytest. Can be run locally with Pycharm.