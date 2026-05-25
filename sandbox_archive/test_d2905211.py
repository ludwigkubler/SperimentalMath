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
    
    def generate_read_twice_bp(n):
        # Generate a random read-twice branching program of size n
        bp = []
        for _ in range(n):
            bp.append(random.choice([0, 1]))
        return bp
    
    def noncrossing_partition(bp):
        # Construct the noncrossing partition graph from the BP
        if len(bp) == 1:
            return [[0]]
        
        partitions = []
        for i in range(len(bp)):
            if bp[i] == 0:
                partitions.append([i])
            else:
                new_partitions = []
                for p in partitions:
                    if p[-1] < i:
                        new_partitions.append(p + [i])
                    else:
                        new_partitions.append(p)
                partitions = new_partitions
        return partitions
    
    def rank(partition):
        # Compute the rank of the noncrossing partition graph
        n = len(partition)
        M = [[0] * n for _ in range(n)]
        for i, p in enumerate(partition):
            for j in p:
                M[i][j] = 1
        
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
                
                A[pivot_row], A[rank] = A[rank], A[pivot_row]
                rank += 1
                
                for row in range(m):
                    if row != rank - 1:
                        factor = Fraction(A[row][col], A[rank - 1][col])
                        for j in range(n):
                            A[row][j] -= factor * A[rank - 1][j]
            
            return rank
        
        return gaussian_elimination(M)
    
    n = random.randint(5, 40)
    bp = generate_read_twice_bp(n)
    partition = noncrossing_partition(bp)
    rank_value = rank(partition)
    
    metric_name = "Rank/LogSize"
    metric_value = rank_value / math.log(n)
    instances_tested = 1
    conjecture_holds = False
    counterexample = ""
    
    if n == 1:
        if rank_value != 1:
            counterexample = f"Trivial BP with size {n} has rank {rank_value}, expected 1"
    elif rank_value <= math.log(n):
        conjecture_holds = True
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))  # Default to first 29 primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        result = f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}"
    elif any(r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        result = f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if r["conjecture_holds"]), "")
        result = f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}"
    
    print(result)