import abc

from album.runner import AlbumRunner
from album.runner.model.solution_script import SolutionScript


class ScriptCreator(abc.ABC):
    """Abstract class for all ScriptCreator classes. Holds methods shared across all ScriptCreator classes."""

    def __init__(self):
        pass

    @abc.abstractmethod
    def get_execution_block(self, solution_object) -> str:
        """The custom code for all scripts created by this class"""
        pass

    def create_script(self, solution_object, argv) -> str:
        """Creates the script with the execution_block of the concrete instance of the class"""
        execution_block = self.get_execution_block(solution_object)

        script = SolutionScript(solution_object, execution_block, argv)

        return script.create_solution_script()


class ScriptCreatorInstall(ScriptCreator):
    def __init__(self):
        super().__init__()

    def get_execution_block(self, _):
        return "\nget_active_solution().install()\n"


class ScriptCreatorUnInstall(ScriptCreator):
    def __init__(self):
        super().__init__()

    def get_execution_block(self, _):
        return "\nget_active_solution().uninstall()\n"


class ScriptCreatorRun(ScriptCreator):
    def __init__(self, pop_solution: bool = False, execution_callback=None):
        super().__init__()
        self.pop_solution = pop_solution

        if execution_callback is not None and callable(execution_callback):
            self.execution_callback = execution_callback
        else:
            self.reset_callback()

    def reset_callback(self):
        self.execution_callback = lambda: ""

    def get_execution_block(self, solution_object: AlbumRunner):
        execution_block = "\nmodule_logger().info(\"Starting %s\")" % solution_object["name"]
        execution_block += "\nmodule_logger().info(\"\")\n"
        if solution_object['run'] and callable(solution_object['run']):
            execution_block += "\nget_active_solution().run()\n"
        else:
            raise ValueError("No \"run\" routine specified for solution \"%s\"! Aborting..." % solution_object["name"])

        # used to insert code blocks during runtime after run but before close. Used when solution serves as parent.
        execution_block += self.execution_callback()

        if solution_object['close'] and callable(solution_object['close']):
            execution_block += "\nget_active_solution().close()\n"

        execution_block += "\nmodule_logger().info(\"\")"
        execution_block += "\nmodule_logger().info(\"Finished %s\")\n" % solution_object["name"]

        if self.pop_solution:
            execution_block += "\npop_active_solution()\n"

        return execution_block


class ScriptCreatorRunWithParent(ScriptCreatorRun):
    def __init__(self, parent_script_creator: ScriptCreatorRun, child_solution_list: list, child_args: list):
        super().__init__()
        self.parent_script_creator = parent_script_creator
        self.child_solution_list = child_solution_list
        self.child_args = child_args

    def get_execution_block(self, solution_object) -> str:
        self.parent_script_creator.execution_callback = self.create_child_scripts
        execution_block = self.parent_script_creator.get_execution_block(solution_object)
        self.parent_script_creator.reset_callback()

        return execution_block

    def create_child_scripts(self):
        children_block = ""

        for child_solution, child_arg in zip(self.child_solution_list, self.child_args):
            s = ScriptCreatorRun(pop_solution=True)
            child_script = s.create_script(child_solution, child_arg)

            children_block += child_script
        return children_block


class ScriptTestCreator(ScriptCreatorRun):
    def __init__(self):
        super().__init__()

    def get_execution_block(self, solution_object):
        execution_block = "\nd = get_active_solution().pre_test()\n"
        execution_block += "\nsys.argv = sys.argv + [\"=\".join([c, d[c]]) for c in d]\n"

        # parse args again after pre_test() routine if necessary.
        if not solution_object["args"] == "pass-through":
            execution_block += "\nget_active_solution().args = parser.parse_args()\n"

        execution_block += super().get_execution_block(solution_object)
        execution_block += "\nget_active_solution().test()\n"

        return execution_block
