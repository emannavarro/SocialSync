import requests

url = 'https://socialsync-434423.wl.r.appspot.com/register'  # Replace with your actual endpoint URL

# Sample data to send in the POST request
data = {
    "first_name": "John",
    "middle_name": "A",  # Optional field
    "last_name": "Doe",
    "email": "johndoe@example.com",
    "dob": "1990-01-01",
    "sex": "Male",
    "country": "USA",
    "street_address": "1234 Elm St",
    "city": "Some City",
    "state": "CA",
    "zip_code": "12345",
    "password": "securepassword123"
}

# Send the POST request
response = requests.post(url, json=data)

# Print the response
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
