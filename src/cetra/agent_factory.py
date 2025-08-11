from cetra.models import AgentConfig
import controlflow as cf

class AgentFactory:

    def create_agents(self, workflow_config_agents:dict[str, AgentConfig])->dict[str, cf.Agent]:
        ret = {}
        for name, agent_config in workflow_config_agents.items():
            ret[name] = cf.Agent()


