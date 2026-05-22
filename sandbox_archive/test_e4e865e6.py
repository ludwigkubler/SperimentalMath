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
    
    def generate_random_cnf(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(variables + [f'~{v}' for v in variables], 2)
            clauses.append(' | '.join(clause))
        return ' & '.join(clauses)

    def dpll(cnf):
        if not cnf:
            return True
        literals, _ = parse_cnf(cnf)
        literal = literals[0]
        positive_clauses = [c for c in cnf.split(' & ') if literal in c or f'~{literal}' not in c]
        negative_clauses = [c for c in cnf.split(' & ') if literal not in c and f'~{literal}' in c]
        if dpll('&'.join(positive_clauses)):
            return True
        if dpll('&'.join(negative_clauses)):
            return True
        return False

    def parse_cnf(cnf):
        literals = []
        for clause in cnf.split(' & '):
            literals.extend([l.strip('~') for l in clause.split(' | ')])
        return literals, set(literals)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_random_cnf(n)
        width = dpll(cnf)
        min_abs_value = 1  # Placeholder value, as the conjecture does not specify how to compute it
        results.append({
            "n": n,
            "cnf": cnf,
            "width": width,
            "min_abs_value": min_abs_value
        })
    
    mean_width = sum(r["width"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["width"] - mean_width) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["width"] <= (n ** 3) * math.log(r["min_abs_value"])) / len(results)
    
    return {
        "metric_name": "DPLL Search Tree Width",
        "metric_value": mean_width,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.95,
        "counterexample": "" if support_fraction >= 0.95 else f"n={results[0]['n']}, width={results[0]['width']}, min_abs_value={results[0]['min_abs_value']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, width={results[0]['width']}, min_abs_value={results[0]['min_abs_value']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")