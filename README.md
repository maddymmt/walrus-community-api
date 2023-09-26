
# Walrus Community API

## Project Overview
This project is a Walrus Community CRUD RESTful API developed using FastAPI and MongoDB, with a streamlit service for user interaction. The API allows for creating, reading, updating, and deleting Walrus data, as well as predicting via a trained model.

## Project Structure
The project has two main services: `streamlit_service` and `walrus_service`, each containing several Python files responsible for different aspects of the application.

### Streamlit Service
This service provides an interface for user interaction, implemented with Streamlit and located in the `streamlit_service` directory.

#### Files
- **config.py**
  - Loads environment variables.
- **entrypoint.py**
  - Currently empty, used only as entrypoint for streamlit
- **status_codes.py**
  - Holds HTTP status codes.

#### Pages
The following files in the `pages` directory are responsible for different pages in the Streamlit interface:
- **1_add.py**: Page for adding Walrus.
- **2_get.py**: Page for retrieving a specific Walrus by name.
- **3_get_all.py**: Page for retrieving all Walruses.
- **4_modify.py**: Page for modifying the favorite food of a Walrus.
- **5_delete.py**: Page for deleting a Walrus by name.
- **6_prediction.py**: Page for predicting via the trained model.

### Walrus Service
This service is responsible for the CRUD operations for Walrus and is located in the `walrus_service` directory.

#### Files
- **api.py**
  - Defines the API routes for CRUD operations and predictions.
- **config.py**
  - Loads environment variables.
- **database.py**
  - Defines abstract classes for database operations and custom exceptions.
- **memory_controller.py**
  - Implements in-memory database operations.
- **models.py**
  - Defines Pydantic models for Walrus data.
- **mongo_controller.py**
  - Implements MongoDB database operations.
- **training_run.py**
  - Contains (commented-out) code for training runs.
- **walrus_classifier.py**
  - Implements a linear classifier and an inference model with PyTorch.

## Running the Project
### Prerequisites
- Python 3.9
- Docker
- MongoDB
- Postman (For API Testing)

### Steps
1. Navigate to the project directory.
2. Run `docker-compose up` to start the services.
3. Interact with the Streamlit interface or test the API using Postman.

## Testing
The project can be tested manually using Postman or programmatically using Python's `requests` or `httpx` libraries.

## Code Quality and Formatting
- Flake8 for style guide enforcement.
- Mypy for type checking.
- Black and isort for code formatting.

## Notes
- Ensure to have the required environment variables set up, as specified in the `config.py` files of each service.
- Review the `docker-compose.yml` and `dev.yml` files for service configuration and port setup.
