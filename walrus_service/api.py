import database

# import memory_controller
import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from models import Walrus
from mongo_controller import WalrusManager
from walrus_classifier import InferenceModel

app = FastAPI()

inference_model = InferenceModel()

db: database.WalrusRepository = WalrusManager()


@app.get("/", status_code=status.HTTP_200_OK)
async def check_server() -> JSONResponse:
    """Check the server status.

    Returns:
        JSONResponse:
            JSON response containing the server status.
            The response will be a dictionary with a single key-value pair:
            - status (bool): The status of the server, True indicating that
            the server is running.
    """
    return JSONResponse({"status": True})


@app.get("/walruses/get", status_code=status.HTTP_200_OK)
def get_walrus(name: str) -> JSONResponse:
    """Get a walrus from the database by name.

    Args:
        name (str): The name of the walrus to be found.

    Returns:
        JSONResponse: JSON response containing the walrus data.
            The walrus is represented as a dictionary with the following keys:
            - name (str): Name of the walrus.
            - friends (List[str]): List of the walrus's friends.
            - favourite_food (str): Favorite food of the walrus.
            - birth_date (str): TBirth date of the walrus in the format
            "YYYY-MM-DD".

    Raises:
        HTTPException: If the walrus is not found in the database. The status
        code will be 404 (Not Found).
            status_code (int): HTTP status code indicating the type of error.
            detail (str): Details of the exception.
    """
    try:
        walrus = db.get(name)
        walrus_data = {
            "name": walrus.name,
            "friends": walrus.friends,
            "favourite_food": walrus.favourite_food,
            "birth_date": walrus.birth_date.strftime("%Y-%m-%d"),
        }
        return JSONResponse(walrus_data)
    except database.WalrusNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@app.get("/walruses/getall", status_code=status.HTTP_200_OK)
def get_all_walruses() -> JSONResponse:
    """Get all walruses from the database.

    Returns:
        JSONResponse: JSON response containing a list of found walruses.
            Each walrus is represented as a dictionary with the following keys:
            - name (str): Name of the walrus.
            - friends (List[str]): List of the walrus's friends.
            - favourite_food (str): Favorite food of the walrus.
            - birth_date (str): Birth date of the walrus in the format
            "YYYY-MM-DD".

    Raises:
        HTTPException: If an error occurs while retrieving the walruses from
        the database. The status code will be 500 (Internal Server Error).
            status_code (int): HTTP status code indicating the type of error.
            detail (str): Details of the exception.
    """
    try:
        walruses = db.get_all()
        walruses_data = []
        for walrus in walruses:
            walrus_data = {
                "name": walrus["name"],
                "friends": walrus["friends"],
                "favourite_food": walrus["favourite_food"],
                "birth_date": walrus["birth_date"],
            }
            walruses_data.append(walrus_data)
        return JSONResponse(walruses_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/walruses/add", status_code=status.HTTP_201_CREATED)
def add_walrus(walrus: Walrus) -> JSONResponse:
    """Create a walrus record in the database.

    Args:
        walrus (Walrus): Walrus data.

    Returns:
        JSONResponse: JSON response containing the name of the created walrus.
            message (str): Success message indicating the walrus was added
            successfully.

    Raises:
        HTTPException: If the walrus name is not unique.
            status_code (int): HTTP status code indicating the type of error.
            detail (str): Details of the exception.

    """
    try:
        db.add(walrus)
        return JSONResponse(
            {"message": f"Walrus: {walrus.name} added successfully"}
        )
    except database.UniqueWalrusException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@app.put("/walruses/modify/{name}", status_code=status.HTTP_200_OK)
def modify_walrus(name: str, favourite_food: str) -> JSONResponse:
    """Update a walrus by name.

    Args:
        name (str): Name of the walrus to modify.
        favourite_food (str): New favorite food for the walrus.

    Returns:
        JSONResponse: JSON response indicating the success of the modification.
            message (str): Message confirming the successful modification.

    Raises:
        HTTPException: If the walrus is not found or the data was not changed.
            status_code (int): HTTP status code indicating the type of error.
            detail (str): Details of the exception.
    """
    try:
        db.modify(name, favourite_food)
        return JSONResponse(
            {"message": f"Walrus '{name}' has been successfully modified."}
        )
    except database.WalrusUnchangedException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    except database.WalrusNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@app.delete("/walruses/delete/{name}", status_code=status.HTTP_200_OK)
def delete_walrus(name: str) -> JSONResponse:
    """Delete walrus data from the db.

    Args:
        name (str): Name of the walrus to delete.

    Raises:
        HTTPException: If the walrus is not found.

    Returns:
        JSONResponse: JSON response indicating the success of the operation.
            message (str): Message confirming the deletion of the walrus.
    """
    try:
        db.delete(name)
        return JSONResponse(
            {"message": f"Walrus '{name}' deleted successfully."}
        )
    except database.WalrusNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@app.get("/walruses/getprediction", status_code=status.HTTP_200_OK)
def get_walrus_prediction(name: str) -> JSONResponse:
    """Get a prediction whether a walrus is lonely or has friends.

    Args:
        name (str): Name of the walrus.

    Raises:
        HTTPException: If the walrus is not found.

    Returns:
        JSONResponse: JSON response containing the prediction.
            prediction (str): Prediction indicating whether the walrus is
            lonely or has friends.
    """
    try:
        walrus = db.get(name)
    except database.WalrusNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )

    prediction = inference_model.predict(walrus.friends)
    return JSONResponse({"prediction": prediction})


if __name__ == "__main__":
    uvicorn.run("api:app", reload=True, host="0.0.0.0", port=1234)
