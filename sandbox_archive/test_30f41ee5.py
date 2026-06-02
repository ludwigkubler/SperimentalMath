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
        for _ in range(n):
            clause = " or ".join(f"({random.randint(1, n)}{random.choice(['', ' not'])})" for _ in range(random.randint(1, 3)))
            clauses.append(clause)
        return " and ".join(clauses)
    
    def dual_cnf(phi):
        literals = set()
        for clause in phi.split(" and "):
            literals.update(int(x.strip("()")) for x in clause.split(" or ") if x)
        dual_clauses = []
        for literal in literals:
            dual_clauses.append(f"({literal} not) or ({-literal})")
        return " and ".join(dual_clauses)
    
    def shannon_entropy(probs):
        return -sum(p * math.log2(p) for p in probs if p > 0)
    
    def min_order(phi, p):
        residues = set()
        for clause in phi.split(" and "):
            for literal in clause.split(" or "):
                lit = int(literal.strip("()"))
                residues.add((lit % p, -lit % p))
        orders = [len(residues) for p in range(2, 100) if len(set(x[0] for x in residues)) == len(set(x[1] for x in residues))]
        return min(orders) if orders else None
    
    def entropy_of_clause_set(phi):
        n = sum(1 for _ in phi.split(" and "))
        probs = [1 / n] * n
        return shannon_entropy(probs)
    
    instances_tested = 0
    total_min_order = 0
    total_entropy = 0
    n_max = 0
    
    for n in range(5, 41):
        phi = generate_cnf(n)
        phi_star = dual_cnf(phi)
        
        min_order_phi = min_order(phi, random.randint(2, 100))
        entropy_phi = entropy_of_clause_set(phi)
        
        if min_order_phi is not None:
            instances_tested += 1
            total_min_order += min_order_phi
            total_entropy += entropy_phi
            n_max = max(n_max, n)
    
    mean_min_order = total_min_order / instances_tested if instances_tested > 0 else 0
    mean_entropy = total_entropy / instances_tested if instances_tested > 0 else 0
    
    correlation_coefficient = (instances_tested * sum(min_order_phi * entropy_phi for min_order_phi, entropy_phi in zip(range(n_max), range(n_max))) - 
                               instances_tested * mean_min_order * mean_entropy) / math.sqrt(
                                   instances_tested * sum((min_order_phi - mean_min_order) ** 2 for min_order_phi in range(n_max)) *
                                   instances_tested * sum((entropy_phi - mean_entropy) ** 2 for entropy_phi in range(n_max)))
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7"
    
    return {
        "metric_name": "Pearson's Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(abs(r["metric_value"]) < 0.5 or abs(r["metric_value"] - (r["n_max"] // 2)) > 2 * std_metric_value for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.7\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if abs(r['metric_value']) < 0.5 or abs(r['metric_value'] - (r['n_max'] // 2)) > 2 * std_metric_value)]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")