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

def generate_3sat(n, m):
    clauses = []
    variables = set(range(1, n + 1))
    for _ in range(m):
        clause = [random.choice([1, -1]) * random.choice(list(variables)) for _ in range(3)]
        if len(set(abs(x) for x in clause)) == 3:
            clauses.append(clause)
    return clauses

def dpll(model, clauses):
    if not clauses:
        return True
    unit_clauses = [c[0] for c in clauses if len(c) == 1]
    if unit_clauses:
        literal = unit_clauses[0]
        new_model = model.copy()
        new_model[literal] = True
        if dpll(new_model, [c for c in clauses if literal not in c]):
            return True
        new_model[literal] = False
        if dpll(new_model, [c for c in clauses if -literal not in c]):
            return True
        return False
    pure_literals = {}
    for literal in set(abs(x) for x in sum(clauses, [])):
        pos_count = sum(1 for c in clauses if literal in c)
        neg_count = sum(1 for c in clauses if -literal in c)
        if pos_count == 0:
            pure_literals[literal] = False
        elif neg_count == 0:
            pure_literals[literal] = True
    if pure_literals:
        literal, value = next(iter(pure_literals.items()))
        new_model = model.copy()
        new_model[literal] = value
        return dpll(new_model, [c for c in clauses if literal not in c and -literal not in c])
    literal = random.choice(sum(clauses, []))
    new_model_true = model.copy()
    new_model_true[literal] = True
    if dpll(new_model_true, [c for c in clauses if literal not in c]):
        return True
    new_model_false = model.copy()
    new_model_false[literal] = False
    return dpll(new_model_false, [c for c in clauses if -literal not in c])

def lz77_compress(sequence):
    n = len(sequence)
    compressed = []
    i = 0
    while i < n:
        j = i + 1
        max_length = 0
        start_index = -1
        while j <= n:
            if sequence[i:j] in sequence[:i]:
                length = j - i
                index = sequence[:i].rfind(sequence[i:j])
                if length > max_length or (length == max_length and index < start_index):
                    max_length = length
                    start_index = index
            j += 1
        if max_length > 0:
            compressed.append((start_index, max_length))
            i += max_length
        else:
            compressed.append(sequence[i])
            i += 1
    return compressed

def circuit_complexity(clauses):
    n = len(clauses)
    m = len(clauses[0])
    inputs = [i for i in range(1, n + 1)]
    outputs = [i for i in range(n * m + 1, (n * m) * 2 + 1)]
    gates = []
    
    def add_gate(gate_type, inputs):
        gate_id = len(gates) + 1
        gates.append((gate_id, gate_type, inputs))
        return gate_id
    
    for i in range(n):
        for j in range(m):
            literal = clauses[i][j]
            if literal > 0:
                add_gate('OR', [inputs[literal - 1]])
            else:
                add_gate('NOT', [inputs[-literal - 1]])
    
    return len(gates)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 20
    m = 80
    clauses = generate_3sat(n, m)
    if not dpll_with_caching(clauses):
        return {
            "metric_name": "K(π_min)",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "unsatisfiable"
        }
    refutation = dpll_with_caching(clauses)
    compressed_refutation = lz77_compress(refutation)
    K_proxy = len(compressed_refutation)
    C_det = circuit_complexity(clauses)
    if K_proxy > 1.5 * C_det + 10:
        return {
            "metric_name": "K(π_min)",
            "metric_value": K_proxy,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"K_proxy({K_proxy}) > 1.5 * C_det({C_det}) + 10"
        }
    return {
        "metric_name": "K(π_min)",
        "metric_value": K_proxy,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

def dpll_with_caching(clauses):
    cache = {}
    
    def dpll(model, clauses):
        if not clauses:
            return True
        unit_clauses = [c[0] for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0]
            new_model = model.copy()
            new_model[literal] = True
            if dpll(new_model, [c for c in clauses if literal not in c]):
                return True
            new_model[literal] = False
            if dpll(new_model, [c for c in clauses if -literal not in c]):
                return True
            return False
        pure_literals = {}
        for literal in set(abs(x) for x in sum(clauses, [])):
            pos_count = sum(1 for c in clauses if literal in c)
            neg_count = sum(1 for c in clauses if -literal in c)
            if pos_count == 0:
                pure_literals[literal] = False
            elif neg_count == 0:
                pure_literals[literal] = True
        if pure_literals:
            literal, value = next(iter(pure_literals.items()))
            new_model = model.copy()
            new_model[literal] = value
            return dpll(new_model, [c for c in clauses if literal not in c and -literal not in c])
        literal = random.choice(sum(clauses, []))
        new_model_true = model.copy()
        new_model_true[literal] = True
        if dpll(new_model_true, [c for c in clauses if literal not in c]):
            return True
        new_model_false = model.copy()
        new_model_false[literal] = False
        return dpll(new_model_false, [c for c in clauses if -literal not in c])
    
    def evaluate_clause(clause):
        if clause in cache:
            return cache[clause]
        result = any(model.get(lit) == True for lit in clause)
        cache[clause] = result
        return result
    
    def evaluate_clauses(clauses):
        return all(evaluate_clause(c) for c in clauses)
    
    return dpll({}, clauses)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r['metric_value'] for r in results) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] and r['metric_value'] > 1.5 * circuit_complexity(generate_3sat(20, 80)) + 10 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"K_proxy({result['metric_value']}) > 1.5 * C_det({circuit_complexity(generate_3sat(20, 80))}) + 10\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")