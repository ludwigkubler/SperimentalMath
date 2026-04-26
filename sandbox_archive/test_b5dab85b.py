import sys
import random
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3sat_instance(n):
        clauses = []
        for _ in range(2 * n):
            literals = [random.choice([1, -1]) * (i + 1) for i in random.sample(range(n), 3)]
            clauses.append(literals)
        return clauses
    
    def clause_variable_incidence_matrix(clauses, n):
        M = [[0] * n for _ in range(len(clauses))]
        for i, clause in enumerate(clauses):
            for literal in clause:
                var_index = abs(literal) - 1
                if literal > 0:
                    M[i][var_index] = 1
                else:
                    M[i][var_index] = -1
        return M
    
    def matrix_rigidity(M):
        n = len(M[0])
        rank = 0
        for k in range(1, n + 1):
            for subset in combinations(range(n), k):
                submatrix = [row[:] for row in M]
                for col in subset:
                    for i in range(len(submatrix)):
                        submatrix[i][col] = 0
                if rank_matrix(submatrix) == k:
                    rank += 1
        return n * (n - rank)
    
    def rank_matrix(M):
        m, n = len(M), len(M[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            if M[i][i] == 0:
                return rank_matrix([row[:] for row in M[:i]] + [row[:] for row in M[i+1:]])
            for j in range(i + 1, m):
                factor = -M[j][i] / M[i][i]
                for k in range(n):
                    M[j][k] += factor * M[i][k]
        return sum(1 for row in M if any(row))
    
    def communication_complexity(clauses):
        # Simplified deterministic communication complexity
        return len(clauses)
    
    n = random.choice([5, 8, 11, 14])
    instance = generate_3sat_instance(n)
    M = clause_variable_incidence_matrix(instance, n)
    rigidity = matrix_rigidity(M)
    comm_complexity = communication_complexity(instance)
    
    metric_name = "communication_complexity"
    metric_value = comm_complexity
    instances_tested = 1
    conjecture_holds = comm_complexity >= rigidity
    counterexample = "" if conjecture_holds else f"Rigidity {rigidity}, Comm. Complexity {comm_complexity}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")