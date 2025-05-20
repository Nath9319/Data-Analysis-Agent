# TCSR-SQL Architecture: Template-Based Constrained Synthesis with Reinforcement Learning

## Overview

This document outlines a comprehensive architecture for implementing TCSR-SQL (Template-based Constrained Synthesis Reinforcement Learning for SQL generation) using LangGraph. The architecture leverages template-based approaches, constrained synthesis, and reinforcement learning to translate natural language questions into accurate SQL queries.

## Architecture Diagram

```
                                  ┌──────────────────┐
                                  │                  │
                                  │  Input Analysis  │
                                  │                  │
                                  └────────┬─────────┘
                                           │
                                           ▼
┌──────────────────┐            ┌──────────────────┐            ┌──────────────────┐
│                  │            │                  │            │                  │
│  Schema Linking  │◄──────────►│ Template Matcher │◄──────────►│ Constraint Parser│
│                  │            │                  │            │                  │
└────────┬─────────┘            └────────┬─────────┘            └────────┬─────────┘
         │                                │                               │
         │                                ▼                               │
         │                     ┌──────────────────┐                       │
         │                     │                  │                       │
         └────────────────────►│  SQL Generator   │◄──────────────────────┘
                               │                  │
                               └────────┬─────────┘
                                        │
                                        ▼
                              ┌──────────────────┐
                              │                  │
                              │ SQL Verification │
                              │                  │
                              └────────┬─────────┘
                                       │
                                       ▼
                          ┌───────────────────────┐
                          │                       │
            ┌────────────►│ Execution & Feedback  │◄────────────┐
            │             │                       │              │
            │             └───────────┬───────────┘              │
            │                         │                          │
            │                         ▼                          │
┌───────────┴───────────┐  ┌──────────────────┐    ┌─────────────┴───────────┐
│                       │  │                  │    │                         │
│ Reinforcement Learner │  │  Output Node     │    │ Template Refinement     │
│                       │  │                  │    │                         │
└───────────────────────┘  └──────────────────┘    └─────────────────────────┘
```

## Node Definitions

### 1. Input Analysis Node

**Purpose**: Analyze and process the natural language question to extract key elements for SQL generation.

**Functions**:
- Parse natural language question using NLP techniques
- Identify query intent (SELECT, INSERT, UPDATE, DELETE)
- Extract entities, attributes, conditions, and operators
- Detect aggregation functions and ordering requirements
- Identify temporal constraints and joins
- Generate semantic representation of the query

**Outputs**:
- Structured query representation
- Query intent classification
- Identified entities and attributes
- Extracted conditions and operators

### 2. Schema Linking Node

**Purpose**: Link natural language elements to database schema elements.

**Functions**:
- Match extracted entities to database tables
- Map attributes to table columns
- Resolve ambiguous references using schema similarity metrics
- Identify potential joins based on foreign key relationships
- Calculate confidence scores for schema mappings
- Handle schema-specific terminology and synonyms

**Outputs**:
- Schema-linked representation
- Entity-table mappings
- Attribute-column mappings
- Join path candidates
- Schema linking confidence scores

### 3. Template Matcher Node

**Purpose**: Select and adapt appropriate SQL templates based on the query type and structure.

**Functions**:
- Maintain a library of SQL templates for different query types
- Match query intent and structure to appropriate templates
- Rank templates by relevance to the current query
- Handle complex nested query patterns
- Select appropriate aggregation templates
- Identify specialized templates (e.g., window functions, CTEs)

**Outputs**:
- Selected SQL templates
- Template ranking scores
- Template slot mappings
- Query structure representation

### 4. Constraint Parser Node

**Purpose**: Define and enforce constraints to ensure SQL validity and correctness.

**Functions**:
- Parse database schema constraints (types, keys, etc.)
- Generate type compatibility constraints
- Apply semantic constraints based on query logic
- Create join path constraints
- Define aggregation and grouping constraints
- Handle nested query constraints
- Generate ordering and limit constraints

**Outputs**:
- Constraint set for SQL generation
- Type compatibility rules
- Join path constraints
- Aggregation constraints
- Query structure constraints

### 5. SQL Generator Node

**Purpose**: Generate SQL queries by filling templates with schema elements while respecting constraints.

**Functions**:
- Fill template slots with column and table references
- Apply constraints during generation
- Handle JOIN clause construction
- Generate WHERE conditions based on natural language constraints
- Apply proper SQL syntax and formatting
- Generate multiple candidate queries when appropriate
- Score generated queries based on constraint satisfaction

**Outputs**:
- Candidate SQL queries
- Generation confidence scores
- Constraint satisfaction metrics
- Generation traces for debugging

