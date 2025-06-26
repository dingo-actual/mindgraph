# Executable Graph-of-Thoughts (ExGoT)

Executable Graph-of-Thoughts (ExGoT) is a comprehensive system designed to orchestrate Large Language Model (LLM) reasoning. It operates on a single, dynamically evolving Directed Acyclic Graph (DAG), where processing prioritizes nodes on the **active frontier**. Each node in this graph undergoes a sequence of operations before requesting a **terminal operation**. This terminal operation is then managed by a central **orchestrator**, which handles all operations. Operations can be _stateful_ (affecting the state of the world outside the graph) or _stateless_. Stateful operations are how ExGoT expresses tool calling. The framework incorporates mechanisms to ensure logical consistency of the graph through scope-based conflict detection, prioritized LLM-arbitrated resolution, retry limits for stateful actions, and orchestrated propagation of externally sourced information.

**1. Core ExGoT Components:**

  A. **Dynamic Reasoning Graph (`G`):** A directed acyclic graph `G = (V, E)`, where `V` is a set of **Node** instances (defined below) and `E` is a set of directed edges representing dependencies/generation sequences between these nodes. The graph evolves dynamically as nodes are added or their states change.
  B. **Node Structure:** Each node $v \in V$ in the graph is a Node, characterized by the following four primary fields: Goal, State, Action, and Thoughts.
    i. **`Goals`**: Describes the objectives for this node.
        a. `immediate`: A description of the immediate objective or task the node exists to accomplish.
        b. `original_query`: The top-level problem statement provided by the user, propagated to all nodes. (EGoT integration)
    ii. **`State`**: Represents the current information content and status of the node.
        a. `current_thoughts`: The primary LLM-generated textual content for this node, describing its current reasoning step toward its immediate goal. 
        b. thought history
        c. received information
          - info from graph-external observations
          - info that originated from another node or nodes in the graph
        d. `status`: A string indicating the current lifecycle phase of the node. Examples: `active_frontier` (eligible for orchestrator-facilitated internal processing), `internal_processing` (currently undergoing its Node-Level Internal operation cycle), `awaiting_orchestrator_action` (internal processing complete, terminal action planned and awaiting orchestrator execution), `awaiting_internal_children_resolution` (spawned recursive children and awaiting their results), `resolved_for_parent` (a recursive child has completed and its result is ready for its internal parent), `merged_into_new_node` (this node's content has been incorporated into a new merged node), `pruned` (marked as a non-viable path), `final_solution_candidate` (deemed a potential final answer), `awaiting_stateful_action_execution` (specific to `StatefulActionTask`, planned and waiting for conflict resolution and tool call execution), `stateful_action_completed` (tool call executed successfully), `stateful_action_failed` (tool call execution failed, rollback attempted), `stateful_action_blocked_by_retry_limit` (consecutive failures for a specific stateful action exceeded the limit).
        * `parent_ids_graph_structure`: A list of `node_id`s of direct parents in the graph `G`.
        * `child_ids_graph_structure`: A list of `node_id`s of direct children in the graph `G`.
        * `stateful_action_scope`: (Specific to nodes with `Goal.type = StatefulActionTask`) A 5-tuple describing the scope of the stateful action. This is populated by the LLM during the NLI cycle when planning a `StatefulActionTask`. It is used by the orchestrator for conflict detection. For non-`StatefulActionTask` nodes, this is null. The tuple structure is:
            * `action_verb`: A standardized verb indicating the nature of the stateful operation (e.g., `CREATE`, `READ`, `UPDATE`, `DELETE`, `EXECUTE_API`, `LOCK`, `UNLOCK`).
            * `resource_type`: A general category of the resource being acted upon (e.g., `DATABASE_TABLE`, `FILE_SYSTEM_OBJECT`, `API_ENDPOINT`, `NETWORK_SERVICE`, `MEMORY_OBJECT`, `EXTERNAL_PROCESS`).
            * `object_identifier`: A unique name or identifier for the primary entity being affected (e.g., "UserDatabase.UsersTable", "/reports/monthly.csv", "PaymentAPI_v1.0").
            * `target_specifier`: (Optional string, null if not applicable) A more specific part of the `object_identifier` being targeted (e.g., "RecordID:789", "Section:Summary", "Method:ProcessPayment", "UserID:user123").
            * `qualifiers`: (Optional list of key-value pairs, empty if not applicable) Tags or constraints that further define the scope or conditions of the action (e.g., `[{"access_mode": "exclusive"}, {"version": "v2.1"}]`, `[{"transaction_id": "tx12345"}]`, `[{"if_exists": "overwrite"}]`).
        * `stateful_action_failure_counters`: (New field, specific to `StatefulActionTask` nodes) A dictionary mapping a unique identifier for each distinct stateful action (derived from its scope or parameters) to its current consecutive failure count. E.g., `{"CREATE_UserDatabase_JohnDoe": 2}`. This is reset to 0 upon successful execution of that action for this node.
        * `stateful_action_retry_limit_config`: An integer, potentially global or configurable per node/action type, specifying the maximum number of consecutive failures allowed for a given stateful action by this node before it is prohibited from attempting that specific action again (e.g., 3 or 5).

    * **`Action`**: Specifies the node's current processing directive and requested subsequent operations.
        * `current_nli_operation_type`: A string indicating the current Node-Level Internal (NLI) operation being performed or next to be performed for this node. This cycles through a predefined sequence. Examples:
            * `NLI_GenerateInitialPayload`: Generate the initial `State.reasoning_payload` (and `State.stateful_action_scope`, and the `rollback_method` specification within `State.reasoning_payload` if `Goal.type` is `StatefulActionTask`) based on `Goal`.
            * `NLI_RefinePayload`: Iteratively improve/elaborate on `State.reasoning_payload` (and related fields like `stateful_action_scope` or `rollback_method` if applicable).
            * `NLI_SelfEvaluatePayload`: LLM self-evaluates its current `State.reasoning_payload`, populating `Thought.self_evaluation_*` fields.
            * `NLI_PrepareChildInputRationale`: LLM synthesizes insights from its `reasoning_payload` and self-evaluation into `State.child_input_rationale_summary` for potential children.
            * `NLI_PlanTerminalOperation`: LLM reflects on its current Goal, State, and Thought fields to determine the `requested_terminal_operation_type` and its `terminal_operation_parameters`.
        * `requested_terminal_operation_type`: A string indicating the single terminal operation requested by the node after completing its NLI cycle. This operation will be executed by the orchestrator. Examples:
            * `REQ_SpawnChildren_NonRecursive`: Request to spawn one or more non-recursive child nodes.
            * `REQ_SpawnChildren_Recursive_AOT_Decomp`: Request to initiate a recursive AOT-style decomposition by spawning child nodes for sub-goals. This node becomes an `InternalParent`.
            * `REQ_SpawnChildren_Recursive_AGoT_Expand`: Request to initiate a recursive AGoT-style expansion by spawning child nodes to elaborate on aspects of this node's content. This node becomes an `InternalParent`.
            * `REQ_MarkSelfResolvedForParent`: For a recursive child node, signal that it has completed its goal and its result is ready for its `InternalParent`.
            * `REQ_InitiateSearchForSelf`: Request the orchestrator to manage the execution of a search operation, based on a plan developed in `State.reasoning_payload`.
            * `REQ_InitiateSketchExpansionForSelf`: Request the orchestrator to manage the expansion of its sketched `State.reasoning_payload` into a detailed one.
            * `REQ_PruneSelf`: Request to mark itself as a pruned (non-viable) path.
            * `REQ_MarkAsFinalCandidate`: Request to identify itself as a potential final solution to the `original_input_question`.
            * `REQ_ExecuteStatefulAction`: (New operation) Request the orchestrator to execute a stateful tool call based on instructions in `State.reasoning_payload` and the defined `State.stateful_action_scope`. This is specific to nodes with `Goal.type = StatefulActionTask`.
        * `terminal_operation_parameters`: A structure containing parameters specific to the `requested_terminal_operation_type`. For example, for `REQ_SpawnChildren_NonRecursive`, this includes `num_children_k_variable` (AGoT: variable number of children) and a list of `child_verbosity_styles_list` (SoT integration: allowing parent to specify sketch/detailed for each child) and `child_goal_descriptions_list`. For `REQ_ExecuteStatefulAction`, this may include `tool_call_specific_parameters` (e.g., timeout settings, retry policies, credentials references).
        * `operation_status`: A string indicating the status of the action (e.g., `pending_nli`, `nli_step_complete`, `pending_terminal_operation_request`, `terminal_operation_requested_to_orchestrator`).

    * **`Thought`**: Captures LLM self-reflection outputs and orchestrator-driven evaluation results.
        * `reflection_on_current_GS`: The LLM's textual interpretation of its current Goal and State.
        * `self_evaluation_score`: A numerical score (e.g., 0-100) assigned by the LLM to its own `State.reasoning_payload` during an `NLI_SelfEvaluatePayload` step.
        * `self_evaluation_confidence`: The LLM's confidence (e.g., 0-1) in its `self_evaluation_score`.
        * `self_evaluation_rationale`: The LLM's textual rationale for its self-evaluation.
        * `confidence_in_current_approach`: The LLM's overall assessment of the likelihood that its current path will lead to a successful resolution of its `Goal`.
        * `suggestion_for_next_nli_or_terminal_operation`: The LLM's suggestion for the next `Action.current_nli_operation_type` or `Action.requested_terminal_operation_type`.
        * `identified_blockers_or_needs`: Any obstacles or missing information identified by the LLM.
        * `orchestrator_evaluation_score`: A numerical score assigned by the orchestrator (via an external LLM call) to this node's `State.reasoning_payload`. (GoT Scoring mechanism integration)
        * `orchestrator_evaluation_confidence`: The confidence (e.g., probability of score token) associated with the `orchestrator_evaluation_score`. (EGoT Score Enhancing integration)
        * `orchestrator_evaluation_rationale`: The rationale provided for the `orchestrator_evaluation_score`. (EGoT integration)

* **Active Frontier Nodes Queue:** A data structure (e.g., a priority queue) maintained by the orchestrator, holding `Node` instances that are eligible for the Node-Level Internal (NLI) processing cycle.
* **Orchestrator:** A central control unit responsible for:
    * Managing the graph `G` and the lifecycle of all `Node`s.
    * Maintaining and processing the `active_frontier_nodes` queue.
    * Facilitating all LLM calls, applying appropriate temperature controls.
    * Executing all non-NLI operations (Node-Level External, Graph-Level Internal, Graph-Level External), including the `StatefulAction` execution with enhanced conflict resolution and rollback.
    * Enforcing depth-based operational constraints.
    * Propagating the `original_input_question` to all nodes. (EGoT integration)
    * Managing conflict resolution and execution of `StatefulAction` operations for nodes with `Goal.type = StatefulActionTask`, ensuring logical consistency through scope-based conflict detection, prioritized resolution, and rollback.
    * Orchestrating the propagation of `externally_queried_information` after each iteration's action phase.
    * Configuration: `StatefulResolutionAttemptLimit` (e.g., 2 or 3) - the number of times an LLM will be asked to resolve a specific `StatefulAction` conflict group before rule-based priority is applied.

**2. Node Scope and Depth:**

* **Internal-Parent (`P`):** A `Node` `P` that successfully executes a terminal operation of type `REQ_SpawnChildren_Recursive_AOT_Decomp` or `REQ_SpawnChildren_Recursive_AGoT_Expand`, thereby initiating a new recursion scope.
* **Nodes "Internal To `P`":** A node `N` is considered "internal to `P`" if `N.Goal.origin_metadata.internal_parent_node_id` is the `node_id` of `P`. This set includes `P`'s direct recursively spawned children and all their non-recursively spawned descendants.
* **Scope `Sc(P)` of an Internal-Parent `P`:** The subgraph of `G` consisting of `P` itself and all nodes that are internal to `P`. Graph-level operations initiated by `P` or concerning nodes internal to `P` are typically confined to this scope.
* **Node Recursion Depth (`depth_k(v)` or `k_{rec}(v)`):** The value stored in `v.Goal.origin_metadata.depth_k`. Nodes at `depth_k = 0` are root-level.
* **Local Generation Step (`d_{local}(v)`):** The non-recursive generational distance of node `v` from its `InternalParent(v)` (if `depth_k(v) > 0`) or from the graph root (if `depth_k(v) = 0`). This is derived from the length of `v.Goal.origin_metadata.heritage_path_within_scope`.

**3. Depth-Based Controls & Temperature Management:**

* **Maximum Recursion Depth (`max_recursion_depth_config`):** A configurable integer (e.g., 3) defining the deepest recursion level at which nodes can be spawned. Nodes at `depth_k = max_recursion_depth_config` cannot initiate further recursive spawning.
* **Allowed Terminal Operations (`AllowedOps(k)`):** A set of `requested_terminal_operation_type`s and strategic orchestrator-driven graph-level operations (like `GLE_OrchestratorMergeNodes`) permissible for nodes at recursion depth `k`. Enforced: `AllowedOps(k) \subseteq AllowedOps(k-1)` for `k > 0`.
    * **Master Set of Controllable Terminal Operations (`MasterOps`):**
        * `REQ_SpawnChildren_NonRecursive` (R1)
        * `REQ_SpawnChildren_Recursive_AOT_Decomp` (R2)
        * `REQ_SpawnChildren_Recursive_AGoT_Expand` (R3)
        * `REQ_MarkSelfResolvedForParent` (R4)
        * `REQ_InitiateSearchForSelf` (R5)
        * `REQ_InitiateSketchExpansionForSelf` (R6)
        * `REQ_PruneSelf` (R7)
        * `REQ_MarkAsFinalCandidate` (R8)
        * `REQ_ExecuteStatefulAction` (R9 - new operation for stateful tool calling)
        * `GLE_OrchestratorMergeNodes` (O1 - strategic merge initiated by orchestrator)
    * **Depth 0 (`k=0`):**
        `AllowedOps(0) = {R1, R2, R3, R5, R6, R7, R8, R9, O1}`.
        (R4 is not applicable as depth 0 nodes have no internal parent.)
    * **Depth 1 (`k=1`):** Assuming `0  0`)
        (Removed R8 from `AllowedOps(0)`.)
    * **Depth 2 (`k=2`):** Assuming `0 < 2 < max_recursion_depth_config`.
        `AllowedOps(2) = {R1, R2, R3, R5, R6, R7, R9, O1}`. (R4 contextually available)
        (Same as Depth 1.)
    * **Depth 3 (`k=3`):** Assuming `3 == max_recursion_depth_config`.
        `AllowedOps(3) = {R1, R5, R6, R7, R9}`. (R4 contextually available)
        (Removed R2, R3, O1 from `AllowedOps(2)`. Recursive spawning and orchestrator merges are disallowed at max depth.)
    *(Note: `GLE_SynthesizeFinalAnswer` is a global final step, not part of these depth-based reasoning allowances).*

