import os
import imp
import xml.etree.ElementTree as ET

class Agent():
    def __init__(self, grid_size):
        # Placeholders
        self.agent_module_types = {}
        self.agent_class_types = {}
        self.agent_type = -1

        # Load the setting file and parse
        settings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.xml')
        self.load_xml_settings(settings_file)

        # Dynamically load the agent and instantiate the correct agent
        fp, path, desc = imp.find_module(os.getcwd()+'\\src\\Agents\\'+self.agent_module_types[self.agent_type])
        module = imp.load_module(self.agent_module_types[self.agent_type], fp, path, desc)
        agent_class = getattr(module,self.agent_class_types[self.agent_type])
        self._agent = agent_class(grid_size)

    def get_state(self, state_id):
        return self._agent.get_unique_state(state_id)

    def set_state(self, state_id, value):
        return self._agent.set_state(state_id, value)
    
    def update(self, state_id, reward):
        return self._agent.update(''.join(str(i) for i in state_id), reward)

    # Load the XML settings and parse it
    def load_xml_settings(self, settings_file):
        settings_tree = ET.parse(settings_file)
        settings_root = settings_tree.getroot()
        for child in settings_root:
            if child.tag == 'Agent_Types':
                for agent_type in child:
                    self.agent_module_types[int(agent_type.attrib['id'])] = agent_type.attrib['module_name']
                    self.agent_class_types[int(agent_type.attrib['id'])] = agent_type.attrib['class_name']
            if child.tag == 'Agent_Selection':
                self.agent_type = int(child.attrib['id'])