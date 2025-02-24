from .base_parser import BaseParser
from app.desktop.studio_server.datamodel.vo.run_output import RunOutput


class R1ThinkingParser(BaseParser):
    START_TAG = "<think>"
    END_TAG = "</think>"

    def parse_output(self, original_output: RunOutput) -> RunOutput:
        """
            将响应中的<think></inthink>标签解析为中间和最终输出。

            参数:
            original_output：包含原始响应字符串的RunOutput

            返回：
            ParsedOutput包含中间内容（思维内容）和最终结果

            报错：
            ValueError：如果响应格式无效（缺少标签、多个标签或关闭标签后没有内容）
        """
        # This parser only works for strings
        if not isinstance(original_output.output, str):
            raise ValueError("Response must be a string for R1 parser")

        # Strip whitespace and validate basic structure
        cleaned_response = original_output.output.strip()
        if not cleaned_response.startswith(self.START_TAG):
            raise ValueError("Response must start with <think> tag")

        # Find the thinking tags
        think_start = cleaned_response.find(self.START_TAG)
        think_end = cleaned_response.find(self.END_TAG)

        if think_start == -1 or think_end == -1:
            raise ValueError("Missing thinking tags")

        # Check for multiple tags
        if (
            cleaned_response.count(self.START_TAG) > 1
            or cleaned_response.count(self.END_TAG) > 1
        ):
            raise ValueError("Multiple thinking tags found")

        # Extract thinking content
        thinking_content = cleaned_response[
            think_start + len(self.START_TAG) : think_end
        ].strip()

        # Extract result (everything after </think>)
        result = cleaned_response[think_end + len(self.END_TAG) :].strip()

        if not result or len(result) == 0:
            raise ValueError("No content found after </think> tag")

        # Parse JSON if needed
        output = result

        # Add thinking content to intermediate outputs if it exists
        intermediate_outputs = original_output.intermediate_outputs or {}
        intermediate_outputs["reasoning"] = thinking_content

        return RunOutput(
            output=output,
            intermediate_outputs=intermediate_outputs,
        )
