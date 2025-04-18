from pymodaq_gui.parameter import ioxml, Parameter, ParameterTree
from pymodaq_gui.parameter.pymodaq_ptypes import registerParameterType, GroupParameter
from pymodaq_gui.utils import select_file
from pymodaq.utils.daq_utils import get_plugins
from pymodaq_utils import utils

from pymodaq_gui.parameter.utils import get_param_dict_from_name

from pymodaq.control_modules.move_utility_classes import params as daq_move_params
from pymodaq.control_modules.viewer_utility_classes import params as daq_viewer_params

DAQ_Move_Stage_type = get_plugins('daq_move')
DAQ_0DViewer_Det_types = get_plugins('daq_0Dviewer')
DAQ_1DViewer_Det_types = get_plugins('daq_1Dviewer')
DAQ_2DViewer_Det_types = get_plugins('daq_2Dviewer')
DAQ_NDViewer_Det_types = get_plugins('daq_NDviewer')



class ConfiguratorScalableActuatorGroup(GroupParameter):
    """
    """

    def __init__(self, **opts):
        opts['type'] = 'actuator_config'
        opts['addText'] = "Add"
        opts['addList'] = [mov['name'] for mov in DAQ_Move_Stage_type]
        super().__init__(**opts)

    def addNew(self, name):
        """
            Add a child.

            =============== ===========
            **Parameters**   **Type**
            *typ*            string
            =============== ===========
        """
        name_prefix = 'actuator'
        child_indexes = [int(par.name()[len(name_prefix) + 1:]) for par in self.children()]
        if not child_indexes:
            newindex = 0
        else:
            newindex = max(child_indexes) + 1

        params = daq_move_params

        parent_module = utils.find_dict_in_list_from_key_val(DAQ_Move_Stage_type, 'name', name)
        class_ = getattr(getattr(parent_module['module'], 'daq_move_' + name),
                         'DAQ_Move_' + name)
        params_hardware = getattr(class_, 'params')


        child = {'title': name, 'name': f'{name_prefix}{newindex:02.0f}', 'type': 'group', 'removable': True,
                 'renamable': False,
                 'children': [
                     {'title': 'Value?:', 'name': 'move_abs_value', 'type': 'float', 'value': 0.,
                      'suffix': 'mm'},
                     {'title': 'Settings?:', 'name': 'settings', 'type': 'group', 'children': params_hardware},
                 ],
                 }

        self.addChild(child)

registerParameterType('actuator_config', ConfiguratorScalableActuatorGroup, override=True)


def main():
    from pymodaq_gui.utils.utils import mkQApp
    app = mkQApp('Configurator')
    param = Parameter.create(name='moves', type='actuator_config')
    tree = ParameterTree()
    tree.setParameters(param, showTop=False)
    tree.show()
    app.exec()


if __name__ == '__main__':
    main()
