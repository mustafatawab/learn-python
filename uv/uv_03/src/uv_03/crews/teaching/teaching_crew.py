from crewai import Agent , Task , Crew # type: ignore
from crewai.project import CrewBase, agent , crew,task #type: ignore

@CrewBase
class TeachingCrew:
    agent_config = 'config/agents.yaml'
    task_config = 'config/tasks.yaml'

    @agent
    def sir_zia_agent(self) -> Agent:
        return Agent(
            config=self.agent_config['sir_zia']

        )


    @task
    def describe_topic_task(self) -> Task:
        return Task(
            config=self.task_config['describe_topic']

        )
    


    @crew
    def teaching_crew(self)->Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True
        )
