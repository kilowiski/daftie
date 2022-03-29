# daftie
look for house in daft ie thank you lib

dont forget make a .env file for these variables
* USER_EMAIL=
* PASSWORD=
* FULL_NAME=
* PHONE=
* MESSAGE=

### HOW THIS WORKS ###
So the flow so far is like this
1. login with ur credentials
2. Config search criteria can see inside the main.py. Maybe can make this prettier in the future
3. Perform search based on criteria & return listings
4. Sequentially visit the links to each listing
5. In each listing, webdriver will click the email agent button, fill in the form with details inside .env file
6. Submit, hopefully all OK

### WARNING ###
Please run only 1 isntance of this at a time, close the browser too if u decide to stop mid way, because if not somehow can cause missing element DOM errors yadayada
