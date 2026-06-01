# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_d_regular_graph(n, d):
        if (d * n) % 2 != 0:
            return None
        adj_matrix = [[0] * n for _ in range(n)]
        edges_added = 0
        while edges_added < d * n // 2:
            u, v = random.sample(range(n), 2)
            if adj_matrix[u][v] == 0 and u != v:
                adj_matrix[u][v] = 1
                adj_matrix[v][u] = 1
                edges_added += 1
        return adj_matrix
    
    def quandle_representation(adj_matrix):
        n = len(adj_matrix)
        quandle = {}
        for i in range(n):
            quandle[i] = {j: (i + j) % n for j in range(n)}
        return quandle
    
    def min_rank(quandle):
        n = len(quandle)
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if quandle[i][j] == j:
                    matrix[i][j] = 1
        rank = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(rank)):
                row = [matrix[j][i] for j in range(n)]
                matrix[rank], matrix[i] = matrix[i], matrix[rank]
                for j in range(i + 1, n):
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(i, n):
                        matrix[j][k] += factor * matrix[i][k]
                rank += 1
        return rank
    
    def circuit_monotone_width(adj_matrix):
        n = len(adj_matrix)
        if n == 0:
            return 0
        width = 0
        for i in range(n):
            for j in range(i + 1, n):
                if adj_matrix[i][j] == 1 and adj_matrix[j][i] == 1:
                    width += 1
        return width
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(rank)):
                row = [matrix[j][i] for j in range(n)]
                matrix[rank], matrix[i] = matrix[i], matrix[rank]
                for j in range(i + 1, n):
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(i, n):
                        matrix[j][k] += factor * matrix[i][k]
                rank += 1
        return rank
    
    def min_rank_quandle(quandle):
        n = len(quandle)
        matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if quandle[i][j] == j:
                    matrix[i][j] = 1
        rank = gaussian_elimination(matrix)
        return rank
    
    def circuit_monotone_width_graph(adj_matrix):
        n = len(adj_matrix)
        if n == 0:
            return 0
        width = 0
        for i in range(n):
            for j in range(i + 1, n):
                if adj_matrix[i][j] == 1 and adj_matrix[j][i] == 1:
                    width += 1
        return width
    
    def run_test(d, n):
        graph = generate_d_regular_graph(n, d)
        if graph is None:
            return {"metric_name": "min_rank", "metric_value": None, "instances_tested": 0, "n_max": n, "conjecture_holds": False, "counterexample": "d-regular graph generation failed"}
        quandle = quandle_representation(graph)
        min_rank_val = min_rank_quandle(quandle)
        circuit_width_val = circuit_monotone_width_graph(graph)
        return {"metric_name": "min_rank", "metric_value": min_rank_val, "instances_tested": 1, "n_max": n, "conjecture_holds": True, "counterexample": ""}
    
    results = []
    for d in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            result = run_test(d, random.randint(5, 40))
            if result["metric_value"] is None:
                return {"seed": seed, "metric_name": "min_rank", "metric_value": None, "instances_tested": 0, "n_max": max([r["n_max"] for r in results]), "conjecture_holds": False, "counterexample": "d-regular graph generation failed"}
            results.append(result)
    
    min_ranks = [r["metric_value"] for r in results if r["metric_value"] is not None]
    circuit_widths = [circuit_monotone_width_graph(generate_d_regular_graph(random.randint(5, 40), random.choice([5, 10, 15, 20, 30, 40]))) for _ in range(len(min_ranks))]
    
    if len(min_ranks) < 30:
        return {"seed": seed, "metric_name": "min_rank", "metric_value": None, "instances_tested": 0, "n_max": max([r["n_max"] for r in results]), "conjecture_holds": False, "counterexample": "not enough instances tested"}
    
    n = len(min_ranks)
    mean_min_rank = sum(min_ranks) / n
    mean_circuit_width = sum(circuit_widths) / n
    
    covariance = sum((min_ranks[i] - mean_min_rank) * (circuit_widths[i] - mean_circuit_width) for i in range(n)) / n
    variance_min_rank = sum((min_ranks[i] - mean_min_rank) ** 2 for i in range(n)) / n
    variance_circuit_width = sum((circuit_widths[i] - mean_circuit_width) ** 2 for i in range(n)) / n
    
    correlation_coefficient = covariance / (math.sqrt(variance_min_rank) * math.sqrt(variance_circuit_width))
    
    predicted_values = [correlation_coefficient * circuit_width + (mean_min_rank - correlation_coefficient * mean_circuit_width) for circuit_width in circuit_widths]
    mean_absolute_difference = sum(abs(predicted_values[i] - min_ranks[i]) for i in range(n)) / n
    
    return {"seed": seed, "metric_name": "min_rank", "metric_value": correlation_coefficient, "instances_tested": len(min_ranks), "n_max": max([r["n_max"] for r in results]), "conjecture_holds": abs(correlation_coefficient) >= 0.8 and mean_absolute_difference <= 3, "counterexample": ""}

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    min_ranks = [r["metric_value"] for r in results if r["metric_value"] is not None]
    circuit_widths = [circuit_monotone_width_graph(generate_d_regular_graph(random.randint(5, 40), random.choice([5, 10, 15, 20, 30, 40]))) for _ in range(len(min_ranks))]
    
    if len(min_ranks) < 30:
        print("RESULT: INCONCLUSIVE reason=not_enough_instances_tested n_tested=<k>")
    else:
        mean_min_rank = sum(min_ranks) / len(min_ranks)
        mean_circuit_width = sum(circuit_widths) / len(circuit_widths)
        
        covariance = sum((min_ranks[i] - mean_min_rank) * (circuit_widths[i] - mean_circuit_width) for i in range(len(min_ranks))) / len(min_ranks)
        variance_min_rank = sum((min_ranks[i] - mean_min_rank) ** 2 for i in range(len(min_ranks))) / len(min_ranks)
        variance_circuit_width = sum((circuit_widths[i] - mean_circuit_width) ** 2 for i in range(len(circuit_widths))) / len(circuit_widths)
        
        correlation_coefficient = covariance / (math.sqrt(variance_min_rank) * math.sqrt(variance_circuit_width))
        
        predicted_values = [correlation_coefficient * circuit_width + (mean_min_rank - correlation_coefficient * mean_circuit_width) for circuit_width in circuit_widths]
        mean_absolute_difference = sum(abs(predicted_values[i] - min_ranks[i]) for i in range(len(min_ranks))) / len(min_ranks)
        
        support_fraction = sum(1 for r in results if abs(r["metric_value"]) >= 0.8 and r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_correlation_coefficient} std={math.sqrt(variance_correlation_coefficient)} support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
            print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_threshold_not_met\" first_failing_seed={first_failing_seed}")