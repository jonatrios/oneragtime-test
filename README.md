[![LinkedIn][linkedin-shield]][linkedin-url]


<br />

  <h3 align="center">Django REST API-Test OneRagTime CASH CALLS</h3>

  <p align="center">
    For automtate the proccess of billing!
  </p>
    
<br />
   




<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#assumptions-made">Assumptions Made</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#django-signals">Django Signals</a></li>
    <li><a href="#updating-fess">Updating Fees</a></li>
    <li><a href="#bills-creation">Bills Creation</a></li>
    <li><a href="#shutting-down">Shutting Down</a></li>
    <li><a href="#run-outside-docker">Run Outside Docker</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

RESTFul JSON API that can list, create, update or delete Fees percentages, Investors and its Investments. Base on the new Investmets, different types of bills are generated on the fly, depending on business rules. It also has a ```Swagger and Redoc``` interface integrated, so...enjoy getting and posting!.
<br></br>

### Assumptions Made

The first assumption was that the requirement need to build a REST API. Knowing this, I started to stablish the workflow to make it happend.
1. To have bills to collect, first of all you have to have some Investor to charge
2. Then, they must have one or more Investments
3. In the middle, you have to set some business rules, like `fee percentage` parameter or `yearly fees` calculation functions
4. Now you are enabled to generate the corresponding yearly or membership fees.

Base on the `pay_upfront` flag on the Investment model, we are going to know if that Investor wants to pay only once for the fees of a given Investment. If the flag is <b>false</b> then Yearly fees would be generated base on the date of the Investment. And also, a first membership fee is generated, that if the sum of the investment for the current year goes beyond certain amount, is set to zero.

And for the fees of the following years, the wolkflow asume that a human through a frontend interface must be checking it out, so I made an update mechanism to have all in control, the generation of the remaining individual yearly fees and also the `state` of the grouping bills a.k.a. `cash calls`
<br></br>

### Built With

* Python 3.8
* Django
* DRF
* Docker
* Postgres



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Just only need to have docker and docker-compose set up on your local system
* to check it you could type in shell (Windows Powershell or Linux)

  ```sh
  docker --version; docker-compose --version
  ```

### Installation

1. Clone the repo, go inside oneragtime-test folder

2. Make sure to add `.env` file with your super secret key!
    ```sh
    echo SECRET_KEY=mysupersecretkey > .env
    ```
    (If you want to use the Rest Framework user interface, set DEBUG=1 in .env)

3. Run docker-compose
   ```sh
   docker-compose up --build
   ```
4. For the use of Django Admin site, you need to generate a super user, so open another terminal and run:
    ```sh
    docker-compose run app python /oneragtime_test/src/manage.py createsuperuser
    ```
    (Or use the same terminal if you run the compose in -d mode!)


<!-- USAGE EXAMPLES -->
## Usage
Open the browser on http://localhost:8000/

The first step is to create one or more investor, so go to http://localhost:8000/api/investor/ and using the POST method:

```javascript
    {
        "first_name": "Juan",
        "last_name": "Perez",
        "company_name": "The Juan Perez Company",
        "email": "juan@gmail.com",
        "is_active": true
    }
```
The `is_active` and `company_name` keys are optionals. By default is_active is true and company_name has the value of "No Company".

You can retrieve all entries or a detail view of the Investor info:

* Can test it using cULR command, to get the list of all records for Investor model.
```sh
   curl --request GET 'http://localhost:8000/api/investor/'
   ```
* It also accepts url params. You can ask for an specific entry, like:
```sh
   curl --request GET 'http://localhost:8000/api/investor/1/
   ```

The following, before to create an Investment, is to set a `fee percentage` value. By default, in settings.py file is an example of a fee percentage that will be use to create a new instance if no value were given at creation time.
```javascript
    {
        "description": "Base Percentage",
        "fee_value": "0.015"
    }
```

The next step is to create an Investment based on a Investor, go to http://localhost:8000/api/investment/ and using the POST method:
```javascript
    {
        "investment_amount": "50000",
        "date_of_investment": "2017-05-17",
        "investor": 1,
        "fee_percentage": 1,
        "pay_upfront": true
    }
```
The `pay_upfront` key is optional, by default is <b>false</b>
<br></br>

<!--Dango Signals!!-->
## Django Signals
So now what?...
Well, if the `pay_upfront` key of the created Investment record is set to <b>true</b> then by `django signals` an Upfront Fee is automatically generated. You can check it by going to http://localhost:8000/api/list-upfront/ :
```javascript
[
    {
        "investment_id": 1,
        "investment_amount": 50000.0,
        "upfront_fee": 3750.0,
        "invoice_expiring_date": "2023-01-25"
    }
]
```

If pay_upfront is set to false an Yearly Fee is automatically generated, depending on the date of the Investment. If the Investment creation date is greater than 31-03-2019 the Yearly fee would contain a certain type of description and the value is calculated based on a preset business rule. An the same for Yearly Fees oldest or equal than 31-03-2019.

You can check this by going to http://localhost:8000/api/list-yearly-after/ for fees after and http://localhost:8000/api/list-yearly-before/ for fees before 31-03-2019. Supose, if you have an investment that the creation date was on 25-01-2017 for $50.000, you may get the following. All depends on the calculation function to determinate the `fee_amount`.
```javascript
[
    {
        "investment_id": 2,
        "investment_amount": 50000.0,
        "fee_amount": 3750.0,
        "description": "Before-04-2019 Fee for first year",
        "invoice_expiring_date": "2018-01-25"
    }
]
```