* **Depth-Temperature Factor (`\gamma`):** A constant multiplicative factor, `\gamma \in (0, 1]`, typically less than 1 (e.g., 0.9).
* **Base Temperature at Recursion Depth `k` (`\tau_k`):** For a node `v` at recursion depth `k_{rec}(v)`, the base temperature is calculated as `\tau_{k_{rec}}(v) = \gamma^{k_{rec}(v)} \cdot \tau_0`, where `\tau_0` is a configurable initial base temperature for `depth_k = 0`.
* **EGoT Dynamic Temperature Control (Effective Temperature `t_{eff}(v)`):** For any LLM call related to node `v`, the orchestrator calculates an effective temperature `t_{eff}(v)`:
    $$ t_{eff}(v) = t_{min}(v_{spawner}) + \frac{1}{2} (\tau_{k_{rec}}(v) - t_{min}(v_{spawner})) \left(1 + \cos\left(\frac{\pi \cdot d_{local}(v)}{D_{local\_max}(Sc(InternalParent(v)))}\right)\right) $$
    Where:
    * `\tau_{k_{rec}}(v)` is the recursion-depth-adjusted base temperature for node `v`.
    * `v_{spawner}` is the direct non-recursive node that spawned `v`.
    * `c(v_{spawner}) = s'_{spawner} \cdot (p'_{s\_spawner})^{1/e_c}` is the EGoT-style confidence score of `v_{spawner}`. `s'_{spawner}` is the normalized `v_{spawner}.Thought.orchestrator_evaluation_score` (e.g., scaled to ), and `p'_{s\_spawner}` is the normalized `v_{spawner}.Thought.orchestrator_evaluation_confidence`. `e_c` is Euler's number (approx 2.718).
    * `t_{min}(v_{spawner}) = T_{min\_default} \cdot (1 - \sqrt{1 - (c(v_{spawner}) - 1)^2})` for `c(v_{spawner}) \in ` (using a circular function for confidence-to-min-temp mapping, scaled by a default minimum temperature `T_{min\_default}`, e.g., 0.1). If `v_{spawner}` is not yet evaluated, or if `v` is a root node, `t_{min}(v_{spawner})` defaults to a pre-set low value (e.g., `T_{min\_default}` or `\tau_{k_{rec}}(v) \cdot 0.1`).
    * `d_{local}(v)` is the local generation step of `v`.
    * `D_{local\_max}(Sc(InternalParent(v)))` is the expected maximum local depth within the current scope `Sc(InternalParent(v))` (or the global scope if `depth_k(v)=0`), which can be pre-configured or dynamically estimated.

