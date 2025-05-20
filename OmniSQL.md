# OmniSQL: Graph-Based Architecture for Text-to-SQL Generation

## Architecture Overview

OmniSQL is designed as a modular, graph-based system for generating SQL queries from natural language. The architecture leverages the langgraph framework to create a flexible, multi-directional workflow that can handle complex query generation tasks across diverse database schemas.

```
                                       ┌──────────────────────┐
                                       │                      │
                                       │  Input Processing    │
                                       │                      │
                                       └──────────┬───────────┘
                                                  │
                                                  ▼
┌──────────────────────┐            ┌──────────────────────┐            ┌──────────────────────┐
│                      │            │                      │            │                      │
│  Schema Retrieval    │◄──────────►│  Semantic Parsing    │◄──────────►│  Query Planning      │
│                      │            │                      │            │                      │
└──────────┬───────────┘            └──────────┬───────────┘            └──────────┬───────────┘
           │                                    │                                  │
           │                                    ▼                                  │
           │                      ┌──────────────────────┐                         │
           │                      │                      │                         │
           └─────────────────────►│  SQL Generation      │◄────────────────────────┘
                                  │                      │
                                  └──────────┬───────────┘
                                             │
                                             ▼
                           ┌──────────────────────────────┐
                           │                              │
                           │  SQL Validation & Refinement │
                           │                              │
                           └──────────┬───────────────────┘
                                      │
                                      ▼
                      ┌──────────────────────────────────────┐
                      │                                      │
      ┌──────────────►│  Query Execution & Feedback          │◄───────────────┐
      │               │                                      │                │
      │               └──────────────────┬───────────────────┘                │
      │                                  │                                    │
      │                                  ▼                                    │
┌─────┴──────────────────┐  ┌───────────────────────┐       ┌────────────────┴─────────┐
│                        │  │                       │       │                          │
│  Query Reformulation   │  │  Response Generation  │       │  Knowledge Base Update   │
│                        │  │                       │       │                          │
└────────────────────────┘  └───────────────────────┘       └──────────────────────────┘
```

## Node Definitions

### 1. Input Processing Node

**Purpose**: Process and understand the natural language query from the user.

**Functions**:
- Parse and tokenize the natural language input
- Identify query type (SELECT, INSERT, UPDATE, DELETE, etc.)
- Extract key entities, conditions, and relationships
- Detect aggregation requirements (COUNT, AVG, SUM, etc.)
- Recognize temporal expressions and constraints
- Handle ambiguous terms and phrases
- Generate query representation for downstream processing

**Outputs**:
- Structured representation of the user query
- Identified entities and attributes
- Query intent classification
- Confidence scores for parsed elements

### 2. Schema Retrieval Node

**Purpose**: Retrieve and prepare relevant database schema information needed for query generation.

**Functions**:
- Access database catalog information
- Extract table structures, columns, and relationships
- Retrieve foreign key constraints and indexes
- Build schema graph representation
- Filter schema elements based on query context
- Generate schema embeddings for matching
- Cache frequently used schema elements

**Outputs**:
- Relevant schema elements
- Schema graph representation
- Schema embeddings
- Foreign key relationships
- Primary key information

### 3. Semantic Parsing Node

**Purpose**: Map natural language elements to database schema elements and SQL concepts.

**Functions**:
- Link natural language mentions to database tables and columns
- Resolve ambiguous references using schema similarity
- Identify join paths between tables
- Map natural language conditions to SQL predicates
- Handle natural language expressions for sorting and grouping
- Recognize natural language descriptions of aggregations
- Generate semantic parse trees

**Outputs**:
- Entity-column mappings
- Table relevance scores
- Join path candidates
- Condition mappings
- Identified aggregations
- Semantic parse representation

### 4. Query Planning Node

**Purpose**: Develop a structured plan for the SQL query before actual generation.

**Functions**:
- Determine required tables and join relationships
- Plan query structure (nested queries, CTEs, etc.)
- Optimize join order for performance
- Handle aggregation planning
- Plan for complex operations (window functions, grouping sets, etc.)
- Structure sorting and pagination requirements
- Apply schema-specific optimization rules

**Outputs**:
- Query execution plan
- Join strategy
- Structured query outline
- Optimization recommendations
- Query complexity assessment

### 5. SQL Generation Node

**Purpose**: Generate a syntactically correct SQL query based on the semantic parse and query plan.

**Functions**:
- Generate SQL SELECT clauses with appropriate columns
- Construct FROM clauses with necessary tables
- Build JOIN conditions based on identified paths
- Create WHERE clauses from mapped conditions
- Add GROUP BY, HAVING, and ORDER BY clauses
- Apply database-specific SQL dialect rules
- Handle subqueries and common table expressions
- Generate multiple candidate queries when appropriate

**Outputs**:
- Complete SQL query
- Alternative candidate queries
- Query generation metadata
- Confidence scores
- Generation decision traces

### 6. SQL Validation & Refinement Node

**Purpose**: Validate the generated SQL and refine it for correctness and efficiency.

