from locust import task, between
from OdooLocust.OdooLocustUser import OdooLocustUser
from odooLocust import OdooTaskSet
from OdooTaskSet import GenericTaskSet

class PartnerGenericTaskset(GenericTaskSet):
    model_name='res.partner'

# requires patch in send for odoolib version 2.0.0
# res = odoolib.rpc.json_rpc(self.url, "call", {"service": service_name, "method": method, "args": args})

class TestUser(OdooLocustUser):
    weight = 1  # weighted picking of user classes if multiple exist
    wait_time = between(1, 5)  # wait 1 - 5 between tasks
    database = '???'

    # weighted task; parameter between () indicates weight
    # @task(x) is x times more likely to be called than task(1)
    # default parameterless @task = @task(1)
    # only methods with @task get executed as tasks by locust
    @task
    def run_task_1(self):
        # model = self.client.get_model('ir.model')
        # model.read([1])
        pass

    # tasks can be tagged
    # including or excluding tags can be done with
    # --tags <tag1> <tag2> .. -> run tasks with these tags
    # --exclude-tags <tag1> <tag2> run tasks without excluded tags
    # exclude > include
    @tag('load')
    @task
    def run_tagged(self):
        pass

    # external tasksets can be loaded as extra tasks to use
    # {taskset class: weight}
    # tasks = {PartnerGenericTaskset: 1}
