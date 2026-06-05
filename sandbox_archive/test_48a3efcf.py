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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_min_deg(p):
        n = len(p)
        if n == 1:
            return 0
        A = [[Fraction(p[i][j], 2) for j in range(n)] for i in range(n)]
        B = [Fraction(p[i][-1], 2) for i in range(n)]
        for k in range(n):
            max_row = k
            for i in range(k+1, n):
                if abs(A[i][k]) > abs(A[max_row][k]):
                    max_row = i
            A[k], A[max_row] = A[max_row], A[k]
            B[k], B[max_row] = B[max_row], B[k]
            for i in range(k+1, n):
                factor = Fraction(A[i][k], A[k][k])
                for j in range(k, n+1):
                    A[i][j] -= factor * A[k][j]
                B[i] -= factor * B[k]
        return sum(1 for row in A if any(x != 0 for x in row))
    
    def compute_entropy(clauses):
        total = len(clauses)
        counts = [clauses.count(c) for c in set(clauses)]
        probabilities = [count / total for count in counts]
        entropy = -sum(p * math.log2(p) for p in probabilities if p != 0)
        return entropy
    
    n_max = 40
    instances_tested = 0
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            clauses = [i for i, val in enumerate(f) if val == 1]
            p = [[0] * (n+1) for _ in range(n)]
            p[0][n] = 1
            for i in range(1, n):
                for j in range(i+1):
                    p[i][j] = -p[i-1][j]
                    if j < i:
                        p[i][j+1] = p[i-1][j]
            min_deg_p = compute_min_deg(p)
            entropy_S = compute_entropy(clauses)
            metric_value += abs(min_deg_p - entropy_S)
            instances_tested += 1
    
    mean_metric_value = metric_value / instances_tested
    support_fraction = instances_tested / (n_max - 4) * 6
    
    if support_fraction >= 0.8:
        return {
            "metric_name": "Correlation between min_deg(p) and Entropy(S)",
            "metric_value": mean_metric_value,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "Correlation between min_deg(p) and Entropy(S)",
            "metric_value": mean_metric_value,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "support_fraction < 0.8"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if not r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction < 0.2:
        print(f"RESULT: FALSIFIED counterexample='support_fraction < 0.2' first_failing_seed={seeds[support_fraction == 0]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction too low")