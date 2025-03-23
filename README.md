# Ticketing

This is a Django-based ticket reservation system. The project allows users to book, cancel, and view tickets and available berths.

## Features

- Book tickets
- Cancel tickets
- View booked tickets
- View available berths

## Requirements

- Docker
- Docker Compose

## Setup

1. **Clone the repository:**

```sh
   git clone https://github.com/yourusername/ticketing.git
   cd ticketing
```

2. **Build and run the Docker containers:**
``` sh

   docker-compose up --build -d

#    docker compose exec web python manage.py migrate

   docker-compose exec web python manage.py reset_berths
```

You can also get the image from docker hub with command
    

```sh 
    docker pull gaurav8341/ticket
```

Dont forget to run the `migrate` and `reset_berths` command

3. **Access the application:**

    Access the application on link `http:localhost:8000`

4. **To Stop the application:**:

```sh
    docker compose down
```


## API Documentation

To see the Detailed postman documentation hop on to: https://documenter.getpostman.com/view/22518061/2sAYkHoJRM
This is a basic api application to book railway tickets.

### 1. End-point: available berths
Get all the berths available for booking
#### Method: GET
>```
>http://localhost:8000/tickets/available/
>```

#### Output: 
>```json
>{
>    "berths": [
>        {
>            "berth_type": "SL",
>            "berth_number": 1
>        },
>        {
>            "berth_type": "MB",
>            "berth_number": 3
>        },
>        ....
>    ]
>}
>```

⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

### 2. End-point: booked
Get all the booked tickets
#### Method: GET
>```
>http://localhost:8000/tickets/booked/
>```
#### Output
>```json
>{
>    "tickets": [
>        {
>            "ticket_id": 1,
>            "passenger_name": "gfd",
>            "passenger_age": 26,
>            "passenger_gender": "F",
>            "berth_type": "LB",
>            "infants": [
>                {
>                    "passenger_name": "asd",
>                    "passenger_age": 4
>                }
>            ],
>            "berth_number": 2,
>            "ticket_type": "CNF"
>        },
>        ....
>    ]
>}
>```

⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

### 3. End-point: book
Book the ticket for the given passnger details.

Give the Infant details if it applies to you.

Gender: applicable values are M : Male, F: Female, O: Other

If tickets are not available then "No Tickets available" message will ome with 400 error message  
  
Otherwise ticket detals will appear with the berth details if applicable

#### Method: POST

>```
>http://localhost:8000/tickets/book/
>```

#### Body (**raw**)

>```json
>{
>    "passenger_name": "gfd",
>    "passenger_age": "26",
>    "infants": [{
>        "passenger_name":"asd",
>        "passenger_age":"4",
>        "gender": "F"
>    }],
>    "gender": "F"
>}
>```

#### Output
>```json
>{
>    "ticket_id": 4,
>    "ticket_type": "CNF",
>    "berth_number": 9,
>    "berth_type": "LB"
>}
>```


⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃ ⁃

### 4. End-point: cancel
Cancel the given ticket id.  
  
On cancellation the next booked RAC, WL ticket will be taken for consideration.


#### Method: POST

>```
>http://localhost:8000/tickets/cancel/
>```

#### Body (**raw**)

>```json
>{
>    "ticket_id":"3"
>}
>```

#### Output

>```json
>{
>    "message": "Ticket cancelled"
>}
>```



## License

This project is licensed under the MIT License.