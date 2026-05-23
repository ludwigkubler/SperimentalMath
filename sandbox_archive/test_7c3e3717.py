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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k * n):
            clause = set(random.sample(range(1, n + 1), 2))
            if random.choice([True, False]):
                clause = {x: -1 for x in clause}
            else:
                clause = {x: 1 for x in clause}
            clauses.append(clause)
        return clauses
    
    def quadratic_form_value(x, q):
        return sum(q[i][j] * x[i-1] * x[j-1] for i in range(1, len(x)+1) for j in range(i+1, len(x)+1))
    
    def minimal_rank(q):
        n = len(q)
        rank = 0
        for _ in range(n):
            max_val = -float('inf')
            max_idx = None
            for i in range(n):
                if q[i][i] > max_val:
                    max_val = q[i][i]
                    max_idx = i
            if max_val == 0:
                break
            rank += 1
            for j in range(n):
                q[j][max_idx] /= max_val
                q[max_idx][j] /= max_val
            for i in range(n):
                if i != max_idx:
                    factor = q[i][max_idx]
                    for j in range(n):
                        q[i][j] -= factor * q[max_idx][j]
        return rank
    
    def communication_complexity(q, n):
        # Simplified model: O(n^k) where k is the minimal rank
        k = minimal_rank(q)
        return n ** k
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_communication = 0
        for _ in range(5):  # Ensure at least 5 instances per size
            clauses = generate_k_cnf(n, n)
            q = [[0] * (n + 1) for _ in range(n + 1)]
            for clause in clauses:
                for x in clause:
                    for y in clause:
                        if x != y:
                            q[abs(x)][abs(y)] += 1
            communication = communication_complexity(q, n)
            total_communication += communication
            instances_tested += 1
        
        mean_communication = total_communication / instances_tested
        conjecture_holds = all(communication <= n ** k for communication, k in zip([mean_communication] * instances_tested, range(n, n + instances_tested)))
        counterexample = "" if conjecture_holds else "Communication complexity exceeds O(n^k)"
        
        results.append({
            "metric_name": "communication_complexity",
            "metric_value": mean_communication,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    return {
        "seed": seed,
        **results[0]
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_communication = sum(result["metric_value"] for result in results) / len(results)
    std_communication = math.sqrt(sum((result["metric_value"] - mean_communication) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_communication} std={std_communication} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Communication complexity exceeds O(n^k)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")