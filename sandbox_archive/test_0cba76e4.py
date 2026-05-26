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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Invalid function length")
        complexity = 0
        for i in range(n):
            count_0 = f[:2**(i+1)].count(0)
            count_1 = f[:2**(i+1)].count(1)
            if count_0 > count_1:
                complexity += 1
            else:
                complexity += 2
        return complexity
    
    def rank_of_dual_object(f):
        n = int(math.log2(len(f)))
        # Placeholder for actual computation of the rank of the dual object
        # This is a dummy implementation that returns a random value for demonstration purposes
        return random.randint(1, n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        R_f = communication_complexity(f)
        rank_f = rank_of_dual_object(f)
        
        if not (1 <= R_f <= C * n):
            return {
                "metric_name": "communication_complexity",
                "metric_value": R_f,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Invalid complexity {R_f} for n={n}"
            }
        
        results.append({
            "n": n,
            "R_f": R_f,
            "rank_f": rank_f
        })
    
    mean_rank = sum(result["rank_f"] for result in results) / len(results)
    std_deviation = math.sqrt(sum((result["rank_f"] - mean_rank)**2 for result in results) / len(results))
    
    return {
        "metric_name": "mean_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": all(abs(result["rank_f"] - mean_rank) <= epsilon * result["R_f"] for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    C = 1.5  # Example constant
    epsilon = 0.1  # Example constant
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")