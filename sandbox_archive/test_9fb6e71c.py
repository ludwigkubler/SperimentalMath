# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import combinations

# Function to generate a random planar graph with n nodes
def generate_planar_graph(n):
    if n < 3:
        raise ValueError("Graph must have at least 3 nodes")
    
    # Generate a random tree as the base of the planar graph
    G = {i: [] for i in range(n)}
    edges = []
    for i in range(1, n):
        u = random.randint(0, i-1)
        v = i
        G[u].append(v)
        G[v].append(u)
        edges.append((u, v))
    
    # Add additional edges to make the graph planar
    while len(edges) < 3 * n - 6:
        u, v = random.sample(range(n), 2)
        if (u, v) not in edges and (v, u) not in edges:
            G[u].append(v)
            G[v].append(u)
            edges.append((u, v))
    
    return G

# Function to calculate the minimal diophantine degree (dd(G)) using LLL reduction
def lll_reduction(matrix):
    m = len(matrix)
    n = len(matrix[0])
    B = [list(row) for row in matrix]
    U = [[1 if i == j else 0 for j in range(n)] for i in range(m)]
    
    def gram_schmidt(B, U):
        for k in range(1, m):
            B[k] = [B[k][j] - sum(U[i][j] * B[i][k] for i in range(k)) for j in range(n)]
            norm_squared = sum(B[k][j]**2 for j in range(n))
            U[k][k] = Fraction(norm_squared).sqrt()
            for j in range(k):
                U[j][k] = Fraction(sum(U[j][i] * B[i][k] for i in range(j+1, k+1)), U[j][j])
                B[j][k] = [B[j][k] - sum(U[j][i] * B[i][k] for i in range(j+1, k+1)) for _ in range(n)]
    
    def size_reduction(B, U):
        for k in range(m-1, 0, -1):
            for j in range(k-1, -1, -1):
                a = Fraction(U[j][k]).floor()
                if abs(a) > 1/2:
                    B[j] = [B[j][i] - a * B[k][i] for i in range(n)]
                    U[j] = [U[j][i] - a * U[k][i] for i in range(m)]
    
    gram_schmidt(B, U)
    size_reduction(B, U)
    
    dd = sum(sum(abs(b[i]) for b in B) for i in range(n))
    return dd

# Function to calculate the communication complexity growth rate (ccr(G))
def communication_complexity_growth_rate(G):
    n = len(G)
    nodes = list(G.keys())
    edges = [(u, v) for u, neighbors in G.items() for v in neighbors if u < v]
    
    # Calculate the communication rank of the graph
    communication_rank = 0
    for node in nodes:
        neighbors = set(G[node])
        for other_node in nodes:
            if other_node != node and not neighbors.intersection(set(G[other_node])):
                communication_rank += 1
    
    ccr = Fraction(communication_rank, n * (n - 1))
    return ccr

# Function to run one trial with a given seed
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a variety of planar graphs G with varying complexities
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        try:
            G = generate_planar_graph(n)
            dd_G = lll_reduction(G)
            ccr_G = communication_complexity_growth_rate(G)
            results.append((dd_G, ccr_G))
        except ValueError as e:
            return {
                "metric_name": "minimal_diophantine_degree",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": str(e)
            }
    
    # Compute the correlation coefficient between dd(G) and ccr(G)
    dd_values = [dd for dd, _ in results]
    ccr_values = [ccr for _, ccr in results]
    n = len(dd_values)
    
    mean_dd = sum(dd_values) / n
    mean_ccr = sum(ccr_values) / n
    
    covariance = sum((dd - mean_dd) * (ccr - mean_ccr) for dd, ccr in results)
    variance_dd = sum((dd - mean_dd)**2 for dd in dd_values)
    variance_ccr = sum((ccr - mean_ccr)**2 for ccr in ccr_values)
    
    if variance_dd == 0 or variance_ccr == 0:
        return {
            "metric_name": "minimal_diophantine_degree",
            "metric_value": None,
            "instances_tested": n,
            "n_max": max(n),
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    correlation_coefficient = covariance / (variance_dd * variance_ccr)**0.5
    
    return {
        "metric_name": "minimal_diophantine_degree",
        "metric_value": correlation_coefficient,
        "instances_tested": n,
        "n_max": max(n),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and correlation_coefficient > 0,
        "counterexample": ""
    }

# Main function to run multiple trials with different seeds
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        seeds = [int(seed) for seed in sys.argv[1:]]
    else:
        # Default list of 30 prime numbers as seeds
        seeds = [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
            31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
            73, 79, 83, 89, 97, 101, 103, 107, 109, 113
        ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, {trial_result}}}")
        results.append(trial_result)
    
    # Compute mean and standard deviation of metric_value
    if all("metric_value" in result and result["metric_value"] is not None for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = (sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))**0.5
    else:
        mean_metric_value = None
        std_metric_value = None
    
    # Compute fraction of seeds where conjecture_holds
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    # Determine the final result based on the acceptance criterion
    if all("metric_value" in result and result["metric_value"] is not None for result in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE metric_value_not_computed")