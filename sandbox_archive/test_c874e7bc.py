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
    
    def shannon_entropy(p):
        return -sum(x * math.log2(x) for x in p if x > 0)

    def renyi_entropy(p, alpha):
        return (1 / (1 - alpha)) * math.log(sum(x**alpha for x in p), 2)

    def generate_kcnf(n, m, k):
        clauses = []
        for _ in range(m):
            clause = random.sample(range(1, n + 1), k)
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def count_satisfying_assignments(instance):
        n = len(instance[0])
        count = 0
        for assignment in range(2**n):
            satisfying = True
            for clause in instance:
                if all((assignment >> (var - 1)) & 1 == abs(lit) % 2 != lit < 0 for lit in clause):
                    continue
                else:
                    satisfying = False
                    break
            if satisfying:
                count += 1
        return count

    def monotone_circuit_size(n, k):
        # This is a placeholder function. In practice, you would need to implement
        # an algorithm to find the size of a monotone circuit for a given instance.
        return k**n

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Test each size with 5 instances
            m = random.randint(n // 2, n * 2)
            k = random.randint(1, min(n, 5))
            instance = generate_kcnf(n, m, k)
            
            satisfying_count = count_satisfying_assignments(instance)
            probabilities = [satisfying_count / (2**n), 1 - satisfying_count / (2**n)]
            entropy = shannon_entropy(probabilities)
            
            circuit_size = monotone_circuit_size(n, k)
            
            results.append({
                "metric_name": "entropic_complexity",
                "metric_value": entropy,
                "instances_tested": 1,
                "conjecture_holds": entropy <= f(n, k),
                "counterexample": "" if entropy <= f(n, k) else f"Instance with n={n}, m={m}, k={k} has E(I) > f(n,k)"
            })
    
    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    std_entropy = math.sqrt(sum((r["metric_value"] - mean_entropy)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_entropy": mean_entropy,
        "std_entropy": std_entropy,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(r["mean_entropy"] for r in results) / len(results)
    std_entropy = math.sqrt(sum((r["mean_entropy"] - mean_entropy)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["support_fraction"] >= 0.8) / len(results)
    
    if support_fraction == 1:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")