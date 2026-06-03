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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_max_cut_instance(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    def find_min_moves(G):
        n = len(G)
        dist = [[math.inf] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
        
        # Floyd-Warshall algorithm to compute shortest paths
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        
        min_moves = 0
        for u in range(n):
            for v in range(u+1, n):
                if G[u][v] == 1 and dist[u][v] > 2:
                    min_moves += 1
        return min_moves
    
    def communication_matrix_rank(G):
        n = len(G)
        R = [[0] * n for _ in range(n)]
        
        # Compute the adjacency matrix of the graph
        for i in range(n):
            for j in range(i+1, n):
                if G[i][j] == 1:
                    R[i][j] = 1
                    R[j][i] = 1
        
        # Gaussian elimination to find the rank
        rank = n
        for i in range(n):
            if R[i][i] == 0:
                found = False
                for j in range(i+1, n):
                    if R[j][i] != 0:
                        for k in range(n):
                            R[i][k], R[j][k] = R[j][k], R[i][k]
                        found = True
                        break
                if not found:
                    rank -= 1
                    continue
            
            pivot = Fraction(R[i][i])
            for j in range(i, n):
                R[i][j] /= pivot
        
            for j in range(n):
                if j != i and R[j][i] != 0:
                    factor = -R[j][i]
                    for k in range(n):
                        R[j][k] += factor * R[i][k]
        
        return rank
    
    def max_cut_to_graph(instance):
        n = len(instance)
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if instance[i] != instance[j]:
                    G[i][j] = 1
                    G[j][i] = 1
        return G
    
    n_max = 40
    instances_tested = 30
    total_metric_value = 0.0
    counterexamples = []
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        instance = generate_max_cut_instance(n)
        G = max_cut_to_graph(instance)
        
        alpha_n = find_min_moves(G)
        k_n = communication_matrix_rank(G)
        
        if k_n > alpha_n**2 * 1.1:
            counterexamples.append(f"n={n}, alpha_n={alpha_n}, k_n={k_n}")
        
        total_metric_value += k_n
    
    metric_name = "communication_matrix_rank"
    metric_value = total_metric_value / instances_tested
    conjecture_holds = len(counterexamples) == 0
    counterexample = ", ".join(counterexamples)
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(len(r["counterexample"]) > 0 for r in results):
        counterexamples = [r["counterexample"] for r in results if len(r["counterexample"]) > 0]
        print(f"RESULT: FALSIFIED counterexample=\"{' '.join(counterexamples)}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested=30")