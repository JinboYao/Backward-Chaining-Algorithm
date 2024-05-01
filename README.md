# Backward Chaining Algorithm in Python

## Overview

The backward chaining algorithm is a method used in artificial intelligence for reasoning backward from goals to known facts or evidence. It is particularly useful in rule-based expert systems to infer conclusions from a given set of rules and facts. This document outlines the implementation of the backward chaining algorithm to solve queries related to familial relationships using first-order logic.

## Problem Statement

The task is to implement the backward chaining algorithm in Python to perform inference based on a given knowledge base of familial relationships and to answer specific queries using this inference technique.

### Knowledge Base

The knowledge base includes rules and facts representing familial relationships:

```python
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
```

### Queries

```python
    queries = [
        "Parent(Tom,x)",
        "Father(Tom,s)",
        "Father(f,s)",
        "Sibling(a,b)"
    ]
```

## Requirements

- The algorithm should derive conclusions from the given knowledge base using backward chaining.
- Only standard Python libraries should be utilized in the implementation.
- The algorithm should correctly answer the queries based on the derived inferences.

## Implementation

Here is a simplified code snippet of the backward chaining algorithm implemented in Python:

## Result
![微信截图_20240501162858.png](https://img2.imgtp.com/2024/05/01/TBxQk52g.png)
