import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

def train_and_log(learning_rate_init=0.001, batch_size=64, hidden_layer_sizes=(100,),
                   n_epochs=30, run_name=None):
    with mlflow.start_run(run_name=run_name):
        mlflow.log_param("learning_rate_init", learning_rate_init)
        mlflow.log_param("batch_size", batch_size)
        mlflow.log_param("hidden_layer_sizes", hidden_layer_sizes)
        mlflow.log_param("n_epochs", n_epochs)
        mlflow.log_param("model_type", "MLPClassifier")

        model = MLPClassifier(
            hidden_layer_sizes=hidden_layer_sizes,
            learning_rate_init=learning_rate_init,
            batch_size=batch_size,
            warm_start=True,
            max_iter=1,
            random_state=42,
        )

        for epoch in range(n_epochs):
            model.fit(X_train, y_train)
            train_loss = model.loss_
            train_acc = accuracy_score(y_train, model.predict(X_train))
            val_acc = accuracy_score(y_test, model.predict(X_test))

            mlflow.log_metric("train_loss", train_loss, step=epoch)
            mlflow.log_metric("train_accuracy", train_acc, step=epoch)
            mlflow.log_metric("val_accuracy", val_acc, step=epoch)

        mlflow.log_metric("final_val_accuracy", val_acc)
        
        run_id = mlflow.active_run().info.run_id
        print(f"Logged run {run_id}  |  lr={learning_rate_init}  batch_size={batch_size}  final_val_acc={val_acc:.4f}")
        return run_id
