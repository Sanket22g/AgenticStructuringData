from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent

from project_job_change.tools.custom_tool import MyCustomTool, PDFExtractorTool


@CrewBase
class ProjectJobChange():
    """PDF Data Extraction and Verification Crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    # ─── Agents ─────────────────────────────────────────────────────────────

    @agent
    def pdf_extractor_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['pdf_extractor_agent'],  # type: ignore[index]
            tools=[PDFExtractorTool()],
            verbose=True,
        )

    @agent
    def data_verifier_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['data_verifier_agent'],  # type: ignore[index]
            tools=[MyCustomTool()],
            verbose=True,
        )

    # ─── Tasks ──────────────────────────────────────────────────────────────

    @task
    def pdf_extraction_task(self) -> Task:
        return Task(
            config=self.tasks_config['pdf_extraction_task'],  # type: ignore[index]
        )

    @task
    def data_verification_task(self) -> Task:
        return Task(
            config=self.tasks_config['data_verification_task'],  # type: ignore[index]
            context=[self.pdf_extraction_task()],  # receives raw text + JSON from extraction task
        )

    # ─── Crew ───────────────────────────────────────────────────────────────

    @crew
    def crew(self) -> Crew:
        """Creates the PDF extraction and verification crew"""
        return Crew(
            agents=self.agents,   # Automatically populated by @agent decorators
            tasks=self.tasks,     # Automatically populated by @task decorators
            process=Process.sequential,
            verbose=True,
        )