Also, when you first create a new Investor, a Membership Fee is automatically generated. You can check this by going to http://localhost:8000/api/list-membership/

All of this endpoints mention before, they could have the a query string to filter based on an Investor ID. Ex: http://localhost:8000/api/list-membership/?investor=1

## Updating Fees

If you want to check for updates in your fees, go to the group of `update-` prefix endpoints. If the backend realize that some of the Yearly or Membership Fees are pending of billing, it going to generate a new one for every year pased since Investment creation date. If they are already created, you will see an empty array (list). For exmaple, the Yearly fee created above, it says "Before-04-2019 Fee for first year", but the invoice expiring date for the first year was 01-25-2018, so if the Investor is still active, it has to have al least 4 more fees generated for that particular Investment with ID 2. So, let's got to http://localhost:8000/api/yearly-update-before/?investor=1
```javascript
    {
    "investor": 1,
    "new_fees": [
        {
        "investment_id": 2,
        "investment_amount": 50000,
        "fee_amount": 750,
        "description": "Before-04-2019 for year 2",
        "invoice_expiring_date": "2019-01-25"
        },
        {
        "investment_id": 2,
        "investment_amount": 50000,
        "fee_amount": 750,
        "description": "Before-04-2019 for year 3",
        "invoice_expiring_date": "2020-01-25"
        },
        {
        "investment_id": 2,
        "investment_amount": 50000,
        "fee_amount": 750,
        "description": "Before-04-2019 for year 4",
        "invoice_expiring_date": "2021-01-25"
        },
        {
        "investment_id": 2,
        "investment_amount": 50000,
        "fee_amount": 750,
        "description": "Before-04-2019 for year 5",
        "invoice_expiring_date": "2022-01-25"
        }
    ]
    }
```
And now you have that Investmet up to date!

## Bills creation

For the grouping bills creation, they are not generated automatically, first you have to give a list of all the Fees IDs that are going to be present in that particular bill, based on some kind of filtering business rule. For example, let's supose that we want to generate a bill with all the Yearly fees mention before, plus the Upfront fee and the Membership. The request body JSON must have the following format:
```javascript
    {
        "cash_call_expire": "2022-01-25",
        "state": "G",
        "investor": 0,
        "upfront_fees": [
            0
        ],
        "yearly_before": [
            0
        ],
        "membership": [
            0
        ]
}
```
The response for this particular request may be:
```javascript
    {
        "id_bill": 1,
        "investor": "Juan",
        "upfront_fees": [
            {
                "investment_id": 1,
                "investment_amount": 50000.0,
                "upfront_fee": 3750.0,
                "invoice_expiring_date": "2023-01-25"
            }
        ],
        "yearly_before": [
            {
                "investment_id": 2,
                "investment_amount": 50000.0,
                "fee_amount": 3750.0,
                "description": "Before-04-2019 Fee for first year",
                "invoice_expiring_date": "2018-01-25"
            },
            {
                "investment_id": 2,
                "investment_amount": 50000.0,
                "fee_amount": 750.0,
                "description": "Before-04-2019 for year 2",
                "invoice_expiring_date": "2019-01-25"
            },
            {
                "investment_id": 2,
                "investment_amount": 50000.0,
                "fee_amount": 750.0,
                "description": "Before-04-2019 for year 3",
                "invoice_expiring_date": "2020-01-25"
            },
            {
                "investment_id": 2,
                "investment_amount": 50000.0,
                "fee_amount": 750.0,
                "description": "Before-04-2019 for year 4",
                "invoice_expiring_date": "2021-01-25"
            },
            {
                "investment_id": 2,
                "investment_amount": 50000.0,
                "fee_amount": 750.0,
                "description": "Before-04-2019 for year 5",
                "invoice_expiring_date": "2022-01-25"
            }
        ],
        "membership": [
            {
                "membership_amount": 0.0,
                "year_of_membership": 1
            }
        ],
        "cash_call_expire": "2022-02-09",
        "state": "G"
    }
```
Note that in this case, the membership amount is zero, becouse the sum of Investmets for this year overcome an arbitrary threshold.

The `cash_call_expire` is set default to `today + 15 days`, but you can customize it. The `state` by default is 'G' that is a short for 'GENERATED'. The state choices are:
* 'G' : Generated
* 'V' : Validated
* 'S' : Sendt by email
* 'P' : Paid
* 'O' : Overdue

The human that is in charge to do the control of the bills state have the option to group them by investor and also by state. A few endpoints were made to simulate the validation, the email send, marked as paid or marked as overdue, that basically change the `state` of a given bill. For example If you go to http://localhost:8000/api/validate-bill/?bill=1 you get:
```javascript
    {
        "msg": "Bill nro 1 validated successfully for investor Juan Perez / The Juan Perez Company"
    }
```

## Shutting Down

* To shutdown and remove CTRL + C and...
```sh
   docker-compose down
   ```

## Run Outside Docker

If you want to use it locally without the docker-compose

* Go inside the folder and create a virtual environment
```sh
    python -m venv venv
```
* Activate the venv
    - Windows : .\venv\Scripts\activate
    - Unix based system:  source ./venv/bin/activate


* Install the requirements
```sh
   pip install -r requirements.txt
   ```
* Last:
```
python /oneragtime-test/src/manage.py
```
 and there you go!




<!-- CONTACT -->
## Contact

Jonathan Rios - jonathanrios@live.com.ar




[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/jonathanrios11/