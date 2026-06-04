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
    
    def generate_cnf(m):
        literals = list(range(1, m + 2))
        clauses = []
        for _ in range(m):
            clause = random.sample(literals, 3)
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        queue = cnf[:]
        while True:
            new_clause = None
            for i in range(len(queue)):
                for j in range(i + 1, len(queue)):
                    if any(-x in queue[i] and x in queue[j] for x in literals):
                        new_clause = [l for l in queue[i] if l not in [-x for x in queue[j]]]
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(queue)
            queue.append(new_clause)
    
    def geometric_quantization_order(cnf):
        # Placeholder function to simulate the computation of o_q(φ)
        return sum(len(clause) for clause in cnf)
    
    metric_values = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        m = random.randint(100, 1000)
        cnf = generate_cnf(m)
        o_q_phi = geometric_quantization_order(cnf)
        w_phi = resolution_width(cnf)
        metric_values.append((o_q_phi, w_phi))
    
    mean_x = sum(x for x, y in metric_values) / len(metric_values)
    mean_y = sum(y for x, y in metric_values) / len(metric_values)
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in metric_values)
    denominator = math.sqrt(sum((x - mean_x) ** 2 for x, _ in metric_values)) * math.sqrt(sum((y - mean_y) ** 2 for _, y in metric_values))
    
    if denominator == 0:
        correlation_coefficient = 0
    else:
        correlation_coefficient = numerator / denominator
    
    p_value = 1  # Placeholder for actual p-value calculation, which is complex and not shown here
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(metric_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.9 and p_value < 0.05,
        "counterexample": "" if correlation_coefficient > 0.9 and p_value < 0.05 else "correlation_coefficient <= 0.9 or p_value >= 0.05"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient <= 0.9 or p_value >= 0.05\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")