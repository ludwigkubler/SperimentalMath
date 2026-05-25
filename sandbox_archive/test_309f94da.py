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
    
    def generate_expander_graph(n):
        # Simple expander graph generation (n x n grid with edges to neighbors)
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            if i > 0:
                G[i][i-1] = 1
                G[i-1][i] = 1
            if i < n - 1:
                G[i][i+1] = 1
                G[i+1][i] = 1
        return G
    
    def tseitin_formula(G):
        # Generate a Tseitin formula for the expander graph
        n = len(G)
        clauses = []
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j] == 1:
                    clauses.append([i + 1, -j - 1])
                    clauses.append([-i - 1, j + 1])
                    clauses.append([i + 1, j + 1])
        return clauses
    
    def resolution_refutation_length(clauses):
        # Simple DPLL solver to estimate refutation length
        stack = []
        assignment = [0] * (len(clauses) * 2)
        
        def dpll():
            if not clauses:
                return True, len(stack)
            literal = next((l for l in range(1, len(assignment)) if assignment[l] == 0), None)
            if literal is None:
                return False, 0
            sign = 1 if random.choice([True, False]) else -1
            stack.append(literal * sign)
            assignment[abs(literal)] = sign
            new_clauses = []
            for clause in clauses:
                if any(abs(l) == abs(literal) for l in clause):
                    continue
                if all(assignment[abs(l)] != 0 for l in clause):
                    return False, 0
                new_clause = [l for l in clause if abs(l) != abs(literal)]
                new_clauses.append(new_clause)
            result, length = dpll()
            if result:
                return True, length + 1
            stack.pop()
            assignment[abs(literal)] = 0
            return dpll()
        
        return dpll()[1]
    
    def geometric_loci_complexity(G):
        # Simple heuristic to estimate geometric loci complexity (number of distinct points)
        n = len(G)
        points = set()
        for i in range(n):
            for j in range(i + 1, n):
                if G[i][j] == 1:
                    points.add((i, j))
        return len(points)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        G = generate_expander_graph(n)
        F_G = tseitin_formula(G)
        refutation_length = resolution_refutation_length(F_G)
        loci_complexity = geometric_loci_complexity(G)
        
        if refutation_length < 2**(n/3) and loci_complexity >= n:
            results.append((True, ""))
        elif refutation_length >= 2**(n/3) and loci_complexity < n:
            results.append((False, "Refutation length > 2^(n/3), but loci complexity < n"))
        else:
            results.append((None, "Undefined mapping for this conjecture"))
    
    metric_value = sum(1 for hold, _ in results if hold) / len(results)
    conjecture_holds = all(hold is True for hold, _ in results)
    counterexample = next(counter for _, counter in results if counter != "")
    
    return {
        "metric_name": "Conjecture Support",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] is True for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")