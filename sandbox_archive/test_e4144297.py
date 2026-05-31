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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def communication_complexity(cnf):
        n = len(set(abs(lit) for lit in sum(cnf, [])))
        m = len(cnf)
        cc = 0
        for i in range(n):
            for j in range(m):
                if any(i == abs(lit) for lit in cnf[j]):
                    cc += 1
        return cc
    
    def topological_entropy(cnf):
        n = len(set(abs(lit) for lit in sum(cnf, [])))
        m = len(cnf)
        entropy = 0
        for i in range(n):
            count = sum(1 for clause in cnf if any(i == abs(lit) for lit in clause))
            entropy += math.log(count / m) if count > 0 else 0
        return -entropy
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(1, n * 2))
            cc = communication_complexity(cnf)
            entropy = topological_entropy(cnf)
            results.append((n, cc, entropy))
    
    if not results:
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n for _, _, _ in results)
    instances_tested = len(results)
    cc_values = [cc for _, cc, _ in results]
    entropy_values = [entropy for _, _, entropy in results]
    
    mean_cc = sum(cc_values) / instances_tested
    std_cc = math.sqrt(sum((x - mean_cc) ** 2 for x in cc_values) / instances_tested)
    mean_entropy = sum(entropy_values) / instances_tested
    std_entropy = math.sqrt(sum((x - mean_entropy) ** 2 for x in entropy_values) / instances_tested)
    
    correlation_coefficient = sum((cc_values[i] - mean_cc) * (entropy_values[i] - mean_entropy) for i in range(instances_tested)) / (instances_tested * std_cc * std_entropy)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_entropy,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7 and abs(mean_entropy - (mean_cc * 1)) <= 3 * std_entropy,
        "counterexample": "" if correlation_coefficient >= 0.7 else f"correlation_coefficient={correlation_coefficient}, mean_entropy={mean_entropy}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 997) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")