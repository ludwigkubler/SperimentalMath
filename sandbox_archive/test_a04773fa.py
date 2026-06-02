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
    
    def generate_cnf(n, h):
        cnf = []
        for _ in range(h):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def compute_clause_entropy(cnf):
        total_clauses = len(cnf)
        entropy = 0
        for i in range(total_clauses):
            for j in range(i + 1, total_clauses):
                if set(cnf[i]) & set(cnf[j]):
                    continue
                p = Fraction(1, total_clauses - i)
                entropy += math.log2(p) * p
        return entropy
    
    def compute_mcd(cnf):
        n = len(set(abs(lit) for clause in cnf for lit in clause))
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_mcd = 0
    total_entropy = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(1, n))
            entropy = compute_clause_entropy(cnf)
            mcd = compute_mcd(cnf)
            total_mcd += mcd
            total_entropy += entropy
            instances_tested += 1
    
    mean_mcd = total_mcd / instances_tested
    mean_entropy = total_entropy / instances_tested
    correlation_coefficient = (instances_tested * sum(mcd * entropy for mcd, entropy in zip([mean_mcd] * instances_tested, [mean_entropy] * instances_tested)) - 
                               sum(mcd for mcd in [mean_mcd] * instances_tested) * sum(entropy for entropy in [mean_entropy] * instances_tested)) / \
                              math.sqrt((instances_tested * sum(mcd**2 for mcd in [mean_mcd] * instances_tested) - 
                                          sum(mcd for mcd in [mean_mcd] * instances_tested)**2) *
                                        (instances_tested * sum(entropy**2 for entropy in [mean_entropy] * instances_tested) - 
                                         sum(entropy for entropy in [mean_entropy] * instances_tested)**2))
    
    mean_abs_diff = abs(mean_mcd - mean_entropy)
    
    return {
        "metric_name": "mcd_vs_entropy",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_abs_diff <= 3,
        "counterexample": "" if correlation_coefficient >= 0.8 and mean_abs_diff <= 3 else f"mcd={mean_mcd}, entropy={mean_entropy}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 59))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.4f}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mcd_vs_entropy\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")