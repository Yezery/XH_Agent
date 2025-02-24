from app.desktop.studio_server.datamodel.vo.run_output import RunOutput


class BaseParser:

    def parse_output(self, original_output: RunOutput) -> RunOutput:
        """
        Method for parsing the output of a model. Typically overridden by subclasses.
        """
        return original_output
