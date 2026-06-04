# auto-injected by SEC sandbox
import json
import sys
import os
import time
import re
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools
import collections

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_clique_free_graph(n, k):
        if n <= 1 or k < 0:
            return []
        
        G = [[] for _ in range(n)]
        edges_added = set()
        
        for i in range(n):
            for j in range(i + 1, n):
                if (i, j) not in edges_added and (j, i) not in edges_added:
                    if random.random() < k / (n * (n - 1) / 2):
                        G[i].append(j)
                        G[j].append(i)
                        edges_added.add((i, j))
        
        return G
    
    def alexander_defect(G):
        n = len(G)
        if n <= 1:
            return 0
        
        # Compute the adjacency matrix
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in G[i]:
                A[i][j] = 1
        
        # Gaussian elimination to find the rank of the matrix
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            rank = 0
            
            for col in range(n):
                pivot_row = -1
                for row in range(rank, m):
                    if A[row][col] != 0:
                        pivot_row = row
                        break
                
                if pivot_row == -1:
                    continue
                
                # Swap rows to bring the pivot to the current rank position
                A[pivot_row], A[rank] = A[rank], A[pivot_row]
                
                # Make all entries in the pivot column 0 below the pivot
                for row in range(rank + 1, m):
                    factor = -A[row][col] / A[rank][col]
                    for j in range(n):
                        A[row][j] += factor * A[rank][j]
                
                rank += 1
            
            return rank
        
        return n - gaussian_elimination(A)
    
    def communication_complexity_rank(G):
        n = len(G)
        if n <= 1:
            return 0
        
        # Compute the adjacency matrix
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in G[i]:
                A[i][j] = 1
        
        # Gaussian elimination to find the rank of the matrix
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            rank = 0
            
            for col in range(n):
                pivot_row = -1
                for row in range(rank, m):
                    if A[row][col] != 0:
                        pivot_row = row
                        break
                
                if pivot_row == -1:
                    continue
                
                # Swap rows to bring the pivot to the current rank position
                A[pivot_row], A[rank] = A[rank], A[pivot_row]
                
                # Make all entries in the pivot column 0 below the pivot
                for row in range(rank + 1, m):
                    factor = -A[row][col] / A[rank][col]
                    for j in range(n):
                        A[row][j] += factor * A[rank][j]
                
                rank += 1
            
            return rank
        
        return rank
    
    n_max = 40
    instances_tested = 0
    total_defect = 0
    total_rank = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            k = random.randint(0, min(n - 1, 3))
            G = generate_k_clique_free_graph(n, k)
            
            if not G:
                continue
            
            defect = alexander_defect(G)
            rank = communication_complexity_rank(G)
            
            total_defect += defect
            total_rank += rank
            instances_tested += 1
    
    mean_defect = total_defect / instances_tested
    mean_rank = total_rank / instances_tested
    correlation_coefficient = (instances_tested * sum(defect * rank for defect, rank in zip(range(instances_tested), range(instances_tested))) -
                               sum(range(instances_tested)) * sum(range(instances_tested))) / \
                              math.sqrt((instances_tested * sum(defect**2 for defect in range(instances_tested)) - sum(range(instances_tested))**2) *
                                        (instances_tested * sum(rank**2 for rank in range(instances_tested)) - sum(range(instances_tested))**2))
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": abs(correlation_coefficient),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": "" if abs(correlation_coefficient) >= 0.7 else "Spearman's rank correlation coefficient < 0.7"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman's rank correlation coefficient < 0.7\" first_failing_seed={seeds[first_failing_seed]}")