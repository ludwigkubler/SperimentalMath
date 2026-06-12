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
    
    def generate_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2**n - 1):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(' OR '.join(clause))
        return ' AND '.join(clauses)
    
    def p_adic_log(x, p):
        if x <= 0:
            return None
        count = 0
        while x % p == 0:
            x //= p
            count += 1
        return -count
    
    def resolution_width(phi):
        # Simplified DPLL solver to estimate width (not accurate but sufficient for testing)
        clauses = phi.split(' AND ')
        queue = [c.split(' OR ') for c in clauses]
        while queue:
            clause = queue.pop()
            if not clause:
                return len(clauses) - 1
            literal = random.choice(clause)
            if literal.startswith('x'):
                neg_literal = 'NOT ' + literal
            else:
                neg_literal = literal.replace('NOT ', '')
            for i, c in enumerate(queue):
                if neg_literal in c:
                    queue[i] = [l for l in c if l != neg_literal]
        return len(clauses) - 1
    
    def mrd(phi):
        clauses = phi.split(' AND ')
        indicators = [0] * (2**len(variables))
        for i, clause in enumerate(clauses):
            indicator = sum(1 << int(l[2:]) if l.startswith('x') else 0 for l in clause.split(' OR '))
            indicators[i] = indicator
        min_distance = float('inf')
        for i in range(len(indicators)):
            for j in range(i + 1, len(indicators)):
                distance = abs(indicators[i] - indicators[j])
                if distance < min_distance:
                    min_distance = distance
        return p_adic_log(min_distance, 2)
    
    n_max = 0
    metric_values = []
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        phi = generate_formula(n)
        mrd_phi = mrd(phi)
        w_phi = resolution_width(phi)
        
        if mrd_phi is not None and w_phi is not None:
            metric_values.append(mrd_phi / math.log(w_phi))
            instances_tested += 1
            n_max = max(n_max, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "mrd/w(log)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "mrd/w(log)",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": 0.7 <= mean <= 1.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")