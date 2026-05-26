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
    
    def generate_boolean_function(n):
        return ''.join(random.choice('01') for _ in range(2**n - 1))
    
    def tseitin_circuit(f):
        n = len(f)
        literals = list(range(n))
        clauses = []
        
        # Implication rules
        for i in range(n):
            clauses.append([literals[i], literals[n + i]])
            clauses.append([-literals[i], -literals[n + i]])
        
        # OR rules
        for j in range(2**n - 1):
            clause = []
            for k in range(n):
                if f[j] & (1 << k):
                    clause.append(literals[k])
                else:
                    clause.append(-literals[k])
            clauses.append(clause)
        
        return clauses
    
    def frege_proof_width(clauses):
        n = len(clauses)
        width = 0
        for i in range(n):
            width = max(width, len(clauses[i]))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        circuit = tseitin_circuit(f)
        proof_width = frege_proof_width(circuit)
        
        if proof_width == 0:
            continue
        
        results.append(proof_width)
    
    if not results:
        return {
            "metric_name": "Frege Proof Width",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if abs(x - math.log(len(results))) < 0.1 * math.log(len(results))) / len(results)
    
    return {
        "metric_name": "Frege Proof Width",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" not in result or result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_deviation = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if "conjecture_holds" not in result or result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_deviation} support_fraction={support_fraction}")
    elif any("counterexample" in result and result["counterexample"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result and result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")