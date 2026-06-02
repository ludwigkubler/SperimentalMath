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
    
    def geometric_entropy(proof):
        explored = set()
        for clause in proof:
            if tuple(clause) not in explored:
                explored.add(tuple(clause))
        return math.log(len(explored), 2)

    def generate_frege_proof(width, depth):
        proof = []
        variables = list(range(1, width + 1))
        for _ in range(depth):
            clause = random.sample(variables, k=random.randint(1, width))
            proof.append(clause)
        return proof

    n_max = 0
    instances_tested = 0
    total_entropy = 0.0
    max_width = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        width = random.randint(1, n)
        depth = random.randint(1, n * 2)
        proof = generate_frege_proof(width, depth)
        entropy = geometric_entropy(proof)
        total_entropy += entropy
        instances_tested += 1
    
    mean_entropy = total_entropy / instances_tested
    conjecture_holds = False
    counterexample = ""
    
    if n_max >= 16:
        # Check the correlation coefficient
        width_values = [random.randint(1, n) for _ in range(instances_tested)]
        entropy_values = [geometric_entropy(generate_frege_proof(w, random.randint(1, w * 2))) for w in width_values]
        
        if len(width_values) > 1:
            mean_width = sum(width_values) / len(width_values)
            mean_entropy = sum(entropy_values) / len(entropy_values)
            
            covariance = sum((w - mean_width) * (e - mean_entropy) for w, e in zip(width_values, entropy_values))
            variance_width = sum((w - mean_width) ** 2 for w in width_values)
            variance_entropy = sum((e - mean_entropy) ** 2 for e in entropy_values)
            
            if variance_width > 0 and variance_entropy > 0:
                correlation_coefficient = covariance / (math.sqrt(variance_width) * math.sqrt(variance_entropy))
                
                if correlation_coefficient >= 0.8:
                    conjecture_holds = True
                else:
                    counterexample = f"Correlation coefficient {correlation_coefficient} < 0.8"
            else:
                counterexample = "Variance is zero, cannot compute correlation coefficient"
        else:
            counterexample = "Not enough data points to compute correlation coefficient"
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": mean_entropy,
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
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_entropy) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample_desc = "Correlation coefficient < 0.8"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")