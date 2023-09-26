from typing import List

import torch
import torch.nn as nn
import torch.optim as optim


class LinearClassifier(nn.Module):
    def __init__(self):
        super(LinearClassifier, self).__init__()
        self.linear = nn.Linear(1, 1)
        self.activation = nn.Sigmoid()

    def forward(self, x):
        """Forward pass of the linear classifier.

        Args:
            x (torch.Tensor): Input tensor.

        Returns:
            torch.Tensor: Output tensor after applying linear and
            sigmoid operations.
        """
        x = self.linear(x)
        x = self.activation(x)
        return x


def preprocess(data: List[str]) -> torch.Tensor:
    """Preprocesses the data to a tensor.

    Args:
        input_data (list[str]): Input data for prediction.

    Returns:
        torch.Tensor: Preprocessed data tensor.
    """
    if data:
        return torch.tensor([1], dtype=torch.float32)
    else:
        return torch.tensor([0], dtype=torch.float32)


def train():
    """Trains the linear classifier model.

    This function trains the model using the defined training data
    and saves the trained model
    parameters to a file.
    """
    model = LinearClassifier()
    criterion = nn.BCELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.1)

    train_data = [
        ([0], [0]),
        ([1], [1]),
    ]

    for epoch in range(1000):
        running_loss = 0.0
        for inputs, labels in train_data:
            optimizer.zero_grad()
            inputs = torch.tensor(inputs, dtype=torch.float32)
            labels = torch.tensor(labels, dtype=torch.float32)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print(f"Epoch {epoch + 1}: Loss = {running_loss}")

    torch.save(model.state_dict(), "model.pth")


class InferenceModel:
    def __init__(self):
        self.model = LinearClassifier()
        self.model.load_state_dict(torch.load("model.pth"))
        self.model.eval()

    def predict(self, input_data: List[str]) -> str:
        """Performs prediction using the trained linear classifier model.

        Args:
            input_data (list[str]): Input data for prediction.

        Returns:
            int: Predicted value. # CR -> bool
        """
        input_tensor = preprocess(input_data)
        output = self.model(input_tensor)
        predicted_value = output > 0.5

        if predicted_value:
            return "Walrus has friends"
        else:
            return "Walrus is lonely"