**Functions**:
- Syntax validation
- Schema compatibility checking
- Type checking in expressions and conditions
- Join validity verification
- Query complexity analysis
- Security verification (SQL injection prevention)
- Query optimization suggestions
- Apply performance-enhancing transformations

**Outputs**:
- Validated SQL query
- Refinement recommendations
- Validation errors (if any)
- Performance metrics
- Security checks results

### 7. Query Execution & Feedback Node

**Purpose**: Execute the SQL query against the database and collect execution results and feedback.

**Functions**:
- Execute SQL query in a safe environment
- Capture query results
- Monitor execution performance
- Collect error information
- Compare results with expected outcomes
- Generate feedback for query improvement
- Check result cardinality (empty sets, too many results)
- Validate results against user intent

**Outputs**:
- Query results
- Execution status
- Performance metrics
- Error messages (if any)
- Result statistics
- Feedback signals for refinement

### 8. Query Reformulation Node

**Purpose**: Revise and improve the query based on execution feedback or validation errors.

**Functions**:
- Analyze execution errors
- Identify problematic query parts
- Apply targeted fixes for specific issues
- Generate alternative query formulations
- Improve join conditions and filters
- Handle edge cases (NULL values, empty results)
- Apply domain-specific query patterns

**Outputs**:
- Reformulated SQL query
- Correction strategy applied
- Reformulation rationale
- Alternative approaches

### 9. Knowledge Base Update Node

**Purpose**: Update the system's knowledge base with new patterns and feedback for future queries.

**Functions**:
- Store successful query patterns
- Record entity-column mappings
- Update schema linking statistics
- Learn from errors and corrections
- Build query pattern library
- Update language-schema alignment models
- Maintain user-specific preferences
- Record schema-specific optimizations

**Outputs**:
- Updated knowledge base entries
- Learning metrics
- New pattern templates
- Feedback integration status

### 10. Response Generation Node

**Purpose**: Generate a natural language response explaining the query and results to the user.

**Functions**:
- Format query results for presentation
- Generate natural language explanation of the SQL query
- Explain the reasoning behind table and column choices
- Describe result statistics
- Provide context for empty results
- Generate clarification requests if needed
- Offer query improvement suggestions
- Include alternative query formulations

**Outputs**:
- Formatted query results
- Natural language explanation
- Result statistics explanation
- Clarification requests (if needed)
- Suggested refinements
- Confidence indicators

## Edge Definitions and Workflow Paths

### Primary Path:
1. Input Processing → Semantic Parsing
2. Input Processing → Schema Retrieval
3. Semantic Parsing → Query Planning
4. Query Planning → SQL Generation
5. Schema Retrieval → SQL Generation
6. SQL Generation → SQL Validation & Refinement
7. SQL Validation & Refinement → Query Execution & Feedback
8. Query Execution & Feedback → Response Generation

### Feedback Loops:
1. Query Execution & Feedback → Query Reformulation → SQL Generation
2. SQL Validation & Refinement → Query Reformulation → SQL Generation
3. Query Execution & Feedback → Knowledge Base Update → Semantic Parsing
4. Query Execution & Feedback → Knowledge Base Update → Query Planning

### Bidirectional Edges:
1. Schema Retrieval ↔ Semantic Parsing (for schema-aware parsing and ambiguity resolution)
2. Semantic Parsing ↔ Query Planning (for iterative plan refinement based on semantic constraints)
3. Query Planning ↔ SQL Generation (for query plan adjustments during generation)

### Conditional Routing:
1. SQL Validation & Refinement → Query Execution & Feedback (if valid)
2. SQL Validation & Refinement → Query Reformulation (if invalid)
3. Query Execution & Feedback → Response Generation (if successful)
4. Query Execution & Feedback → Query Reformulation (if execution error)

## State Management

A comprehensive state object is maintained throughout the workflow, evolving as it passes through different nodes:

```python
state = {
    # Input and analysis
    "original_query": str,              # Original natural language query
    "query_intent": str,                # Identified query intent (SELECT, INSERT, etc.)
    "entities": list,                   # Entities extracted from query
    "attributes": list,                 # Attributes extracted from query
    "conditions": list,                 # Conditions extracted from query
    
    # Schema information
    "database_schema": dict,            # Full database schema
    "relevant_tables": list,            # Tables relevant to the query
    "relevant_columns": dict,           # Columns relevant to the query
    "join_paths": list,                 # Potential join paths
    "schema_graph": object,             # Graph representation of schema
    
    # Semantic parse
    "entity_column_mappings": dict,     # Mappings from entities to columns
    "condition_mappings": dict,         # Mappings from conditions to SQL predicates
    "semantic_parse_tree": object,      # Semantic parse representation
    "ambiguities": list,                # Ambiguous references
    
    # Query plan
    "query_plan": object,               # Structured query plan
    "join_strategy": list,              # Join strategy
    "aggregation_plan": dict,           # Plan for aggregations
    "nesting_structure": object,        # Structure for nested queries
    
    # SQL generation
    "generated_sql": str,               # Generated SQL query
    "candidate_queries": list,          # Alternative candidate queries
    "generation_confidence": float,     # Confidence in generated query
    
    # Validation
    "validation_errors": list,          # Any validation errors
    "validation_warnings": list,        # Any validation warnings
    "refinement_suggestions": list,     # Suggestions for refinement
    
    # Execution
    "execution_results": object,        # Results from query execution
    "execution_errors": object,         # Any execution errors
    "execution_metrics": dict,          # Performance metrics
    "result_statistics": dict,          # Statistics about results
    
    # Reformulation
    "reformulation_history": list,      # History of query reformulations
    "reformulation_strategy": str,      # Current reformulation strategy
    
    # Knowledge base
    "learned_patterns": list,           # Patterns learned from current query
    "updated_mappings": dict,           # Updated entity-column mappings
    
    # Response
    "natural_language_response": str,   # Generated response
    "explanation": str,                 # Explanation of the query
    
    # Control flow
    "current_node": str,                # Current active node
    "next_node": str,                   # Next node to process
    "iteration_count": int,             # Count of iterations through the graph
    "error_state": bool,                # Whether an error has occurred
}
```

