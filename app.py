# app.py
# REST and Python: Tools of the Trade:
# Modules to install:
#      c:\python -m pip install flask
#      c:\python -m pip install flask-expects-json

"""In this section, you'll look at three popular frameworks for building REST APIs
in Python. Each framework has pros and cons, so you'll have to evaluate which 
works best for your needs. To this end, in the next sections, you'll look at a 
REST API in each framework. All the examples will be for a similar API that 
manages a collection of countries.

Each country will have the following fields:
- name is the name of the country.
- capital is the capital of the country.
- area is the area of the country in square kilometers.
The fields name, capital, and area store data about a specific country somewhere
in the world.

Most of the time, data sent from a REST API comes from a database. Connecting to 
a database is beyond the scope of this tutorial. For the examples below, you'll 
store your data in a Python list. The exception to this is the Django REST 
framework example, which runs off the SQLite database that Django creates.

Note: It's advised that you create individual folders for each of the examples to
separate the source files. You'll also want to use virtual environments to isolate
dependencies.

To keep things consistent, you'll use countries as your main endpoint for all 
three frameworks. You'll also use JSON as your data format for all three 
frameworks.

Now that you've got the background for the API, you can move on to the next
section, where you'll look at the REST API in Flask. """


# Flask:
"""Flask is a Python microframework used to build web applications and REST APIs.
Flask provides a solid backbone for your applications while leaving many design 
choices up to you. Flask's main job is to handle HTTP requests and route them to 
the appropriate function in the application.

Note: The code in this section uses the new Flask 2 syntax. If you're running an 
older version of Flask, then use @app.route("/countries") instead of 
@app.get("/countries") and @app.post("/countries").

To handle POST requests in older versions of Flask, you'll also need to add the 
methods parameter to @app.route():

@app.route("/countries", methods=["POST"])
This route handles POST requests to /countries in Flask 1.

Below is an example Flask application for the REST API:"""

# app.py
from flask import Flask, request, jsonify, abort, url_for, render_template, json
from flask_expects_json import expects_json
from werkzeug.exceptions import HTTPException


app = Flask(__name__)

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "capital": {"type": "string"},
        "area": {"type": "number"},
    },
    "required": ["name", "capital"],
}

