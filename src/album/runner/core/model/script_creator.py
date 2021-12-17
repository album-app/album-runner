import abc

from album.runner.album_logging import get_active_logger
from album.runner.core.api.model.script_creator import IScriptCreator
from album.runner.core.api.model.solution import ISolution
from album.runner.core.model.solution_script import SolutionScript


class ScriptCreator(IScriptCreator):

    def __init__(self, append_arguments=True):
        self.append_arguments = append_arguments

    @abc.abstractmethod
    def get_execution_block(self, solution_object: ISolution) -> str:
        """The custom code for all scripts created by this class"""
        pass

    def create_script(self, solution_object: ISolution, argv) -> str:
        execution_block = self.get_execution_block(solution_object)

        script = SolutionScript(solution_object, execution_block, argv, self.append_arguments)

        return script.create_solution_script()


class ScriptCreatorInstall(ScriptCreator):
    def __init__(self):
        super().__init__(append_arguments=False)

    def get_execution_block(self, _):
        return "\nget_active_solution().setup().install()\n"


class ScriptCreatorUnInstall(ScriptCreator):
    def __init__(self):
        super().__init__(append_arguments=False)

    def get_execution_block(self, _):
        return "\nget_active_solution().setup().uninstall()\n"


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

    def get_execution_block(self, solution_object: ISolution):
        execution_block = "\nget_active_logger().info(\"Starting %s\")\n" % solution_object.setup().name
        if solution_object.setup().run and callable(solution_object.setup().run):
            execution_block += "\nget_active_solution().setup().run()\n"
        else:
            get_active_logger().warn("No \"run\" routine configured for solution \"%s\"." % solution_object.setup().name)

        # used to insert code blocks during runtime after run but before close. Used when solution serves as parent.
        execution_block += self.execution_callback()

        if solution_object.setup().close and callable(solution_object.setup().close):
            execution_block += "\nget_active_solution().setup().close()\n"

        execution_block += "\nget_active_logger().info(\"Finished %s\")\n" % solution_object.setup().name

        if self.pop_solution:
            execution_block += "\npop_active_solution()\n"

        return execution_block


class ScriptCreatorRunWithParent(ScriptCreatorRun):
    def __init__(self, parent_script_creator: ScriptCreatorRun, child_solution_list: list, child_args: list):
        super().__init__()
        self.parent_script_creator = parent_script_creator
        self.child_solution_list = child_solution_list
        self.child_args = child_args

    def get_execution_block(self, solution_object: ISolution) -> str:
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


class ScriptCreatorTest(ScriptCreatorRun):
    def __init__(self):
        super().__init__()

    def get_execution_block(self, solution_object: ISolution):
        execution_block = "\nd = get_active_solution().setup().pre_test()\n"
        execution_block += "\nsys.argv = sys.argv + [\"=\".join([c, d[c]]) for c in d]\n"

        # parse args again after pre_test() routine if necessary.
        if not solution_object.setup()["args"] == "pass-through":
            execution_block += "\nget_active_solution().set_args(parser.parse_args())\n"

        execution_block += super().get_execution_block(solution_object)
        execution_block += "\nget_active_solution().setup().test()\n"

        return execution_block