## LangGraph Implementation

```python
from langgraph.graph import StateGraph

# Define the graph
workflow = StateGraph()

# Add nodes
workflow.add_node("input_processing", input_processing_function)
workflow.add_node("schema_retrieval", schema_retrieval_function)
workflow.add_node("semantic_parsing", semantic_parsing_function)
workflow.add_node("query_planning", query_planning_function)
workflow.add_node("sql_generation", sql_generation_function)
workflow.add_node("sql_validation", sql_validation_function)
workflow.add_node("query_execution", query_execution_function)
workflow.add_node("query_reformulation", query_reformulation_function)
workflow.add_node("knowledge_base_update", knowledge_base_update_function)
workflow.add_node("response_generation", response_generation_function)

# Add primary path edges
workflow.add_edge("input_processing", "semantic_parsing")
workflow.add_edge("input_processing", "schema_retrieval")
workflow.add_edge("semantic_parsing", "query_planning")
workflow.add_edge("query_planning", "sql_generation")
workflow.add_edge("schema_retrieval", "sql_generation")
workflow.add_edge("sql_generation", "sql_validation")
workflow.add_edge("sql_validation", "query_execution")
workflow.add_edge("query_execution", "response_generation")

# Add bidirectional edges
workflow.add_edge("schema_retrieval", "semantic_parsing")
workflow.add_edge("semantic_parsing", "schema_retrieval")
workflow.add_edge("semantic_parsing", "query_planning")
workflow.add_edge("query_planning", "semantic_parsing")
workflow.add_edge("query_planning", "sql_generation")
workflow.add_edge("sql_generation", "query_planning")

# Add feedback loops
workflow.add_edge("query_execution", "query_reformulation")
workflow.add_edge("query_reformulation", "sql_generation")
workflow.add_edge("query_execution", "knowledge_base_update")
workflow.add_edge("knowledge_base_update", "semantic_parsing")
workflow.add_edge("knowledge_base_update", "query_planning")

# Add conditional edges
workflow.add_conditional_edge(
    "sql_validation",
    validation_router,
    {
        "valid": "query_execution", 
        "invalid": "query_reformulation"
    }
)

workflow.add_conditional_edge(
    "query_execution",
    execution_router,
    {
        "success": "response_generation",
        "failure": "query_reformulation"
    }
)

# Compile the graph
compiled_workflow = workflow.compile()
```

## Key Features

### 1. Modular Design
The architecture is highly modular, allowing components to be developed, tested, and improved independently. This enables easier maintenance and iterative improvements.

### 2. Multi-Directional Flow
The graph supports bidirectional communication between components, enabling feedback and refinement during the query generation process.

### 3. Robust Schema Understanding
The Schema Retrieval and Semantic Parsing nodes work together to ensure accurate mapping between natural language and database elements.

### 4. Iterative Refinement
Multiple feedback loops enable the system to learn from mistakes and improve query generation over time.

### 5. Knowledge Base Integration
The Knowledge Base Update node allows the system to learn from each interaction, improving performance for future queries.

### 6. Conditional Routing
Conditional edges allow the system to take different paths based on the results of validation and execution.

### 7. Comprehensive State Management
A rich state object tracks the progress and decisions made throughout the workflow, providing context for each component.

### 8. Explainable Results
The Response Generation node creates natural language explanations of the generated queries, making the system more transparent to users.

### 9. Error Handling
The architecture includes dedicated paths for handling validation and execution errors, ensuring graceful failure recovery.

### 10. Adaptability
The system can adapt to different database schemas and SQL dialects through its knowledge base and schema-aware components.

## Conclusion

This OmniSQL architecture provides a comprehensive, flexible framework for text-to-SQL generation using langgraph. The graph-based structure allows for complex workflows with feedback loops and conditional paths, enabling the system to handle a wide range of query complexities and adapt to different database schemas. The modular design supports continuous improvement through knowledge accumulation and facilitates the integration of advanced NLP and database management techniques.