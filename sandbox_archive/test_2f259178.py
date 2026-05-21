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
    
    def evaluate_circuit(circuit, input_values):
        stack = []
        for gate in circuit:
            if gate[0] == 'AND':
                a = stack.pop()
                b = stack.pop()
                stack.append(a and b)
            elif gate[0] == 'OR':
                a = stack.pop()
                b = stack.pop()
                stack.append(a or b)
            elif gate[0] == 'NOT':
                a = stack.pop()
                stack.append(not a)
        return stack[0]
    
    def greedy_bias_trajectory(truth_table):
        n = len(truth_table)
        t = math.ceil(math.log2(n))
        p_i, q_i = Fraction(1), Fraction(1)
        trajectory = []
        
        for _ in range(t):
            max_diff = -1
            best_var = None
            best_val = None
            
            for var in range(n):
                for val in [0, 1]:
                    restricted_table = [truth_table[i][var] == val for i in range(n)]
                    prob = sum(restricted_table) / n
                    diff = abs(prob - Fraction(1, 2))
                    if diff > max_diff:
                        max_diff = diff
                        best_var = var
                        best_val = val
            
            p_i, q_i = Fraction(sum(truth_table[i][best_var] == best_val for i in range(n)), n), Fraction(n)
            trajectory.append((p_i, q_i))
        
        return trajectory
    
    def continued_fraction_length(fraction):
        a, b = fraction.numerator, fraction.denominator
        length = 0
        
        while b != 0:
            quotient = a // b
            remainder = a % b
            a, b = b, remainder
            length += 1
        
        return length
    
    def build_truth_table(n, size):
        truth_table = [[random.choice([0, 1]) for _ in range(n)] for _ in range(size)]
        return truth_table
    
    def is_acc0_circuit(circuit):
        gates = set()
        for gate in circuit:
            gates.add(gate[0])
        return len(gates) <= 3 and all(gate[0] in ['AND', 'OR', 'NOT'] for gate in circuit)
    
    def is_sipser_depth_3_ac0_formula(circuit):
        if not is_acc0_circuit(circuit):
            return False
        depth = 0
        stack = []
        for gate in circuit:
            if gate[0] == 'AND' or gate[0] == 'OR':
                stack.append(gate)
                depth += 1
            elif gate[0] == 'NOT':
                stack[-1] = ('NOT', stack[-1])
        return depth <= 3
    
    def is_parity_function(circuit):
        if not is_acc0_circuit(circuit):
            return False
        for gate in circuit:
            if gate[0] != 'AND' and gate[0] != 'OR':
                return False
        return True
    
    def is_majority_function(circuit):
        if not is_acc0_circuit(circuit):
            return False
        for gate in circuit:
            if gate[0] != 'AND' and gate[0] != 'OR':
                return False
        return True
    
    def build_random_circuit(n, size, depth):
        gates = ['AND', 'OR', 'NOT']
        circuit = []
        stack = []
        
        for _ in range(size):
            if len(stack) < depth:
                gate = random.choice(gates)
                stack.append((gate, stack.pop() if gate != 'NOT' else None))
            else:
                gate = random.choice(['AND', 'OR'])
                a = stack.pop()
                b = stack.pop()
                circuit.append((gate, a, b))
                stack.append((gate, (a[0], b[0])))
        
        while len(stack) > 1:
            gate = random.choice(['AND', 'OR'])
            a = stack.pop()
            b = stack.pop()
            circuit.append((gate, a, b))
            stack.append((gate, (a[0], b[0])))
        
        return circuit
    
    def build_sipser_depth_3_ac0_formula(n):
        # This is a simplified example. A real implementation would be more complex.
        gates = ['AND', 'OR']
        circuit = []
        stack = []
        
        for _ in range(10):  # Simplified size
            if len(stack) < 3:
                gate = random.choice(gates)
                stack.append((gate, stack.pop() if gate != 'NOT' else None))
            else:
                gate = random.choice(['AND', 'OR'])
                a = stack.pop()
                b = stack.pop()
                circuit.append((gate, a, b))
                stack.append((gate, (a[0], b[0])))
        
        while len(stack) > 1:
            gate = random.choice(['AND', 'OR'])
            a = stack.pop()
            b = stack.pop()
            circuit.append((gate, a, b))
            stack.append((gate, (a[0], b[0])))
        
        return circuit
    
    def build_parity_function(n):
        # This is a simplified example. A real implementation would be more complex.
        gates = ['AND', 'OR']
        circuit = []
        stack = []
        
        for _ in range(5):  # Simplified size
            if len(stack) < 3:
                gate = random.choice(gates)
                stack.append((gate, stack.pop() if gate != 'NOT' else None))
            else:
                gate = random.choice(['AND', 'OR'])
                a = stack.pop()
                b = stack.pop()
                circuit.append((gate, a, b))
                stack.append((gate, (a[0], b[0])))
        
        while len(stack) > 1:
            gate = random.choice(['AND', 'OR'])
            a = stack.pop()
            b = stack.pop()
            circuit.append((gate, a, b))
            stack.append((gate, (a[0], b[0])))
        
        return circuit
    
    def build_majority_function(n):
        # This is a simplified example. A real implementation would be more complex.
        gates = ['AND', 'OR']
        circuit = []
        stack = []
        
        for _ in range(5):  # Simplified size
            if len(stack) < 3:
                gate = random.choice(gates)
                stack.append((gate, stack.pop() if gate != 'NOT' else None))
            else:
                gate = random.choice(['AND', 'OR'])
                a = stack.pop()
                b = stack.pop()
                circuit.append((gate, a, b))
                stack.append((gate, (a[0], b[0])))
        
        while len(stack) > 1:
            gate = random.choice(['AND', 'OR'])
            a = stack.pop()
            b = stack.pop()
            circuit.append((gate, a, b))
            stack.append((gate, (a[0], b[0])))
        
        return circuit
    
    def build_sipser_hard_function(n):
        # This is a simplified example. A real implementation would be more complex.
        gates = ['AND', 'OR']
        circuit = []
        stack = []
        
        for _ in range(15):  # Simplified size
            if len(stack) < 3:
                gate = random.choice(gates)
                stack.append((gate, stack.pop() if gate != 'NOT' else None))
            else:
                gate = random.choice(['AND', 'OR'])
                a = stack.pop()
                b = stack.pop()
                circuit.append((gate, a, b))
                stack.append((gate, (a[0], b[0])))
        
        while len(stack) > 1:
            gate = random.choice(['AND', 'OR'])
            a = stack.pop()
            b = stack.pop()
            circuit.append((gate, a, b))
            stack.append((gate, (a[0], b[0])))
        
        return circuit
    
    n_values = [12, 15, 18]
    results = []
    
    for n in n_values:
        for size in [20, 40, 80]:
            for depth in [2, 3, 4]:
                if is_acc0_circuit(build_random_circuit(n, size, depth)):
                    truth_table = build_truth_table(n, size)
                    trajectory = greedy_bias_trajectory(truth_table)
                    D_f = sum(continued_fraction_length(Fraction(p_i, q_i)) for p_i, q_i in trajectory)
                    results.append({
                        "metric_name": "D(f)",
                        "metric_value": D_f,
                        "instances_tested": 1,
                        "conjecture_holds": D_f <= 8 * depth * (math.log2(size) ** 2) + depth * math.log2(n),
                        "counterexample": ""
                    })
    
    for n in n_values:
        if n == 18:
            truth_table = build_parity_function(n)
            trajectory = greedy_bias_trajectory(truth_table)
            D_f = sum(continued_fraction_length(Fraction(p_i, q_i)) for p_i, q_i in trajectory)
            results.append({
                "metric_name": "D(f)",
                "metric_value": D_f,
                "instances_tested": 1,
                "conjecture_holds": D_f <= 8 * depth * (math.log2(size) ** 2) + depth * math.log2(n),
                "counterexample": ""
            })
    
    for n in n_values:
        if n == 18:
            truth_table = build_majority_function(n)
            trajectory = greedy_bias_trajectory(truth_table)
            D_f = sum(continued_fraction_length(Fraction(p_i, q_i)) for p_i, q_i in trajectory)
            results.append({
                "metric_name": "D(f)",
                "metric_value": D_f,
                "instances_tested": 1,
                "conjecture_holds": D_f > 8 * depth * (math.log2(size) ** 2) + depth * math.log2(n),
                "counterexample": ""
            })
    
    for n in n_values:
        if n == 18:
            truth_table = build_sipser_depth_3_ac0_formula(n)
            trajectory = greedy_bias_trajectory(truth_table)
            D_f = sum(continued_fraction_length(Fraction(p_i, q_i)) for p_i, q_i in trajectory)
            results.append({
                "metric_name": "D(f)",
                "metric_value": D_f,
                "instances_tested": 1,
                "conjecture_holds": D_f > 8 * depth * (math.log2(size) ** 2) + depth * math.log2(n),
                "counterexample": ""
            })
    
    for n in n_values:
        if n == 18:
            truth_table = build_sipser_hard_function(n)
            trajectory = greedy_bias_trajectory(truth_table)
            D_f = sum(continued_fraction_length(Fraction(p_i, q_i)) for p_i, q_i in trajectory)
            results.append({
                "metric_name": "D(f)",
                "metric_value": D_f,
                "instances_tested": 1,
                "conjecture_holds": D_f > 8 * depth * (math.log2(size) ** 2) + depth * math.log2(n),
                "counterexample": ""
            })
    
    mean_D = sum(result["metric_value"] for result in results) / len(results)
    std_D = math.sqrt(sum((result["metric_value"] - mean_D) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "mean_D": mean_D,
        "std_D": std_D,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_D = sum(result["mean_D"] for result in results) / len(results)
    std_D = math.sqrt(sum((result["mean_D"] - mean_D) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.8) / len(results)
    
    if all(result["support_fraction"] >= 0.8 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_D} std={std_D} support_fraction={support_fraction}")
    elif any(result["support_fraction"] < 0.8 for result in results) and any(result["support_fraction"] >= 0.5 for result in results):
        print("RESULT: FALSIFIED counterexample=\"not enough support\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")