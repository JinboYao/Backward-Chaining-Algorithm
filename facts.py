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

def is_fact(query, facts):
    """
    Check if the query matches any fact in the knowledge base, accounting for variables.
    """
    for fact in facts:
        if match_fact(query, fact):
            return True
    return False

def unify(predicate, target):
    pred_parts = predicate.strip().split("(")[1].split(")")[0].split(",")
    target_parts = target.strip().split("(")[1].split(")")[0].split(",")
    substitution = {}
    for pred_part, target_part in zip(pred_parts, target_parts):
        if pred_part != target_part:
            if pred_part.islower():  # Variable in predicate
                substitution[pred_part] = target_part
            else:
                return None  # Mismatch, cannot unify
    return substitution

def backward_chaining(query, knowledge_base):
    facts = knowledge_base['facts']
    rules = knowledge_base['rules']
    answer = []
    if is_fact(query, facts):
        for fact in facts:
            substitution = unify(query, fact)
            if substitution != {}:
                answer.append(substitution)
                # print(answer)
    return answer

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

demo = backward_chaining("Parent(Tom,x)",knowledge_base)
print(demo)  # 应该输出：{'x': 'John'}