### 6. SQL Verification Node

**Purpose**: Verify the syntactic and semantic correctness of generated SQL queries.

**Functions**:
- Check SQL syntax validity
- Verify schema references (tables and columns)
- Check type compatibility in expressions
- Validate JOIN conditions
- Ensure constraint satisfaction
- Identify potential injection vulnerabilities
- Assess query complexity and performance implications

**Outputs**:
- Verification results
- Syntax check results
- Schema reference validation
- Constraint validation results
- Security check results

### 7. Execution & Feedback Node

**Purpose**: Execute SQL queries against the database and gather execution feedback.

**Functions**:
- Execute SQL queries in a safe environment
- Capture execution results or errors
- Measure execution performance
- Compare results with expected outcomes
- Generate feedback signals for refinement
- Identify execution pattern issues
- Track execution history for learning

**Outputs**:
- Execution results
- Error messages (if any)
- Performance metrics
- Feedback signals
- Execution success/failure status

### 8. Template Refinement Node

**Purpose**: Refine templates based on execution feedback.

**Functions**:
- Analyze execution failures
- Identify template weaknesses
- Apply specific fixes to templates
- Generate new template variants
- Prune ineffective templates
- Adjust template matching scores
- Update template library

**Outputs**:
- Refined templates
- Template adjustment records
- New template variants
- Updated template library

### 9. Reinforcement Learning Node

**Purpose**: Learn from feedback to improve future SQL generation.

**Functions**:
- Process feedback signals from execution
- Update reinforcement learning model
- Calculate rewards based on execution success
- Update policy for template selection
- Update policy for constraint application
- Learn schema linking patterns
- Balance exploration and exploitation
- Track learning progress

**Outputs**:
- Updated RL model
- Learned policies
- Learning metrics
- Exploration strategy updates

### 10. Output Node

**Purpose**: Format and return the final SQL query and related information.

**Functions**:
- Select the best SQL query from candidates
- Format SQL for readability
- Generate explanation for the query
- Provide confidence scores
- Include alternative queries if appropriate
- Format error messages when needed
- Include execution statistics

**Outputs**:
- Final SQL query
- Query explanation
- Confidence score
- Alternative queries (if appropriate)
- Execution statistics (if requested)

## Edge Definitions and Workflow

### Primary Path:
1. Input Analysis → Schema Linking
2. Input Analysis → Template Matcher
3. Schema Linking → SQL Generator
4. Template Matcher → SQL Generator
5. Constraint Parser → SQL Generator
6. SQL Generator → SQL Verification
7. SQL Verification → Execution & Feedback
8. Execution & Feedback → Output Node

### Feedback Loops:
1. Execution & Feedback → Template Refinement → Template Matcher
2. Execution & Feedback → Reinforcement Learner → Template Matcher
3. Execution & Feedback → Reinforcement Learner → Schema Linking
4. SQL Verification → SQL Generator (for failed verification)
5. SQL Verification → Constraint Parser (for constraint adjustment)

### Bidirectional Edges:
1. Schema Linking ↔ Template Matcher (for schema-aware template selection)
2. Template Matcher ↔ Constraint Parser (for template-specific constraints)
3. SQL Verification ↔ Execution & Feedback (for early feedback)

## State Management

The system maintains a comprehensive state object that evolves as it passes through the nodes:

```python
state = {
    # Input and analysis
    "original_question": str,              # Original natural language question
    "query_intent": str,                   # Identified query intent (SELECT, INSERT, etc.)
    "entities": list,                      # Entities extracted from question
    "attributes": list,                    # Attributes extracted from question
    "conditions": list,                    # Conditions extracted from question
    
    # Schema information
    "database_schema": dict,               # Full database schema
    "table_mappings": dict,                # Mappings from entities to tables
    "column_mappings": dict,               # Mappings from attributes to columns
    "join_paths": list,                    # Potential join paths
    "schema_confidence": dict,             # Confidence in schema mappings
    
    # Templates
    "selected_templates": list,            # Templates selected for the query
    "template_scores": dict,               # Scores for each template
    "template_slots": dict,                # Slot definitions for templates
    
    # Constraints
    "type_constraints": list,              # Data type constraints
    "join_constraints": list,              # Join path constraints
    "aggregation_constraints": list,       # Aggregation and grouping constraints
    "semantic_constraints": list,          # Semantic validity constraints
    
    # Generation
    "candidate_queries": list,             # Generated SQL queries
    "generation_scores": dict,             # Scores for generated queries
    "constraint_violations": dict,         # Any constraint violations
    
    # Verification and execution
    "verification_results": dict,          # Results of SQL verification
    "execution_results": dict,             # Results of query execution
    "execution_errors": dict,              # Any execution errors
    "performance_metrics": dict,           # Query performance metrics
    
    # Learning and feedback
    "feedback_signals": dict,              # Feedback signals from execution
    "reward_signals": dict,                # Reward signals for RL
    "policy_state": dict,                  # Current state of RL policy
    "template_updates": dict,              # Updates to templates
    
    # Output
    "final_query": str,                    # Final selected SQL query
    "query_explanation": str,              # Explanation of the query
    "confidence_score": float,             # Overall confidence in the query
    "alternatives": list,                  # Alternative queries
    
    # Control flow
    "iteration_count": int,                # Number of refinement iterations
    "current_node": str,                   # Current active node
    "next_node": str,                      # Next node to process
}
```

