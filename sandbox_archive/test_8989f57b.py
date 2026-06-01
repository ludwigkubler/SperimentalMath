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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(2, n))]
            clauses.append(clause)
        return clauses
    
    def frege_proof_size(cnf):
        # Simplified Frege proof size calculation
        return sum(len(clause) for clause in cnf)
    
    def quadratic_residues(cnf):
        residues = set()
        for clause in cnf:
            for literal in clause:
                if literal % 2 == 0:
                    residues.add(literal // 2)
        return residues
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        cnf = generate_cnf(random.randint(5, n_max))
        Q_phi = quadratic_residues(cnf)
        w_phi = frege_proof_size(cnf)
        
        if len(Q_phi) == 0 or w_phi == 0:
            continue
        
        metric_values.append((len(Q_phi), w_phi))
    
    if not metric_values:
        return {
            "metric_name": "Q(φ)",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    Q_values, w_values = zip(*metric_values)
    mean_Q = sum(Q_values) / len(Q_values)
    mean_w = sum(w_values) / len(w_values)
    abs_diffs = [abs(q - w) for q, w in zip(Q_values, w_values)]
    mean_abs_diff = sum(abs_diffs) / len(abs_diffs)
    
    return {
        "metric_name": "Q(φ)",
        "metric_value": mean_Q,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": all(diff <= 3 for diff in abs_diffs),
        "counterexample": "" if all(diff <= 3 for diff in abs_diffs) else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r['conjecture_holds'] for r in results):
        mean_Q = sum(r['metric_value'] for r in results) / len(results)
        std_Q = (sum((r['metric_value'] - mean_Q) ** 2 for r in results) / len(results)) ** 0.5
        support_fraction = Fraction(len([r for r in results if r['conjecture_holds']]), len(results))
        print(f"RESULT: SUPPORTED mean={mean_Q} std={std_Q} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")