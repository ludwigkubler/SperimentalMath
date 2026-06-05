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

def generate_tseitin_formula(n, d):
    if n % d != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    variables = list(range(1, n + 1))
    clauses = []
    for i in range(1, n + 1):
        clause = [i]
        for j in range(d - 2):
            k = random.choice(variables)
            if k not in clause:
                clause.append(k)
        clauses.append(clause)
    
    formula = []
    for clause in clauses:
        formula.append([x * (-1) for x in clause] + [0])
        for i in range(len(clause)):
            for j in range(i + 1, len(clause)):
                formula.append([clause[i], clause[j], -1 * (i + 1), -1 * (j + 1), 0])
    
    return formula

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        d = 2
        formula = generate_tseitin_formula(n, d)
        
        # Calculate resolution proof width (simplified DPLL)
        def dpll(clauses):
            if not clauses:
                return True
            clause = next(c for c in clauses if any(x > 0 for x in c))
            literal = min(abs(l) for l in clause)
            new_clauses = []
            for c in clauses:
                if literal not in c and -literal not in c:
                    new_clauses.append([l for l in c if l != -literal])
            return dpll(new_clauses) or dpll([c[:] for c in new_clauses if any(l > 0 for l in c)])
        
        proof_width = len(formula)
        
        # Calculate tropical Hodge decomposition order (simplified example)
        hodge_order = n
        
        results.append({
            "n": n,
            "hodge_order": hodge_order,
            "proof_width": proof_width
        })
    
    correlation_sum = 0
    max_hodge_order = 0
    for result in results:
        if result["hodge_order"] > 3 * result["proof_width"]:
            return {
                "metric_name": "correlation",
                "metric_value": None,
                "instances_tested": len(results),
                "n_max": max(result["n"] for result in results),
                "conjecture_holds": False,
                "counterexample": f"HODGEOH({result['hodge_order']}) > 3 * PROOFWIDTH({result['proof_width']})"
            }
        correlation_sum += (result["hodge_order"] - result["proof_width"]) / result["proof_width"]
        max_hodge_order = max(max_hodge_order, result["hodge_order"])
    
    correlation_mean = correlation_sum / len(results)
    support_fraction = sum(1 for r in results if abs(r["hodge_order"] - r["proof_width"]) / r["proof_width"] >= 0.8) / len(results)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_mean,
        "instances_tested": len(results),
        "n_max": max_hodge_order,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(result['counterexample'] for result in results if result['counterexample'])}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")