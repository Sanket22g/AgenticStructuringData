# AgenticStructuringData

AgenticStructuringData is a small example project demonstrating a multi-agent architecture (a "crew") using the crewAI-style pattern. It shows how multiple agents, each with specific roles and tools, collaborate to complete tasks defined in configuration files.

**Goals:**
- Produce outputs in the company's required Excel format (see `src/project_job_change/tools/custom_tool.py`). The crew's primary purpose is to extract, normalize, validate, and export tabular records into an Excel workbook that matches the company's column/format requirements.
- Provide a runnable pipeline that converts source data (PDFs, text, or structured sources) into the company's Excel template with correct headers, types, and validation.
- Make it easy for engineers to adapt mappings, the output file path, and sheet name via task/agent inputs so the export integrates with downstream company systems.

## Company Excel output

This project includes a deterministic helper tool that writes rows in the exact schema the company expects. See `src/project_job_change/tools/custom_tool.py` for the implementation and the full list of columns:

- `company__name`, `product_name`, `opening_units`, `purchase_units`, `purchase_free`, `purchase_return`, `sales_units`, `sales_free`, `sales_return`, `closing_units`, `stock_code`, `from_date`, `to_date`, `ptr`, `mrp`, `rate`, `value`, `company_division_name`, `company_division_code`, `company_division_type`, `company_division_region`, `company_division_state`, `company_division_city`, `company_division_area`, `company_division_zone`, `company_division_territory`, `company_division_channel`, `company_division_subchannel`.

How it is used:

- Agents (or tasks) gather and normalize data into a list of records (one dict per row) matching the column names above.
- The crew wires the `json_to_excel` tool (implemented in `custom_tool.py`) to save the records into an `.xlsx` file. The tool validates rows against the expected types and writes a header row with formatting.
- Configure output path and worksheet name via the task inputs (e.g. `output_path` and `sheet_name`) so the produced file fits the company's ingestion pipeline.

Quick example (agent / task passes to tool):
h
```python
# records = [ {"company_division_name": "Div A", "product_name": "P1", ...}, ... ]
# call the tool with records and optional path
result = json_to_excel.run(records=records, output_path="F:/project_job_change/company_report.xlsx", sheet_name="Report")
```

Validation and mapping notes:

- Use the crew or a preprocessing agent to map source field names to the column keys listed above before calling the tool.
- The tool returns an error message if any row fails validation — use that to log and correct source mapping.
- Adjust date formats and numeric types in the preprocessing step to ensure the generated Excel file meets company validation rules.

## Key files
- [src/project_job_change/crew.py](src/project_job_change/crew.py) — crew definition and agent wiring
- [src/project_job_change/main.py](src/project_job_change/main.py) — simple runner/entrypoint
- [src/project_job_change/config/agents.yaml](src/project_job_change/config/agents.yaml) — agent definitions
- [src/project_job_change/config/tasks.yaml](src/project_job_change/config/tasks.yaml) — task definitions
- [src/project_job_change/tools/custom_tool.py](src/project_job_change/tools/custom_tool.py) — example helper tool
- [tests/test_tool.py](tests/test_tool.py) — simple unit test example

## Multi‑Agent Architecture (How it works)

This project follows a crew/agent pattern. At a high level:

- **Crew (Coordinator):** `ProjectJobChange` (in `crew.py`) composes agents and tasks into a runnable unit. It is responsible for assembling agents, setting up tools and configuration, and starting execution.
- **Agents:** Individual AI workers with a role, goal, and optional tools. Each agent focuses on a subtask (researcher, writer, tester, etc.). Agent behavior and tool access are configured in `config/agents.yaml`.
- **Tasks:** Declarative descriptions of work items (inputs, expected output, guardrails). Tasks live in `config/tasks.yaml` and are assigned to agents by the crew at runtime.
- **Tools:** Lightweight helper modules (see `tools/custom_tool.py`) that agents can call to perform deterministic work (file I/O, parsing, API wrappers).
- **Manager / Delegation:** In hierarchical setups the crew can include a manager agent that delegates tasks to specialist agents, balances work, and aggregates results.
- **Guardrails & Validation:** Tasks may include guardrails (validation rules) so outputs are checked and retried or escalated when necessary.

Execution flow (typical):

1. Start the crew via the entrypoint (`main.py`) or with `crewai run`.
2. The crew reads `agents.yaml` and `tasks.yaml` to construct the agent instances and task list.
3. The crew kicks off the execution: managers (if present) assign tasks or agents pick tasks based on definitions.
4. Agents call tools to perform deterministic sub-steps and may use LLMs for reasoning when configured.
5. Results are validated against task guardrails and persisted or routed to follow-up tasks.

Design notes:

- Keep agents small and focused: each agent encapsulates a single responsibility.
- Use tools for repeatable code (parsing, fetching, deterministic transforms).
- Keep configuration in `config/*.yaml` so behavior can be changed without code edits.

## Running locally

Recommended steps to run and develop locally (Windows examples shown):

1. Create a virtual environment and activate it:

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
```

2. Install the package in editable mode (this will pick up `pyproject.toml`):

```powershell
pip install -e .
```

3. Run the example crew runner:

```powershell
python -m project_job_change.main
```

4. Run tests:

```powershell
pip install -U pytest
pytest -q
```

Notes:
- `main.py` contains a minimal `run()` that demonstrates starting the crew. Update its `inputs` dict for your data paths.
- If you prefer using the CrewAI CLI (`crewai`), you can also run `crewai run` if the project is configured for it.

## Development tips

- Edit agent and task definitions in `config/agents.yaml` and `config/tasks.yaml` to change behavior.
- Add deterministic helpers to `src/project_job_change/tools/` and expose them to agents via the crew wiring in `crew.py`.
- Keep guardrails narrow and test them with unit tests in `tests/`.

## Contributing

Feel free to open issues or pull requests. Small improvements that clarify agent responsibilities or add tests are especially welcome.

---
Made as a compact reference for understanding and extending the multi-agent crew in this repository
