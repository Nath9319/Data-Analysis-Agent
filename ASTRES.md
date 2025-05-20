# ASTRES - Architecture & Workflow Design for Text-to-SQL Generation

## Overview

This document outlines a graph-based architecture for implementing ASTRES (Abstract Syntax Tree Reinforcement & Enhancement System) for Text-to-SQL generation. The architecture leverages LangGraph to create a flexible, multi-directional workflow that enables recursive refinement and optimization of SQL queries.

## Architecture Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │     │                 │
│  Input Processing ─────▶ Schema Linking  ─────▶  AST Generation  ─────▶  SQL Generation  │
│                 │     │                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
                                                       ▲                        │
                                                       │                        │
                                                       │                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │     │                 │
│    Output       ◀─────  Reinforcement   ◀─────  AST Refinement  ◀─────  Query Execution │
│                 │     │   Learning      │     │                 │     │  & Validation   │
└─────────────────┘     └─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Node Definitions

### 1. Input Processing Node

**Purpose**: Analyze and process the natural language query input to prepare it for SQL generation.

**Functions**:
- Parse natural language query
- Extract entities and intent
- Identify key terms and relationships
- Normalize query tokens
- Remove ambiguities

**State Updates**:
- Adds processed query representation
- Adds identified entities and intents
- Adds normalized query tokens

### 2. Schema Linking Node

**Purpose**: Connect natural language elements to database schema elements.

**Functions**:
- Match query terms with database schema elements (tables, columns)
- Calculate similarity scores between query terms and schema elements
- Resolve ambiguous schema references
- Create mappings between natural language concepts and schema elements
- Identify relevant tables and join conditions

**State Updates**:
- Adds schema element mappings
- Adds relevant tables list
- Adds potential join paths
- Adds schema-aware query representation

### 3. AST Generation Node

**Purpose**: Generate Abstract Syntax Trees (ASTs) representing potential SQL queries.

**Functions**:
- Create AST templates based on query intent
- Populate AST with identified schema elements
- Generate multiple candidate ASTs for different interpretations
- Score and rank initial AST candidates
- Apply grammar constraints

**State Updates**:
- Adds candidate ASTs
- Adds AST scores
- Adds tree structure representations
- Adds syntactic validation results

### 4. SQL Generation Node

**Purpose**: Convert AST representations into executable SQL queries.

**Functions**:
- Transform AST to SQL syntax
- Apply database-specific formatting rules
- Ensure proper SQL syntax
- Handle special cases (e.g., subqueries, aggregations)
- Optimize naive query structures

**State Updates**:
- Adds candidate SQL queries
- Adds SQL parsing validation results
- Adds query complexity metrics

### 5. Query Execution & Validation Node

**Purpose**: Execute generated SQL queries and validate results against expected output.

**Functions**:
- Execute SQL queries against database
- Capture execution results and errors
- Validate query syntax and execution
- Measure query performance
- Compare results with expected outputs (if available)
- Detect edge cases and errors

**State Updates**:
- Adds execution results
- Adds error messages
- Adds performance metrics
- Adds validation scores

### 6. AST Refinement Node

**Purpose**: Refine and optimize ASTs based on execution results and feedback.

**Functions**:
- Analyze execution errors and performance issues
- Apply transformations to ASTs to fix issues
- Simplify complex expressions
- Rewrite problematic patterns
- Apply domain-specific optimizations
- Generate alternative AST structures

**State Updates**:
- Adds refined AST candidates
- Updates AST transformation history
- Adds refinement rationale

### 7. Reinforcement Learning Node

**Purpose**: Apply reinforcement learning techniques to improve query generation over time.

**Functions**:
- Calculate rewards based on execution results
- Update RL policy for AST generation
- Balance exploration and exploitation
- Track successful query patterns
- Learn from historical corrections
- Maintain memory of similar queries and solutions

**State Updates**:
- Updates RL policy parameters
- Adds reward signals
- Updates exploration parameters
- Adds learning progress metrics

### 8. Output Node

**Purpose**: Deliver the final SQL query along with explanations and confidence metrics.

**Functions**:
- Select best SQL query from candidates
- Format final output
- Generate explanation of the query
- Provide confidence scores
- Include alternative queries (if applicable)
- Generate documentation

**State Updates**:
- Sets final SQL query
- Sets explanation text
- Sets confidence scores
- Sets query metadata

## State Management

The LangGraph implementation will maintain a shared state object that evolves as it passes through the nodes. The state will include:

