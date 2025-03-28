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

>```sh
>   git clone https://github.com/yourusername/ticketing.git
>   cd ticketing
>```

2. **Build and run the Docker containers:**

We are using same 5432 port for db contaner. 

**Please make sure that youre postgres service is down**

>``` sh
>
>   docker-compose up --build -d
>
>#    docker compose exec web python manage.py migrate
>```

In case you want to reset your application data run this command.

>```sh
>   docker-compose exec web python manage.py reset_berths
>```

You can also get the image from docker hub with command
    

>```sh 
>    docker pull gaurav8341/ticket
>```

Dont forget to run the `migrate` and `reset_berths` command

3. **Access the application:**

    Access the application on link `http:localhost:8000`

4. **To Stop the application:**:

>```sh
>    docker compose down
>```


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

## TODO:

#### Django templates and forms

1. Add Django templates and forms for better UI experience

2. Should be debated to go with django templates or React

#### Authentication and Authorizaton.

1. User authentication will require adding new login, logout and signup apis

2. For Authorization part the user will only be able to see the ticket details of the ticktes he has ownership of or he is staff member.

#### Testacases

1. Django testcases to be written

2. Postman testcases

#### Booking Logic Revamp

Currently only one ticket details can be booked at a time. Real product will not behave in such a way.

1. Make sure to allow multiple passengers to allow booking of tickets.

2. Allow at least 5 passengers to book the ticket at a time. This will change many things.
    - the request payload will change.
    - Currently we are telling which seat to be allocated.
    - But Nonetheless select nearbuy seats if multiple passengers are being booked. 

    - This will make things easier, will also make the priority cpde redundant but Maybe give user the freedom to select his own seats

#### Allow Trains to be added

1. Trains to be added by staff user. with their schdule and number coaches with their type.

2. Each Berth Will have sertain Coaches with differeing type

3. Each Coach will have certain number of berths.

4. Coach, Train These models will be added newly.

5. Because of the new things the lock mechanosm will change. It will be based on time. While booking, first check if that berth has any seat allocated for the journey time.

#### Emails and updates.
Send emails to the user in case of confirmation or update in ticket details.

#### Models

1. Train
2. Coaches
3. TrainJourneyLog -- will have all the relavant details like how many passengers of which type and all metadata.
4. PaymentLogs --
5. CustomUser -- With option for staff user and passenger user, etc

## License

This project is licensed under the MIT License.