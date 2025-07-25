from crewai.flow.flow import Flow, start , listen # type: ignore
import time

class SimpleFLow(Flow):

    @start()
    def function1(self):
        print("step 1 .....")
        time.sleep(1)

    @listen(function1)
    def function2(self):
        print("step 2 ...")
        time.sleep(2)

    @listen(function2)
    def function3(self):
        print("step 3....")
        time.sleep(3)


def kickoff():
    print("Hello world")
    obj = SimpleFLow()
    obj.kickoff()