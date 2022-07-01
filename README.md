# Problem Statement
## Application overview
<br>
Create a price alert application that triggers an email when the user’s target price is
achieved.
<br>
Say, the current price of BTC is $28,000, a user sets an alert for BTC at a price of 33,000$.
The application should send an email to the user when the price of BTC reaches 33,000$.
Similarly, say, the current price of BTC is 35,000$, a user sets an alert for BTC at a price of
33,000$. The application should send an email when the price of BTC reaches 33,000$.

# Solution

## Add
INSIDE .ENV.DEV
EMAIL_HOST_USER = {your_email_id}
EMAIL_HOST_PASSWORD = [your_password}

and run

```
docker-compose up --build
```


Users are currently added manually from the admin panel for that you would need to create a superuser 
