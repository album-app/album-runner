import abc

from album.runner import AlbumRunner
from album.runner.model.solution_script import SolutionScript


class ScriptCreator(abc.ABC):
    """Abstract class for all ScriptCreator classes. Holds methods shared across all ScriptCreator classes."""

    def __init__(self, execution_callback=None):
        self.execution_block = None
        self.common_inset = None
        if execution_callback is not None and callable(execution_callback):
            self.execution_callback = execution_callback
        else:
            self.reset_callback()

    def reset_callback(self):
        self.execution_callback = lambda: ""

    @abc.abstractmethod
    def set_execution_block(self, solution_object):
        """The custom code for all scripts created by this class"""
        pass

    @abc.abstractmethod
    def set_common_inset(self, solution_object):
        pass

    def create_script(self, solution_object, argv) -> str:
        """Creates the script with the execution_block of the concrete instance of the class"""
        self.set_common_inset(solution_object)
        self.set_execution_block(solution_object)

        script = SolutionScript(solution_object, self.execution_block, argv)

        return script.create_solution_script()


class ScriptCreatorInstall(ScriptCreator):
    def __init__(self):
        super().__init__()

    def set_execution_block(self, _):
        self.execution_block = "\nget_active_solution().install()\n"

    def set_common_inset(self, _):
        self.common_inset = ""


class ScriptCreatorUnInstall(ScriptCreator):
    def __init__(self):
        super().__init__()

    def set_execution_block(self, _):
        self.execution_block = "\nget_active_solution().uninstall()\n"

    def set_common_inset(self, _):
        self.common_inset = ""


class ScriptCreatorRun(ScriptCreator):
    def __init__(self, pop_solution: bool = False, execution_callback=None):
        super().__init__(execution_callback)
        self.pop_solution = pop_solution

    def set_common_inset(self, _):
        self.common_inset = ""

    def set_execution_block(self, solution_object: AlbumRunner):
        execution_block = self.common_inset
        execution_block += "\nmodule_logger().info(\"Starting %s\")" % solution_object["name"]
        execution_block += "\nmodule_logger().info(\"\")\n"
        if solution_object['run'] and callable(solution_object['run']):
            execution_block += "\nget_active_solution().run()\n"
        else:
            raise ValueError("No \"run\" routine specified for solution \"%s\"! Aborting..." % solution_object["name"])

        execution_block += self.execution_callback()

        if solution_object['close'] and callable(solution_object['close']):
            execution_block += "\nget_active_solution().close()\n"

        execution_block += "\nmodule_logger().info(\"\")"
        execution_block += "\nmodule_logger().info(\"Finished %s\")\n" % solution_object["name"]

        if self.pop_solution:
            execution_block += "\npop_active_solution()\n"

        self.execution_block = execution_block


class ScriptTestCreator(ScriptCreatorRun):
    def __init__(self):
        super().__init__()

    def set_common_inset(self, solution_object):
        common_inset = "\nd = get_active_solution().pre_test()\n"
        common_inset += "\nsys.argv = sys.argv + [\"=\".join([c, d[c]]) for c in d]\n"

        # parse args again after pre_test() routine if necessary.
        if not solution_object["args"] == "pass-through":
            common_inset += "\nget_active_solution().args = parser.parse_args()\n"

        self.common_inset = common_inset

    def set_execution_block(self, solution_object):
        super().set_execution_block(solution_object)
        self.execution_block += "\nget_active_solution().test()\n"