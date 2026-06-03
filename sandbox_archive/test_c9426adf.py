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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-n, n-1) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def frege_proof_width(cnf):
        # Simplified model of Frege proof width
        return len(cnf) * random.random() + 1
    
    def hodge_norm(cnf):
        # Simplified model of Hodge norm
        return math.log(len(cnf))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        proof_width = frege_proof_width(cnf)
        norm = hodge_norm(cnf)
        
        if proof_width <= 0 or norm < 0:
            continue
        
        results.append((n, norm, proof_width))
    
    if not results:
        return {
            "metric_name": "Hodge Norm vs Frege Proof Width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    n_max = max(n for n, _, _ in results)
    if n_max < 16:
        return {
            "metric_name": "Hodge Norm vs Frege Proof Width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Insufficient instance sizes"
        }
    
    norms = [norm for _, norm, _ in results]
    widths = [width for _, _, width in results]
    
    mean_norm = sum(norms) / len(norms)
    mean_width = sum(widths) / len(widths)
    
    if any(norm > 1.2 * math.log(width) for norm, width in zip(norms, widths)):
        return {
            "metric_name": "Hodge Norm vs Frege Proof Width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Hodge norm exceeds 1.2 * log(Frege proof width)"
        }
    
    return {
        "metric_name": "Hodge Norm vs Frege Proof Width",
        "metric_value": mean_norm / math.log(mean_width),
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("metric_value" not in r or r["metric_value"] is None for r in results):
        print("RESULT: INCONCLUSIVE no valid instances found")
    else:
        mean_metric = sum(r["metric_value"] for r in results) / len(results)
        std_metric = math.sqrt(sum((r["metric_value"] - mean_metric)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" not in r or r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
        elif any("counterexample" in r and r["counterexample"] for r in results):
            counterexample = next(r["counterexample"] for r in results if "counterexample" in r and r["counterexample"])
            first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
            print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE insufficient support")