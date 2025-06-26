b. `type`: A string categorizing the goal, guiding the orchestrator's prompting strategy and allowed operations. Examples include: `InitialQuery`, `RecursiveSubProblem_AOT_Decomposition` (initiating Atom of Thoughts style decomposition), `RecursiveSubProblem_AGoT_Expansion` (initiating Adaptive Graph of Thoughts style expansion), `SearchTask` (planning and executing a search), `ExpansionTask` (planning and executing a sketch expansion), `MergeCandidate` (signifying the node's content is a candidate for merging), `AOT_ContractionTask` (synthesizing results from AOT sub-goals), `StatefulActionTask` (a new type specifically for defining and requesting the execution of stateful tool-calling operations that affect the world state).
        c. **JUST MAKE A METADATA STRUCTURE** `origin_metadata`: A structure containing metadata about the node's creation and position within the graph:
            * `node_id`: A unique identifier for this node.
            * `parent_node_id`: The `node_id` of the node that directly spawned this one through a non-recursive operation. Can be the same as `internal_parent_node_id` if spawned directly by its internal parent. Null for root nodes.
            * `internal_parent_node_id`: The `node_id` of the node that initiated the current recursion scope to which this node belongs. Null if the node is at recursion depth 0.
            * `depth_k` (also `k_{rec}(v)`): An integer representing the recursion depth of node `v`. Root nodes (nodes with no `internal_parent_node_id`) are at `depth_k = 0`. Recursively spawned children have `depth_k` incremented by 1 from their recursive spawner. Non-recursive children inherit the `depth_k` of their spawner.
            * `heritage_path_within_scope`: (AGoT integration) A list of tuples, e.g., `[(step_1, index_1), (step_2, index_2), ...]`, uniquely identifying the node's non-recursive lineage from its `internal_parent_node_id` (or from the root if `depth_k = 0`). Each tuple represents a generation step and the sibling index at that step within the current recursion scope.

In the case of a `StatefulActionTask`, this payload contains:
    1. Detailed instructions for the tool call (e.g., API request body, script to execute).
    2. A specification of the `rollback_method`: A description of the compensating action or state restoration instructions to be executed by the orchestrator if the stateful action fails or needs to be undone.

* `child_input_rationale_summary`: An aggregated summary of rationales or key insights prepared by this node (during its internal processing) intended as contextual input for any child nodes it might subsequently spawn.
* `verbosity_style`: A string indicating the format of `reasoning_payload`: `sketch` (with sub-types: `conceptual_chaining`, `chunked_symbolism`, `expert_lexicon` - SoT integration) or `detailed`. For newly created child nodes, this is specified by their parent node's LLM during its planning phase.
* `llm_parameters_used`: A record of LLM parameters used for generating content within this node, including the `effective_temperature_t_eff(v)` (defined later).

