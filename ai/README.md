
## AI vs Me
**What did the AI do better — and do you understand its version well enough to explain it?**
The AI agent is really good at creating boiler templates for CRUD, it actually created a shorter version of the code, as well as a more robust error handling for update compared to what I have written, and it seems that it also considered integrating the object to the dictionary which I did not really thought of. It does make sense, because it actually refined how my validation works.

I can explain most of the code like why it used Pydantic models for validation, why declare an ID rather than creating a workaround for auto increment. Though, there are parts that I dont really like about, it relied more on the library functions, though yes, I'd say, that should how we code relying on the libraries, I dont like it because of that reason, solely, its also because I didnt read enough of the docs, it makes me look or double check how that particualr function works.

**What did it get wrong or quietly ignore from your prompt? (A missing 400 ? A wrong status code? A database you never asked for?)**
In the prompt, it asked me if I want to implement a database, and so if I let the ai on autopilot it would've implemented a database. I think I didnt had a proble for this because I refined the prompt before giving it to the AI agent to create the project.

**What did your prompt forget to specify — and what did the AI silently decide for you?**
Mainly I forgot tests, like the curl requests, it automatically created those. Which its an advantage using AI, beause it can automatically do those tests, rather than check it in the terminal. Also I think it read what I made, so it got the gist of what I want and just refined it.

I refined my prompt using Chatgpt 


# Original Prompt
Create a simple CRUD for managing Tasks using Python and FastAPI. Install all dependencies using pip and use in-memory storage. Implement auto increment, also  validate the JSON Body for whitespaces,the JSON structure would look like:

{
  "id": 1,
  "title": "Task",
  "done": false
}
Endpoints should be POST /tasks to create a task, GET /tasks to retrieve all tasks, GET /tasks/{id} to retrieve a single task, PUT /tasks/{id} to update a task, and DELETE /tasks/{id} to delete a task.Use proper exception handling and return the correct HTTP status codes like 200 for OK and other.

# Refined

# FastAPI CRUD API Specification

## Objective

Build a simple REST API for managing **Tasks** using **Python** and **FastAPI**.

## Tech Stack

* Python
* FastAPI
* Uvicorn
* Pydantic
* Install dependencies using `pip`

## Storage

* Use **in-memory storage** only.
* Do not use a database.

## Task Model

```json
{
  "id": 1,
  "title": "Complete assignment",
  "done": false
}
```

| Field | Type    | Rules                                   |
| ----- | ------- | --------------------------------------- |
| id    | Integer | Auto-generated, unique                  |
| title | String  | Required, cannot be empty or whitespace |
| done  | Boolean | Defaults to `false`                     |

## Endpoints

| Method | Route         | Description      |
| ------ | ------------- | ---------------- |
| POST   | `/tasks`      | Create a task    |
| GET    | `/tasks`      | Get all tasks    |
| GET    | `/tasks/{id}` | Get a task by ID |
| PUT    | `/tasks/{id}` | Update a task    |
| DELETE | `/tasks/{id}` | Delete a task    |

## Validation

The API must reject:

* Empty `title`
* Whitespace-only `title`
* Missing required fields
* Incorrect data types (e.g. `"done": "true"`)
* Requests for non-existent task IDs

## Exception Handling

Handle the following cases:

* Task not found
* Invalid request body
* Validation errors
* Unexpected server errors

Return meaningful JSON error responses.

## HTTP Status Codes

| Scenario              | Status Code                 |
| --------------------- | --------------------------- |
| Successful GET        | `200 OK`                    |
| Successful POST       | `201 Created`               |
| Successful PUT        | `200 OK`                    |
| Successful DELETE     | `204 No Content`            |
| Invalid request       | `400 Bad Request`           |
| Validation failure    | `422 Unprocessable Entity`  |
| Task not found        | `404 Not Found`             |
| Internal server error | `500 Internal Server Error` |

## Deliverables

* Complete FastAPI project
* Pydantic models
* In-memory storage
* Fully functional CRUD endpoints
* Request validation
* Exception handling
* Sample request and response JSON for every endpoint
* Instructions to install dependencies and run the API using Uvicorn