```python
state = {
    # Input and processing
    "original_query": str,              # Original natural language query
    "processed_query": dict,            # Processed query with annotations
    "entities": list,                   # Extracted entities
    "intent": str,                      # Identified query intent
    
    # Schema linking
    "schema": dict,                     # Database schema information
    "schema_links": dict,               # Mappings between query terms and schema elements
    "relevant_tables": list,            # Tables relevant to the query
    "join_paths": list,                 # Potential join paths
    
    # AST generation and refinement
    "candidate_asts": list,             # List of candidate ASTs
    "ast_scores": dict,                 # Scores for each AST
    "ast_history": list,                # History of AST transformations
    "ast_similarity_mask": dict,        # Similarity matrix between ASTs
    
    # SQL generation
    "candidate_queries": list,          # Generated SQL queries
    "query_validation": dict,           # SQL syntax validation results
    
    # Execution and validation
    "execution_results": list,          # Results from query execution
    "execution_errors": dict,           # Errors encountered during execution
    "performance_metrics": dict,        # Query performance metrics
    
    # Reinforcement learning
    "rewards": dict,                    # Reward signals for RL
    "policy_state": dict,               # Current state of the RL policy
    "exploration_rate": float,          # Current exploration rate
    
    # Output
    "final_query": str,                 # Final selected SQL query
    "confidence": float,                # Confidence score
    "explanation": str,                 # Explanation of the query
    "alternatives": list,               # Alternative queries
    
    # Control flow
    "iteration_count": int,             # Number of refinement iterations
    "max_iterations": int,              # Maximum allowed iterations
    "early_stop": bool,                 # Flag to stop processing early
}
```

## Decision Logic and Routing

The workflow incorporates decision points that determine the flow through the graph:

1. **After Query Execution & Validation**:
   - If execution is successful and meets quality thresholds → proceed to Output
   - If execution fails or performance is poor → route to AST Refinement

2. **After AST Refinement**:
   - If maximum iterations reached → route to Output with best result so far
   - If significant improvements found → loop back to AST Generation
   - If marginal improvements → apply Reinforcement Learning

3. **Reinforcement Learning Decisions**:
   - Update policy and decide between exploration (trying new patterns) or exploitation (refining successful patterns)
   - Route back to AST Generation with updated policy parameters
   - If convergence criteria met → proceed to Output

## Multi-directional Flow Implementation

The LangGraph implementation enables multi-directional flows through:

```python
from langgraph.graph import StateGraph

# Define the graph
workflow = StateGraph()

# Add nodes
workflow.add_node("input_processing", input_processing_function)
workflow.add_node("schema_linking", schema_linking_function)
workflow.add_node("ast_generation", ast_generation_function)
workflow.add_node("sql_generation", sql_generation_function)
workflow.add_node("query_execution", query_execution_function)
workflow.add_node("ast_refinement", ast_refinement_function)
workflow.add_node("reinforcement_learning", reinforcement_learning_function)
workflow.add_node("output", output_function)

# Define edges
workflow.add_edge("input_processing", "schema_linking")
workflow.add_edge("schema_linking", "ast_generation")
workflow.add_edge("ast_generation", "sql_generation")
workflow.add_edge("sql_generation", "query_execution")

# Conditional edges based on execution results
workflow.add_conditional_edge(
    "query_execution",
    execution_router_function,
    {
        "success": "output",
        "refine": "ast_refinement",
    }
)

# Conditional edges for refinement
workflow.add_conditional_edge(
    "ast_refinement",
    refinement_router_function,
    {
        "max_iterations": "output",
        "significant_improvement": "ast_generation",
        "marginal_improvement": "reinforcement_learning"
    }
)

# Edge from reinforcement learning back to AST generation
workflow.add_edge("reinforcement_learning", "ast_generation")

# Compile the graph
compiled_workflow = workflow.compile()
```

## Special Features

### 1. AST Similarity Masking

The ASTRES system leverages AST similarity measures to:
- Avoid redundant exploration of similar query structures
- Group semantically similar queries
- Identify patterns that consistently succeed or fail
- Guide the refinement process toward diverse solutions

### 2. Schema-Guided Generation

The architecture incorporates database schema knowledge to:
- Constrain AST generation to valid table and column references
- Suggest join conditions based on foreign key relationships
- Detect and handle schema ambiguities
- Apply domain-specific optimizations

### 3. Iterative Refinement

The workflow supports multiple passes through the refinement cycle:
- Tracks improvement across iterations
- Applies increasingly aggressive transformations as needed
- Maintains a history of transformations for explainability
- Uses early stopping when improvements plateau

### 4. Reinforcement Learning Integration

The architecture employs reinforcement learning to:
- Learn from successful and unsuccessful queries
- Adapt to specific database schemas and query patterns
- Balance exploration of new query structures with exploitation of known successful patterns
- Improve over time with accumulated experience

## Conclusion

This architecture provides a comprehensive, graph-based implementation of the ASTRES approach to text-to-SQL generation. By leveraging LangGraph, the system supports complex, multi-directional workflows that enable iterative refinement, reinforcement learning, and dynamic routing based on execution results. The modular design allows for easy extension and optimization of individual components while maintaining a coherent end-to-end system.

The implementation focuses on creating syntactically correct, efficient SQL queries through careful AST manipulation and validation, while incorporating feedback from query execution to continuously improve performance.