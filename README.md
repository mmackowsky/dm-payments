# DeviceMinder - Payments Service

## Description
<p>
   Service has a task to handle the operation of making payment for subscriptions by Stripe. There is an endpoint that makes payment session which generate url to Stripe form. After fill in the form and making a request, the webhook is listening what events happen and doing operations like: saving data to the database etc.
</p>

## Technologies

<ul>
  <li><img src="https://github.com/mmackowsky/HabitualLife/assets/123114901/8cc0785a-7f2c-4efd-8891-7f796c934ad8" width=15> Python 3.11</li>
  <li><img src="https://github.com/mmackowsky/HabitualLife/assets/123114901/9ffb3ef3-76a6-48da-acf2-787e8062d05e" width=20> PostgreSQL 15</li>
  <li>FastAPI</li>
  <li><img src="https://github.com/mmackowsky/HabitualLife/assets/123114901/3ab3f47d-b088-4473-bec4-330882f78bfb" width=15> Docker</li>
  <li><img src="https://github.com/mmackowsky/HabitualLife/assets/123114901/fd90329c-e363-430a-8593-952ac694c1be" width="15"> Poetry</li>
  <li>Stripe</li>
</ul>

## Setup
To use Stripe payments you need to:
- make an account on: [Stripe | Financial Infrastructure for the Internet](https://stripe.com/en-pl)
- make a project in your profile
- get STRIPE_API_KEY and put it to your .env file (all needed settings you will find in config.py file)
- to use webhook you will need to add an endpoint with it to the project that you made earlier. To do this you have to login to your Stripe account by Stripe CLI in the application terminal (poetry run stripe login). Below CLI installing tutorial: [Get started with the Stripe CLI | Stripe Documentation](https://docs.stripe.com/stripe-cli)
<img src="https://github.com/mmackowsky/dm-payments/assets/123114901/1b1a00ea-0fdd-4fda-bf30-12778507fc41">
- next do: stripe listen –forward-to <path_to_endpoint>
- now after making a payment webhook will handle all events
