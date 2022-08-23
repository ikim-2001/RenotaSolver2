# Renota Solver
### The first iteration of Renota's Solver takes in Algebra 1 work, (currently single-variable equations/inequalities), and returns in "{}" any algebraic terms that were incorrectly calculated during the mathematical process.

<p align="right">(<a href="https://github.com/ikim-2001/Mathpix/">Renota Solver Frontend</a>)</p>

## Local Flask setup before running on Postman

1. Clone the repo
   ```sh
   git clone https://github.com/ikim-2001/RenotaSolver2/
   ```
2. Open directory in virtual environment (i.e., PyCharm)

3. Download simpy, flask, and CORS for flask
   ```sh
   pip install simpy flask -U flask-cors
   ```

4. Run application.py 
   ```sh
   python application.py 
   ```
   
Running the Flask application should output a localhost IP address similar to the one shown below:

![LMFAO](https://github.com/ikim-2001/RenotaSolver2/blob/main/img/application.png?raw=true)
   
## Making local POST requests on Postman

Using your localhost IP address, enter "http://YourFlaskAppLocalHostIPaddress/test" into the URL section of Postman. 

Format the body of your request json as shown below:

![LMFAO](https://github.com/ikim-2001/RenotaSolver2/blob/main/img/postman.png?raw=true)


<p align="right">(<a href="#readme-top">back to top</a>)</p>

