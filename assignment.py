import itertools

def is_fact(query, facts):
    """
    Check if the query matches any fact in the knowledge base, accounting for variables.
    """
    for fact in facts:
        if match_fact(query, fact):
            return True
    return False

# Fact
def match_fact(query, fact):
    """
    Check if the fact matches the query, accounting for variables in the query.
    Variables are assumed to be lowercase single characters.
    """
    query_parts = query.split("(")[1][:-1].split(",")
    fact_parts = fact.split("(")[1][:-1].split(",")
    if query.split("(")[0] != fact.split("(")[0]:
        return False  # The predicate names do not match
    for q_part, f_part in zip(query_parts, fact_parts):
        if q_part.islower():  # This is a variable, skip
            continue
        if q_part != f_part:  # Constant does not match
            return False
    return True
def parse_rule(rule):
    ant, con = rule.split("=>")
    antecedent = ant.strip().replace(" and ", " ")
    consequent = con.strip()
    return antecedent, consequent

# backward_chaining
def unify(predicate, target):
    pred_parts = predicate.strip().split("(")[1].split(")")[0].split(",")
    target_parts = target.strip().split("(")[1].split(")")[0].split(",")
    substitution = {}
    if len(pred_parts)!=len(target_parts):
        return None

    for pred_part, target_part in zip(pred_parts, target_parts):
        if pred_part != target_part:
            if pred_part.islower():  # Variable in predicate
                substitution[pred_part] = target_part
            else:
                return None  # Mismatch, cannot unify
    return substitution

def substitute(predicate, substitution):
    for var, value in substitution.items():
        predicate = predicate.replace(var, value)
    return predicate

# merge
def extract_dictionaries(data):
    # 提取所有的字典
    if isinstance(data, dict):
        return [data]
    elif isinstance(data, list):
        dicts = []
        for item in data:
            dicts.extend(extract_dictionaries(item))
        return dicts
    return []

def generate_combinations(dicts):
    # 根据提取的字典生成所有键值组合
    values_by_key = {}
    for entry in dicts:
        for key, value in entry.items():
            if key not in values_by_key:
                values_by_key[key] = set()
            values_by_key[key].add(value)

    all_combinations = list(itertools.product(*(values_by_key[key] for key in sorted(values_by_key))))
    final_results = []
    for combination in all_combinations:
        result = {key: value for key, value in zip(sorted(values_by_key), combination)}
        final_results.append(result)

    return final_results

def backward_chaining(query, knowledge_base):
    facts = knowledge_base['facts']
    rules = knowledge_base['rules']
    answer = []
    if is_fact(query, facts):
        # print(query)
        for fact in facts:
            substitution = unify(query, fact)
            if substitution != {} and substitution is not None:
                answer.append(substitution)
    else:
        for rule in rules:
            antecedents, consequent = parse_rule(rule)  ## get rule construction
            # print(consequent)# Sibling(y,z)
            # print(antecedents)# Father(x,y) Father(x,z)
            if consequent.split("(")[0] == query.split("(")[0]:
                substitution = unify(consequent, query)
                # print(1)
                # print(substitution)#{'x:y': 'Tom:s'}
                if substitution != {}:
                    sub_queries = [substitute(ant, substitution) for ant in antecedents.split(" ")]
                    # print(sub_queries) #['Parent(x,a)', 'Male(x)']   ['Parent(x,b)', 'Male(x)']
                    for sub_query in sub_queries:
                        # print(sub_query) #Parent(x,a) Male(x) Father(x,b)
                        sub_answers = backward_chaining(sub_query, knowledge_base)
                        # print(sub_answers)
                        if sub_answers is not None or sub_answers!=[]:
                            # print(answer)
                            answer.append(sub_answers)
                            # print(answer)
    return answer

def solve_queries(queries, knowledge_base):
    all_results = []
    for query in queries:
        entry = backward_chaining(query, knowledge_base)
        dicts = extract_dictionaries(entry)
        results = generate_combinations(dicts)
        all_results.append(results)
    return all_results

if __name__ == '__main__':
    ## INPUT
    queries = [
        "Parent(Tom,x)",
        "Father(Tom,s)",
        "Father(f,s)",
        "Sibling(a,b)"
    ]
    knowledge_base = {
        'facts': [
            "Parent(Tom,John)",
            "Male(Tom)",
            "Parent(Tom,Fred)"
        ],
        'rules': [
            "Parent(x,y) and Male(x) => Father(x,y)",
            "Father(x,y) and Father(x,z) => Sibling(y,z)"
        ]
    }

    all_results = solve_queries(queries,knowledge_base)
    for idx, result in enumerate(all_results):
        print(f"Results for entry {idx+1}:")
        for res in result:
            print(res)