**4. Atom of Thoughts (AOT) Contraction Frequency Control:**

*   For a node `v` at recursion depth `k = depth_k(v)`, if its `NLI_PlanTerminalOperation` step determines that its current `Goal` or `State.reasoning_payload` is complex and requires further breakdown, the orchestrator may enforce an AOT-style recursive decomposition (i.e., mandate `REQ_SpawnChildren_Recursive_AOT_Decomp` as the terminal action). This enforcement occurs with a probability `P_{AOT\_contract}(k)` that increases with `k`:
    $$ P_{AOT\_contract}(k) = P_{AOT\_min} + (P_{AOT\_max} - P_{AOT\_min}) \cdot \left(1 - e^{-\lambda_{AOT} \cdot k}\right) $$
    Where `P_{AOT\_min}` is a base probability (e.g., 0.1), `P_{AOT\_max}` is the maximum probability (e.g., 0.9), and `\lambda_{AOT}` is a positive constant controlling the rate of increase with depth `k` (e.g., 0.5). This occurs before checking `AllowedOps(k)`.

**5. Operation Classification & Execution:**

Operations are classified based on their driver (node's internal plan vs. external agent) and scope (single node vs. multiple nodes). All operations, once planned by a node or decided by the orchestrator, are executed or mediated by the orchestrator.

* **Node-Level Internal (NLI):** Operations driven by a node's LLM to act upon itself. The orchestrator facilitates these by making LLM calls for the active node.
    * `NLI_GenerateInitialPayload`, `NLI_RefinePayload`, `NLI_SelfEvaluatePayload`, `NLI_PrepareChildInputRationale`, `NLI_PlanTerminalOperation`.
    * These operations aim to bring the node itself closer to fulfilling its `Goal`. They are generally frequent and modify only the node's own `State`, `Action`, and `Thought` fields. For `StatefulActionTask` nodes, `NLI_GenerateInitialPayload` or `NLI_RefinePayload` will include the LLM defining the `State.stateful_action_scope` 5-tuple, the tool call instructions, and the `rollback_method` in `State.reasoning_payload`.

* **Node-Level External (NLE):** Operations driven by the orchestrator (or conceptually by an "external node" like a parent awaiting results) that affect a single target node.
    * `NLE_OrchestratorEvaluateNode(target_node)`: The orchestrator prompts an LLM (using global evaluation methodologies and `t_{eff}(target_node)`) with `target_node.Goal` and `target_node.State.reasoning_payload`. Results update `target_node.Thought.orchestrator_evaluation_*` fields. (Implements GoT Scoring Mechanism; uses EGoT confidence for score enhancement). If the evaluation confidence is below a threshold, re-evaluation can be triggered.
    * `NLE_PropagateResolvedDataToInternalParent(resolved_child_node)`: If `resolved_child_node` (which was a recursive child, search task, or expansion task) completes (status `resolved_for_parent`), its primary output (e.g., `State.reasoning_payload` or `State.externally_queried_information`) is transferred to the `State.externally_queried_information` field of its `InternalParent(resolved_child_node)`. The orchestrator then reactivates the `InternalParent` node. This is crucial for AOT Contraction.

* **Graph-Level Internal (GLI):** Operations initiated by a node (via `requested_terminal_operation_type`) that affect multiple nodes but are confined within the scope `Sc(InternalParent(node))` of the initiating node's internal parent, or operations that define a new internal scope.
    * `GLI_Execute_SpawnChildren_NonRecursive(parent_node, params)`: The `parent_node` (after its NLI cycle) requests to spawn new non-recursive child nodes. Parameters include `num_children_k_variable` (AGoT: variable number of children) and `child_verbosity_styles_list`. New children inherit `parent_node.Goal.origin_metadata.internal_parent_node_id` and `depth_k`. The orchestrator checks if this operation is in `AllowedOps(depth_k(parent_node))`. New nodes are added to `active_frontier_nodes`.
    * `GLI_Execute_SpawnChildren_Recursive_AOT_Decomp(parent_node, params)`: The `parent_node` requests to become an `InternalParent` and spawn recursive children for AOT-style sub-goal decomposition. New children get `depth_k = parent_node.depth_k + 1`, and their `internal_parent_node_id` is `parent_node.node_id`. Temperature `t_{eff}` for these children will reflect the new depth. Orchestrator checks `AllowedOps(depth_k(parent_node))`. `parent_node.State.node_status` changes to `awaiting_internal_children_resolution`.
    * `GLI_Execute_SpawnChildren_Recursive_AGoT_Expand(parent_node, params)`: Similar to AOT decomposition, but children are for AGoT-style expansion/elaboration.
    * `GLI_Execute_PropagatePruningToInternalDescendants(node_to_prune)`: If `node_to_prune` is marked for pruning, the orchestrator prunes its non-recursive descendants within the same internal scope `Sc(InternalParent(node_to_prune))`.
    * `GLI_Execute_InitiateSearchForParent(parent_node, search_plan_params)`: `parent_node` requests to spawn a special "search" child node. This child is internal to `InternalParent(parent_node)` and has the same `depth_k`. Its goal is to execute the search. Results propagate back via `NLE_PropagateResolvedDataToInternalParent`.
    * `GLI_Execute_InitiateSketchExpansionForParent(parent_node_sketch, expansion_plan_params)`: Similar to search, but for expanding a sketch.

* **Graph-Level External (GLE):** Operations initiated by the orchestrator (or conceptually by a node if its `requested_terminal_operation_type` implies a global effect allowed at `depth_k=0`) that affect multiple nodes, potentially across different internal scopes or at the root level of the graph.
    * `GLE_OrchestratorMergeNodes(nodes_to_merge, merge_logic_prompt_config)`: The orchestrator selects a set of `nodes_to_merge` (often guided by GoT Ranking based on `Thought.orchestrator_evaluation_score` and `_confidence`). A new `MergedNode` is created. Its `Goal`, initial `State.reasoning_payload`, `depth_k`, and `internal_parent_node_id` are determined by an LLM call guided by `merge_logic_prompt_config` and the content of `nodes_to_merge`. (Implements GoT Aggregation). The orchestrator checks if merging is allowed for the effective depth of the new node. The new node is added to `active_frontier_nodes`.
    * `GLE_SynthesizeFinalAnswer(candidate_leaf_nodes_list)`: (EGoT Aggregation of multiple leaf Answering nodes). The orchestrator selects `final_solution_candidate` nodes (conceptually equivalent to EGoT's "leaf Answering nodes"). An LLM is prompted to synthesize a final output from their `State.reasoning_payload`. This is typically a terminal operation for the entire graph.
    * `GLE_PropagatePruningToEntireInternalScope(internal_parent_node_to_prune)`: If an `InternalParent` node is pruned, the orchestrator prunes all nodes internal to it (i.e., the entire scope `Sc(internal_parent_node_to_prune)`).
    * `GLE_ExecuteStatefulActionsWithConflictResolution(candidate_stateful_action_nodes)`: (Enhanced orchestrator-managed GLE operation). This operation takes a list of `active_frontier_nodes` that have requested `REQ_ExecuteStatefulAction`.
        1. **Conflict Detection:** For all pairs in `candidate_stateful_action_nodes`, check for overlapping `State.stateful_action_scope` using a function `ScopesOverlap(scope_A, scope_B)`.
        2. **Conflict Resolution:** For each identified conflict group `C_g`:
            * Initialize `resolution_attempts = 0`.
            * While `resolution_attempts < StatefulResolutionAttemptLimitConfig` and more than one action in `C_g` is pending selection:
                * Orchestrator prompts an LLM with descriptions of the conflicting actions (goals, reasoning payloads, scopes, `rollback_method` specifications, evaluation scores, depth) from `C_g`. The LLM is tasked to choose at most one action to execute.
                * Increment `resolution_attempts`.
                * If LLM selects one action: Mark it as chosen for `C_g`.
                * If LLM fails to select one (e.g., selects none, or more than one, or an invalid choice): continue loop if attempts remain.
            * **If LLM resolution failed after `StatefulResolutionAttemptLimitConfig` attempts and conflict persists in `C_g`:**
                * Apply **Priority-Based Resolution** for `C_g`:
                    * Calculate a priority score `P(v)` for each node `v \in C_g` based on a weighted combination or lexicographical order of: `v.Thought.orchestrator_evaluation_score` (higher better), `v.Thought.orchestrator_evaluation_confidence` (higher better), `v.Thought.self_evaluation_score` (higher better), `v.Thought.self_evaluation_confidence` (higher better), and `v.Goal.origin_metadata.depth_k` (lower better).
                    * Select the node `v*` with the highest `P(v*)`.
                    * If ties exist for `P(v*)` among multiple nodes `C_tie \subseteq C_g`:
                        * Orchestrator makes one LLM call to choose one action from `C_tie`.
                        * If LLM fails to break the tie: select one node from `C_tie` randomly.
                * Mark the chosen node as the one to execute from `C_g`.
            * For all non-selected nodes `v_{ns} \in C_g` (those not chosen by LLM or priority rule):
                * `v_{ns}.State.node_status` becomes `stateful_action_failed`.
                * `v_{ns}.State.externally_queried_information` is updated with an LLM-generated justification (or a system message if priority rule was used) for non-selection.
                * Increment `v_{ns}.State.stateful_action_failure_counters` for the specific action. If this exceeds `v_{ns}.State.stateful_action_retry_limit_config`, set `v_{ns}.State.node_status` to `stateful_action_blocked_by_retry_limit`.
        3. **Parallel Execution & Synchronization:** Let `S_executable` be the set of nodes from `candidate_stateful_action_nodes` that were non-conflicting or chosen through conflict resolution (and not blocked by retry limits).
            * The orchestrator executes their `StatefulAction`s (tool calls) in parallel.
            * The orchestrator *waits* for all actions in `S_executable` to complete (successfully or with failure and attempted rollback) before proceeding to subsequent phases of the iteration (data propagation, merge, pruning).
            * For each executed action on node `v_exec \in S_executable`:
                * If successful: `v_exec.State.externally_queried_information` is updated with the result, `v_exec.State.node_status` to `stateful_action_completed`, and relevant `v_exec.State.stateful_action_failure_counters` reset to 0.
                * If failed: Orchestrator attempts to execute the `rollback_method` specified in `v_exec.State.reasoning_payload`. `v_exec.State.externally_queried_information` updated with failure details and rollback status. `v_exec.State.node_status` to `stateful_action_failed`. Increment relevant `v_exec.State.stateful_action_failure_counters`. If this exceeds `v_exec.State.stateful_action_retry_limit_config`, set `v_exec.State.node_status` to `stateful_action_blocked_by_retry_limit`.
    * `GLE_PropagateExternallyQueriedInformation`: (New orchestrator-managed GLE operation). After all actions in an iteration (including stateful actions) have resolved, the orchestrator places an LLM call. This LLM call evaluates all `State.externally_queried_information` fields from recently updated nodes (e.g., search results, stateful action outcomes, recursive sub-graph results) to determine which pieces of information are relevant and should be propagated to which other destination nodes in the graph. The LLM generates a propagation plan (source_node_id, information_snippet, destination_node_id, destination_field_to_update). The orchestrator then executes this plan, updating the `State` of destination nodes (e.g., adding to their `State.reasoning_payload` or a dedicated "propagated_info" field). This allows for more flexible information flow than just parent-child propagation.

**GoT Ranking Mechanism:** The orchestrator employs ranking based on `Thought.orchestrator_evaluation_score` and `Thought.orchestrator_evaluation_confidence` when:
1. Selecting nodes for `GLE_OrchestratorMergeNodes`.
2. Choosing which `final_solution_candidate` nodes to include in `GLE_SynthesizeFinalAnswer`.
3. Optionally, for prioritizing nodes in the `active_frontier_nodes` queue.
4. As part of the priority calculation during `StatefulAction` conflict resolution if LLM attempts fail.

**6. Orchestrator Workflow:**

1. **Initialization:**
    * Define global methodologies, `AllowedOps(k)` for `k=0...max_recursion_depth_config`, `\tau_0`, `\gamma`, AOT params, `stateful_action_retry_limit_config`, `StatefulResolutionAttemptLimit`.
    * **EGoT: Use of multiple root nodes:** Create initial `Node`(s) at `depth_k = 0`. Add to `active_frontier_nodes`.

2. **Processing Cycle (Iteration):**
    a. **Node Internal Processing (NLI) Phase:**
        i. For each `CurrentNode` in `active_frontier_nodes`:
            1. Set `CurrentNode.State.node_status = internal_processing`.
            2. Orchestrator calculates `t_{eff}(CurrentNode)`.
            3. Orchestrator facilitates NLI cycle. This includes populating `State.stateful_action_scope` and defining `rollback_method` in `State.reasoning_payload` if `CurrentNode.Goal.type` is `StatefulActionTask`.
            4. Orchestrator applies AOT Contraction Frequency Control logic.
            5. `CurrentNode.State.node_status` becomes `awaiting_orchestrator_action`.
    b. **Orchestrator Operations Phase (End of Iteration - executed sequentially in this order):**
        i. **NLE - Orchestrator Evaluation:** Perform `NLE_OrchestratorEvaluateNode` for relevant nodes `awaiting_orchestrator_action`.
        ii. **GLE - Stateful Action Conflict Resolution & Execution:**
            1. Perform `GLE_ExecuteStatefulActionsWithConflictResolution` for all nodes that requested `REQ_ExecuteStatefulAction`. This entire step (including parallel execution and waiting for all to resolve) completes before proceeding.
        iii. **GLE - Data Propagation:**
            1. Perform `GLE_PropagateExternallyQueriedInformation` based on newly available `State.externally_queried_information` from all actions in the current iteration.
        iv. **GLI/GLE - Execute Other Requested Terminal Operations:** For nodes `awaiting_orchestrator_action` not handled by stateful action execution (or whose stateful action failed/was blocked but they might have an alternative non-stateful terminal action plan, if allowed by logic):
            1. Verify operation is in `AllowedOps(depth_k)`.
            2. Execute (e.g., `GLI_Execute_SpawnChildren`, `GLI_Execute_InitiateSearchForParent`).
            3. Handle `REQ_MarkSelfResolvedForParent` via `NLE_PropagateResolvedDataToInternalParent`.
        v. **GLE - Orchestrator-Initiated Pruning and Merges (performed *after* StatefulAction resolution and data propagation):**
            1. The orchestrator may initiate `GLE_PropagatePruningToEntireInternalScope` if an `InternalParent` node was pruned during previous steps.
            2. The orchestrator may initiate `GLE_OrchestratorMergeNodes`. New merged nodes enter `active_frontier_nodes`.
    c. **Reactivation of Parent Nodes:** If an `InternalParent` node was awaiting results and dependencies are met:
        1. Orchestrator changes its `State.node_status` to `active_frontier`.
        2. Its `Action.current_nli_operation_type` is set (e.g., to `NLI_RefinePayload` for AOT Contraction).
        3. Parent node is re-added to `active_frontier_nodes`.

3. **Termination and Final Output:** Loop until global termination criteria. Final answer produced by `GLE_SynthesizeFinalAnswer`.

This UGRF version provides a highly robust mechanism for incorporating stateful world interactions by defining clear scopes, implementing a multi-stage conflict resolution strategy (LLM attempts followed by priority rules), handling failures with rollbacks and retry limits, and synchronizing these actions before further graph operations like data propagation, merging, or pruning.