## LangGraph Implementation

```python
from langgraph.graph import StateGraph

# Define the graph
workflow = StateGraph()

# Add nodes
workflow.add_node("input_analysis", input_analysis_function)
workflow.add_node("schema_linking", schema_linking_function)
workflow.add_node("template_matcher", template_matcher_function)
workflow.add_node("constraint_parser", constraint_parser_function)
workflow.add_node("sql_generator", sql_generator_function)
workflow.add_node("sql_verification", sql_verification_function)
workflow.add_node("execution_feedback", execution_feedback_function)
workflow.add_node("template_refinement", template_refinement_function)
workflow.add_node("reinforcement_learner", reinforcement_learner_function)
workflow.add_node("output_node", output_function)

# Add primary path edges
workflow.add_edge("input_analysis", "schema_linking")
workflow.add_edge("input_analysis", "template_matcher")
workflow.add_edge("schema_linking", "sql_generator")
workflow.add_edge("template_matcher", "sql_generator")
workflow.add_edge("constraint_parser", "sql_generator")
workflow.add_edge("sql_generator", "sql_verification")
workflow.add_edge("sql_verification", "execution_feedback")
workflow.add_edge("execution_feedback", "output_node")

# Add bidirectional edges
workflow.add_edge("schema_linking", "template_matcher")
workflow.add_edge("template_matcher", "schema_linking")
workflow.add_edge("template_matcher", "constraint_parser")
workflow.add_edge("constraint_parser", "template_matcher")

# Add feedback loops
workflow.add_edge("execution_feedback", "template_refinement")
workflow.add_edge("template_refinement", "template_matcher")
workflow.add_edge("execution_feedback", "reinforcement_learner")
workflow.add_edge("reinforcement_learner", "template_matcher")
workflow.add_edge("reinforcement_learner", "schema_linking")

# Add conditional edges for verification results
workflow.add_conditional_edge(
    "sql_verification",
    verification_router_function,
    {
        "success": "execution_feedback",
        "syntax_error": "sql_generator",
        "constraint_violation": "constraint_parser"
    }
)

# Add conditional edges for execution results
workflow.add_conditional_edge(
    "execution_feedback",
    execution_router_function,
    {
        "success": "output_node",
        "refinement_needed": "template_refinement",
        "learning_needed": "reinforcement_learner"
    }
)

# Compile the graph
compiled_workflow = workflow.compile()
```

## Key Features

### 1. Template-Based Approach
TCSR-SQL uses a template library for SQL generation, allowing for structured, predictable queries. Templates capture common SQL patterns and are filled with appropriate schema elements.

### 2. Constrained Synthesis
Constraints guide the SQL generation process to ensure:
- Type compatibility
- Schema validity
- Logical consistency
- Security (preventing SQL injection)
- Performance considerations

### 3. Reinforcement Learning
The system learns from execution feedback to improve:
- Template selection
- Schema linking accuracy
- Constraint application
- Query optimization

### 4. Multi-Directional Workflow
The graph structure allows for:
- Multiple paths through the system
- Feedback loops for refinement
- Bidirectional communication between components
- Dynamic routing based on verification and execution results

### 5. Iterative Refinement
Failed queries can be refined through:
- Template adjustments
- Constraint relaxation or tightening
- Schema link reconsideration
- Policy updates via reinforcement learning

## Conclusion

This architecture for TCSR-SQL implements a sophisticated text-to-SQL system using template-based constrained synthesis with reinforcement learning. The graph-based workflow allows for multi-directional processing, iterative refinement, and learning from feedback. By separating concerns into distinct nodes while allowing communication between them, the system can handle the complexity of SQL generation while maintaining modularity and extensibility.

The use of LangGraph enables the implementation of feedback loops and conditional routing that are essential for template refinement and reinforcement learning. This design creates a system that can improve over time and adapt to different database schemas and query patterns.