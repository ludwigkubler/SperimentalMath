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
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, 2*m), -random.randint(1, 2*m)]
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        queue = set()
        for lit in set(x for clause in cnf for x in clause):
            queue.add(frozenset([lit]))
        
        while len(queue) > 0:
            i, j = random.sample(list(queue), 2)
            if i.intersection(j):
                new_lit = -i.intersection(j).pop()
                if not any(new_lit == -x for x in queue):
                    queue.add(frozenset([new_lit]))
            else:
                return len(queue)
        return len(queue)
    
    def geometric_quantization_order(cnf):
        # Placeholder function to simulate the computation
        # This is a dummy implementation and should be replaced with actual arithmetic geometry logic
        return random.randint(1, 10) * len(cnf)
    
    m_values = [100, 200, 300, 400, 500]
    o_q_values = []
    w_phi_values = []
    
    for m in m_values:
        cnf = generate_cnf(m)
        o_q_values.append(geometric_quantization_order(cnf))
        w_phi_values.append(resolution_width(cnf))
    
    if len(o_q_values) < 30 or len(w_phi_values) < 30:
        return {
            "metric_name": "o_q vs w_phi",
            "metric_value": None,
            "instances_tested": len(o_q_values),
            "n_max": max(m_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    n = len(o_q_values)
    mean_o_q = sum(o_q_values) / n
    mean_w_phi = sum(w_phi_values) / n
    
    covariance = sum((o_q_values[i] - mean_o_q) * (w_phi_values[i] - mean_w_phi) for i in range(n)) / n
    variance_o_q = sum((o_q_values[i] - mean_o_q) ** 2 for i in range(n)) / n
    variance_w_phi = sum((w_phi_values[i] - mean_w_phi) ** 2 for i in range(n)) / n
    
    correlation_coefficient = covariance / (math.sqrt(variance_o_q) * math.sqrt(variance_w_phi))
    
    return {
        "metric_name": "o_q vs w_phi",
        "metric_value": correlation_coefficient,
        "instances_tested": len(o_q_values),
        "n_max": max(m_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.9 and p_value < 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    
    support_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = Fraction(support_count, len(results)).limit_denominator()
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= Fraction(80, 100):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"not_enough_instances\" first_failing_seed={r['seed']}")
                break