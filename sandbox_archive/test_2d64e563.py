import sys
import random
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def degree_of_permutation_polynomial(clauses):
        # Simplified heuristic to estimate the degree of a permutation polynomial
        # based on the number of unique variables in clauses.
        unique_vars = set()
        for clause in clauses:
            for var in clause:
                unique_vars.add(abs(var))
        return len(unique_vars)
    
    def min_abp_size(clauses):
        n = max(abs(var) for var in sum(clauses, []))
        dp = [0] * (n + 1)
        for clause in clauses:
            for i in range(n, -1, -1):
                if i >= abs(clause[0]):
                    dp[i] += dp[i - abs(clause[0])]
                if i >= abs(clause[1]):
                    dp[i] += dp[i - abs(clause[1])]
        return max(dp)
    
    n = random.choice([5, 8, 11, 14])
    m = random.randint(2 * n, 3 * n)
    cnf = generate_cnf(n, m)
    degree = degree_of_permutation_polynomial(cnf)
    abp_size = min_abp_size(cnf)
    
    return {
        "metric_name": "ABP Size",
        "metric_value": abp_size,
        "instances_tested": 1,
        "conjecture_holds": abs(abp_size - degree**2) <= 0.1 * degree**2,
        "counterexample": "" if conjecture_holds else f"Degree {degree}, ABP Size {abp_size}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_abp_size = sum(r["metric_value"] for r in results)
    num_seeds = len(results)
    avg_abp_size = total_abp_size / num_seeds
    std_abp_size = (sum((r["metric_value"] - avg_abp_size) ** 2 for r in results) / num_seeds) ** 0.5
    
    support_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = support_count / num_seeds
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_abp_size} std={std_abp_size} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")