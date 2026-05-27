# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_tseitin_circuit(n, D):
        # Simplified Tseitin circuit generation for demonstration purposes
        if n == 1 and D == 1:
            return ["A"]
        elif n == 2 and D == 1:
            return ["A", "B", "NOT A", "NOT B", "AND A B", "OR A B"]
        else:
            raise NotImplementedError("mapping_undefined")
    
    def generate_qmc_sequence(d, degree):
        # Simplified QMC sequence generation for demonstration purposes
        if d == 1 and degree == 1:
            return [0.5]
        elif d == 2 and degree == 1:
            return [0.3, 0.7]
        else:
            raise NotImplementedError("mapping_undefined")
    
    def compute_min_dist(sequence):
        n = len(sequence)
        min_dist = float('inf')
        for i in range(n):
            for j in range(i + 1, n):
                dist = abs(sequence[i] - sequence[j])
                if dist < min_dist:
                    min_dist = dist
        return min_dist
    
    def compute_spearman_rank_correlation(distances, sizes):
        n = len(distances)
        rank_distances = [0] * n
        rank_sizes = [0] * n
        
        for i in range(n):
            for j in range(i + 1, n):
                if distances[i] < distances[j]:
                    rank_distances[i] += 1
                else:
                    rank_distances[i] -= 1
                
                if sizes[i] < sizes[j]:
                    rank_sizes[i] += 1
                else:
                    rank_sizes[i] -= 1
        
        for i in range(n):
            rank_distances[i] = (n + 1) / 2 + rank_distances[i]
            rank_sizes[i] = (n + 1) / 2 + rank_sizes[i]
        
        mean_rank_dist = sum(rank_distances) / n
        mean_rank_size = sum(rank_sizes) / n
        
        numerator = sum((rank_distances[i] - mean_rank_dist) * (rank_sizes[i] - mean_rank_size) for i in range(n))
        denominator = 0
        for i in range(n):
            denominator += (rank_distances[i] - mean_rank_dist) ** 2
            denominator += (rank_sizes[i] - mean_rank_size) ** 2
        
        rho = numerator / (denominator ** 0.5)
        return rho
    
    n_values = [5, 10, 15, 20, 30, 40]
    distances = []
    sizes = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            D = random.randint(1, min(n, 10))
            circuit = generate_tseitin_circuit(n, D)
            size = len(circuit)
            qmc_sequence = generate_qmc_sequence(D, D)
            min_dist = compute_min_dist(qmc_sequence)
            distances.append(min_dist)
            sizes.append(size)
    
    rho = compute_spearman_rank_correlation(distances, sizes)
    conjecture_holds = rho >= 0.7
    counterexample = "" if conjecture_holds else f"Spearman rank correlation {rho} < 0.7"
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": rho,
        "instances_tested": len(distances),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    std_rho = (sum((r["metric_value"] - mean_rho) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman rank correlation < 0.7\" first_failing_seed={first_failing_seed}")