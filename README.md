# seniordesign
Senior Design Repository for the Statefarm Automotive Fraud Project

## Database Access
Make a copy of the ``.env.example`` file and make the following changes.
1. remove ``.example`` from the extension
2. Paste the username and password provided in MongoDB Atlas (if you should have access but do not, please contact @waseem-polus)
3. Paste the connection URL provided provided in MongoDB Atlas. Include the password and username fields using ``${VARIABLE}`` syntax to embed the value of the variable

## Run Scrapers locally
**Prerequisites**
- python3
- pipenv

**Installing dependencies**  
Navigate to ``scrapers/`` and open the virtual environment using
```bash
pipenv shell
```
Then install dependencies using
```bash
pipenv install
```

**Scraper Usage**  
To create build a Docker Image use
```bash
pipenv run build
```
to run a docker container "smarecontainer" use
```bash
pipenv run cont
```
then
```bash
# Scrape Craigsist homepage
pipenv run craigslist

# Scrape Facebook Marketplace homepage
pipenv run facebook
```