countries = [
    {"id": 1, "name": "Thailand", "capital": "Bangkok", "area": 513120},
    {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
    {"id": 3, "name": "Egypt", "capital": "Cairo", "area": 1010408},
]


def _find_next_id():
    return max(country["id"] for country in countries) + 1


@app.get("/countries")
def get_countries():
    return jsonify(countries)  # Returns the list of all countries in the


#   Dictionary list, this could also be extracted from a database table.


@app.post("/countries")
@expects_json(schema)  # expect payload in json format if not 415 error.
def add_country():
    # if request.is_json:  No needed because we are using @expect_json(schema)
    #                      which automatically covers all errors related to
    #                      400 "BAD Request", 415-> 'UNSUPPORTED MEDIA TYPE',
    # this means that if the payload/data is invalid, then the Request will be
    # aborted with error code 400 or 415...

    print(f"request.data--> {request.data} type: {type(request.data)}")
    # request.data--> b'{"name":"peru", "capital": "Lima", "area": 357022}'
    #                                      type: <class 'bytes'>

    print(f"request.json--> {request.json} type: {type(request.json)}")
    # request.json--> {'name': 'peru', 'capital': 'Lima', 'area': 357022}
    #                                      type: <class 'dict'>

    expected_payload_attributes = ("name", "capital", "area")

    # Validate all keys in payload, if not raise error 400 - Bad Request
    # payload_dict = json.loads(request.data)
    for key in request.json:  # which is a dictionary datatype.
        print(f"key --> {key}")
        if key not in expected_payload_attributes:
            abort(422)

    payload = request.get_json()
    print(f"type(payload) --> {type(payload)}")
    # OUTPUT: type(payload) --> <class 'dict'>

    print(f" LENGTH: {len(payload)} AND {len(countries[0].keys())}")
    if len(payload) + 1 != len(countries[0].keys()):
        abort(400)  # abort number of attribute in payload not enough

    country = request.get_json()  # get data from the payload in dict datatype
    print(f"type(country) --> {type(country)}")
    # OUTPUT: type(country) --> <class 'dict'>
    country["id"] = _find_next_id()  # complete the data to post
    countries.append(country)  # append to the dict/database.
    return jsonify(country), 201

    # return {"error": "Request must be JSON"}, 415   no needed.


@app.errorhandler(Exception)  # Registering the Error/Exception handle for
#                               all possible errors or exceptions.
def handle_exception(exception):
    # This exceptions handle handles all type of exceptions.
    # pass through HTTP errors:
    if isinstance(exception, HTTPException):
        """Return in JSON format instead of HTML for each HTTP method errors"""
        # start with the correct headers and status code from the error/exception
        response_hector = exception.get_response()

        # convert the response_hector body/data to JSON format
        response_hector.data = json.dumps(
            {
                "code": exception.code,
                "message": exception.name,
                "description": exception.description,
            }
        )
        response_hector.content_type = "application/json"

        return response_hector

    # below to handle the non-HTTP exceptions only:
    # return render_template("500_generic.html", e=exception), 500
    return jsonify(error=str(exception)), 500  # convert to json.


"""This application defines the API endpoint /countries to manage the list of 
countries. It handles two different kinds of requests:

GET /countries returns the list of countries.
POST /countries adds a new country to the list.
Note: This Flask application includes functions to handle only two types of 
requests to the API endpoint, /countries. In a full REST API, you'd want to 
expand this to include functions for all the required operations.

You can try out this application by installing flask with pip:
$ python -m pip install flask

Once flask is installed, save the code in a file called app.py. To run this 
Flask application, you first need to set an environment variable called FLASK_APP
 to app.py. This tells Flask which file contains your application.

Run the following command inside the folder that contains app.py:

$ export FLASK_APP=app.py   --) en Unix
This sets FLASK_APP to app.py in the current shell. Optionally, you can set
FLASK_ENV to development, which puts Flask in debug mode:
$ export FLASK_ENV=development

Besides providing helpful error messages, debug mode will trigger a reload of 
the application after all code changes. Without debug mode, you'd have to 
restart the server after every change.

Note: The above commands work on macOS or Linux. If you're running this on 
Windows, then you need to set FLASK_APP and FLASK_ENV like this in the Command
Prompt:
C:\> set FLASK_APP=app.py
C:\> set FLASK_ENV=development
Now FLASK_APP and FLASK_ENV are set inside the Windows shell.

With all the environment variables ready, you can now start the Flask development
server by calling flask run:

$ flask run
* Serving Flask app "app.py" (lazy loading)
* Environment: development
* Debug mode: on
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
This starts up a server running the application. Open up your browser and go to 
http://127.0.0.1:5000/countries, and you'll see the following response:
[
    {
        "area": 513120,
        "capital": "Bangkok",
        "id": 1,
        "name": "Thailand"
    },
    {
        "area": 7617930,
        "capital": "Canberra",
        "id": 2,
        "name": "Australia"
    },
    {
        "area": 1010408,
        "capital": "Cairo",
        "id": 3,
        "name": "Egypt"
    }
]
This JSON response contains the three countries defined at the start of app.py. 
Take a look at the following code to see how this works:
@app.get("/countries")
def get_countries():
    return jsonify(countries)

This code uses @app.get(), a Flask route decorator, to connect GET requests to a
function in the application (app.py). When you access resource /countries, Flask
calls the decorated function "get_countries()" to handle the HTTP request and 
return a response.

In the code above, get_countries() takes countries, which is a Python list of
Dictionary Python Datatype, and converts it to JSON with jsonify(). This JSON 
is returned in the response.

VERY IMPORTANT Note: Most of the time, you can just return a Python dictionary 
from a Flask function. Flask will automatically convert any Python dictionary to
JSON. You can see this in action with the function below:"""


@app.get("/country")
def get_country():
    return jsonify(countries[1])


"""In this code, you return the second dictionary from countries. Flask will 
convert this dictionary to JSON. Here's what you'll see when you 
request /country:

{
    "area": 7617930,
    "capital": "Canberra",
    "id": 2,
    "name": "Australia"
}
This is the JSON version of the dictionary you returned from get_country().

In get_countries(), you need to use jsonify() because you're returning a list of 
dictionaries and not just a single dictionary. Flask doesn't automatically 
convert lists to JSON.

Now take a look at add_country(). This function handles POST requests to
/countries and allows you to add a new country to the list. It uses the Flask 
request object (imported in line 55) to get information about the current HTTP
request:

@app.post("/countries")
def add_country():
    if request.is_json:
        country = request.get_json()
        country["id"] = _find_next_id()
        countries.append(country)
        return country, 201
    return {"error": "Request must be JSON"}, 415
This function performs the following operations:

- Using request.is_json to check that the request is JSON (based on Content-Type)
- Creating a new country instance/object with request.get_json().
- Finding the next id and setting it on the country.
- Appending the new country dictionary to countries list of dictionaries. In case
  We were using a database to store the resource, a this time we could execute 
  the query to insert into the table to store the resource.
- Returning the country in the response along with a 201 Created status code.
- Returning an error message and 415 Unsupported Media Type status code if the 
  request wasn't JSON.

add_country() also calls _find_next_id() to determine the id for the new country:
def _find_next_id():
    return max(country["id"] for country in countries) + 1

This helper function uses a generator expression to select all the country IDs 
and then calls max() on them to get the largest value. It increments this value
 by 1 to get the next ID to use.

You can try out this endpoint in the shell using the command-line tool curl, 
which allows you to send HTTP requests from the command line (We have to download 
and install curl). Or using PostMan.
Here, you'll add a new country to the list of countries:

$ curl -i http://127.0.0.1:5000/countries \
-X POST \
-H 'Content-Type: application/json' \
-d '{"name":"Germany", "capital": "Berlin", "area": 357022}'

HTTP/1.0 201 CREATED
Content-Type: application/json
...

{
    "area": 357022,
    "capital": "Berlin",
    "id": 4,
    "name": "Germany"
}
This curl command has some options that are helpful to know:

-X sets the HTTP method for the request.
-H adds an HTTP header to the request.
-d defines the request data.
With these options set, curl sends JSON data in a POST request with the 
Content-Type header set to application/json. The REST API returns 201 CREATED 
along with the JSON for the new country you added.

Note: In this example, add_country() doesn't contain any validation to confirm
that the JSON in the request matches the format of countries. Check out 
flask-expects-json (at https://pypi.org/project/flask-expects-json/) if you'd 
like to validate the format of JSON in Flask.

You can use curl to send a GET request to /countries to confirm that the new 
country was added. If you don't use -X in your curl command, then it sends a GET
request by default:

$ curl -i http://127.0.0.1:5000/countries

HTTP/1.0 200 OK
Content-Type: application/json
...

[
    {
        "area": 513120,
        "capital": "Bangkok",
        "id": 1,
        "name": "Thailand"
    },
    {
        "area": 7617930,
        "capital": "Canberra",
        "id": 2,
        "name": "Australia"
    },
    {
        "area": 1010408,
        "capital": "Cairo",
        "id": 3,
        "name": "Egypt"
    },
    {
        "area": 357022,
        "capital": "Berlin",
        "id": 4,
        "name": "Germany"
    }
]
This returns the full list of countries in the system, with the newest country at
the bottom.

This is just a sampling of what Flask can do. This application could be expanded 
to include endpoints for all the other HTTP methods. Flask also has a large 
ecosystem of extensions that provide additional functionality for REST APIs, 
such as database integrations, authentication, and background processing.
"""


# Get specific country by id.
@app.get("/countries/<parm_id>")
def get_country_by_id(parm_id):
    print(f"parm_id --> {parm_id}")
    country_found = False

    for country in countries:
        if country["id"] == int(parm_id):
            country_found = True
            return jsonify(country)

    if not country_found:
        abort(404)


# PUT Method:
@app.put("/countries/<parm_id>")
def put_country(parm_id):
    country_found = False

    # validate all key in payload:
    expected_payload_attributes = ("name", "capital", "area")
    for key in request.json:
        if key not in expected_payload_attributes:
            abort(422)

    payload = request.get_json()
    print(f"type(payload) --> {type(payload)}")
    # OUTPUT: type(payload) --> <class 'dict'>

    print(f" LENGTH: {len(payload)} AND {len(countries[0].keys())}")
    if len(payload) + 1 != len(countries[0].keys()):
        abort(400)  # abort number of attribute in payload not enough

    for i in range(len(countries)):
        if countries[i]["id"] == int(parm_id):
            country_found = True

            for key in payload:
                countries[i][key] = payload[key]

            return jsonify(countries[i]), 200

    if not country_found:
        abort(404)


# PATCH Method:
@app.patch("/countries/<parm_id>")
def patch_country(parm_id):
    country_found = False

    # validate all key in payload:
    expected_payload_attributes = ("name", "capital", "area")
    for key in request.json:
        if key not in expected_payload_attributes:
            abort(422)

    payload = request.get_json()
    print(f"type(payload) --> {type(payload)}")
    # OUTPUT: type(payload) --> <class 'dict'>

    print(f" LENGTH: {len(payload)} AND {len(countries[0].keys())}")
    if len(payload) + 1 > len(countries[0].keys()):
        abort(400)  # abort number of attribute in payload > countries

    for i in range(len(countries)):
        if countries[i]["id"] == int(parm_id):
            country_found = True

            for key in payload:
                countries[i][key] = payload[key]

            return jsonify(countries[i]), 200

    if not country_found:
        abort(404)


# DELETE Method:
@app.delete("/countries/<parm_id>")
def delete_country(parm_id):
    country_found = False

    for i in range(len(countries)):
        if countries[i]["id"] == int(parm_id):
            country_found = True

            del countries[i]

            return {}, 204

    if not country_found:
        abort(404)
