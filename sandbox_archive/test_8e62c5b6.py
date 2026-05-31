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
    
    def communication_complexity(f):
        n = len(f)
        max_comm_cost = 0
        for i in range(1 << (n - 1)):
            prefix = f[:i]
            suffix = f[i:]
            comm_cost = sum(1 for x, y in zip(prefix, suffix) if x != y)
            max_comm_cost = max(max_comm_cost, comm_cost)
        return max_comm_cost
    
    def coxeter_diagram(f):
        n = len(f)
        relations = set()
        for i in range(n):
            for j in range(i + 1, n):
                if f[i] != f[j]:
                    relations.add((i, j))
        return relations
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_relations = 0
        
        while instances_tested < 30:
            f = generate_boolean_function(n)
            C_f = communication_complexity(f)
            R_f = coxeter_diagram(f)
            
            if len(R_f) > 100:  # Skip very large diagrams
                continue
            
            total_relations += len(R_f)
            instances_tested += 1
        
        mean_relations_per_instance = Fraction(total_relations, instances_tested)
        ratio = mean_relations_per_instance / math.log(n)
        
        results.append({
            "n": n,
            "mean_relations_per_instance": mean_relations_per_instance,
            "ratio": ratio
        })
    
    if not results:
        return {
            "metric_name": "Ratio of relations to log(n)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    n_max = max(result["n"] for result in results)
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["ratio"] - mean_ratio)**2 for result in results) / len(results))
    
    if any(result["ratio"] > 10 for result in results):  # Arbitrary threshold
        return {
            "metric_name": "Ratio of relations to log(n)",
            "metric_value": mean_ratio,
            "instances_tested": sum(1 for result in results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": f"Ratio exceeded 10 at n={max(result['n'] for result in results if result['ratio'] > 10)}"
        }
    
    return {
        "metric_name": "Ratio of relations to log(n)",
        "metric_value": mean_ratio,
        "instances_tested": sum(1 for result in results),
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, {result}}}")
        results.append(result)
    
    mean_ratio = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeded 10\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=No valid instances generated")