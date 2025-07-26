from crewai.flow.flow import Flow , start , listen # type: ignore
from dotenv import load_dotenv , find_dotenv # type: ignore
from litellm import completion # type: ignore
from uv_03.crews.teaching.teaching_crew import TeachingCrew

_:bool = load_dotenv(find_dotenv())
class PanaFlow(Flow):
    @start()
    def generate_topic(self):
        response = completion(
            model="gemini/gemini-2.0-flash",
            messages=[
                {
                    "role" : "user",
                    "content" : """Best AI Agents"""
                }
            ],
            max_tokens=100,
            temperature=0.5
        )

        self.state["topic"] = response['choices'][0]['message']['content']
        print(f"Step 1 topic : {self.state['topic']}")
    
    @listen(generate_topic)
    def generate_content(self):
        result = TeachingCrew().crew().kickoff(
            inputs={
                "topic":self.state['topic']
            }
        )
        print(result.raw)
        return


def main():
    flow = PanaFlow()
    response = flow.kickoff()
    print("Reponse " , response)

if __name__ == "__main__":
    main()