import atexit
import json
import time
import uuid
from abc import ABC, abstractmethod

import numpy as np
import tqdm

from sklearn.metrics.pairwise import distance_metrics, pairwise_distances
from sklearn.preprocessing import normalize


class BaseRetriever(ABC):

    @abstractmethod
    def query():
        pass


class LocalRetriever(BaseRetriever):

    def __init__(
        self,
        embeddings: list[list[float]] | np.ndarray,
        data: list[dict],
        norm: bool = False,
        distance_metric: str = "cosine",
    ):
        """vector similarity retrieval for local retrieval

        Args:
            embeddings (list[list[float]] | np.ndarray): list of embeddings
            data (list[dict]): list of data
            norm (bool, optional): normalize embeddings. Defaults to False.
            distance_metric (str, optional): distance metric. Defaults to "cosine".
        """
        if len(embeddings) != len(data):
            raise ValueError("The number of embeddings must equal the number of data!")
        if distance_metric not in distance_metrics():
            raise ValueError(
                f"Unknown distance metric '{distance_metric}', must be one of {list(distance_metrics().keys())}"
            )
        if norm:
            embeddings = normalize(embeddings, norm="l2")
        self.distance_metric = distance_metric
        self.embeddings = np.array(embeddings)
        self.data = data

    def query(
        self, query_vector: list[float] | np.ndarray, top_k: int = 10, distance_metric: str | None = None
    ) -> list[dict]:
        """query the retriever

        Args:
            query_vector (list[float] | np.ndarray): query vector
            top_k (int, optional): number of results. Defaults to 10.
            distance_metric (str | None, optional): override default distance metric. Defaults to None."""
        if not distance_metric:
            distance_metric = self.distance_metric
        elif distance_metric not in distance_metrics():
            raise ValueError(
                f"Unknown distance metric '{distance_metric}', must be one of {list(distance_metrics().keys())}"
            )
        query_vector = np.array(query_vector).reshape(1, -1)
        distances = pairwise_distances(query_vector, self.embeddings, metric=distance_metric)[0]
        indices = np.argsort(distances)
        results = [{"id": int(i), "distance": float(distances[i]), "data": self.data[i]} for i in indices[:top_k]]
        return results
