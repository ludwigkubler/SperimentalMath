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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if random.random() < 0.5:
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def truth_table_entropy(clauses):
        n = len(clauses[0])
        counts = [0] * (2**n)
        for clause in clauses:
            index = sum(1 << i if c > 0 else -(1 << i) for i, c in enumerate(clause))
            counts[index] += 1
        total = sum(counts)
        entropy = -sum(c / total * math.log2(c / total) for c in counts if c > 0)
        return entropy
    
    def diophantine_approximation(entropy):
        # Simplified approximation method (not rigorous)
        return entropy * 100
    
    n_values = [10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        clauses = generate_3cnf(n)
        entropy = truth_table_entropy(clauses)
        approx_index = diophantine_approximation(entropy)
        
        if approx_index > n * math.log2(n):
            return {
                "metric_name": "Diophantine Index",
                "metric_value": approx_index,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, entropy={entropy}, approx_index={approx_index}"
            }
    
    return {
        "metric_name": "Diophantine Index",
        "metric_value": sum(diophantine_approximation(truth_table_entropy(generate_3cnf(n))) for n in n_values) / len(n_values),
        "instances_tested": 5,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")