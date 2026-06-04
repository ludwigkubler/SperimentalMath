# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, m), -random.randint(1, m)]
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        # Simplified resolution width calculation
        seen_clauses = set()
        while True:
            new_clause = None
            for clause in cnf:
                if len(clause) == 1:
                    return len(seen_clauses)
                for lit in clause:
                    if -lit in seen_clauses:
                        new_clause = [l for l in clause if l != lit and -l not in clause]
                        break
                if new_clause is not None:
                    break
            if new_clause is None:
                return len(seen_clauses)
            seen_clauses.add(tuple(sorted(new_clause)))
    
    def geometric_quantization_order(cnf):
        # Simplified geometric quantization order calculation
        return len(cnf) ** 0.5
    
    instances_tested = 0
    n_max = 1
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for m in [5, 10, 15, 20, 30, 40]:
        cnf = generate_cnf(m)
        w_phi = resolution_width(cnf)
        o_q_phi = geometric_quantization_order(cnf)
        
        instances_tested += 1
        n_max = max(n_max, m)
        metric_values.append((o_q_phi, w_phi))
    
    if len(metric_values) < 30:
        conjecture_holds = False
        counterexample = "insufficient_instances"
    
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in metric_values)
    correlation_coefficient /= (len(metric_values) * sum((x - mean_x) ** 2 for x, _ in metric_values) * sum((y - mean_y) ** 2 for _, y in metric_values)) ** 0.5
    p_value = 1  # Placeholder for actual p-value calculation
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"m={r['n_max']}, o_q(φ)={r['metric_value'][0]}, w(φ)={r['metric_value'][1]}"
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(r)]}")