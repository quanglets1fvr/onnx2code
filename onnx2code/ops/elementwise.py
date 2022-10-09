import numpy as np

from .operation import OpCall, OpImpl, Operation
from ..util import get_attribute


class Elementwise(Operation):
    """
    Elementwise operators

    For example: ReLU, Tanh, Sigmoid, etc.
    """

    node_types = {"Relu", "Tanh", "Sigmoid", "Clip"}

    def parse(self) -> None:
        assert len(self.inputs) == 1, "expected one input"
        assert len(self.outputs) == 1, "expected one output"
        assert (
            self.inputs[0].size == self.outputs[0].size
        ), "input and output tensors should have the same size"

        self.op: str = self.node.op_type
        self.size = self.inputs[0].size

    def call(self) -> OpCall:
        return OpCall(
            name=f"{self.op}_{self.size}",
            params=["A", "B"],
            inputs=self.inputs,
            outputs=self.outputs,
        )


@Elementwise.variant("c")
class ElementwiseC(Elementwise):
    def impl(self) -> OpImpl:
        op, size = self.op, self.size

        if op == "Relu":
            impl = "A[i] > 0 ? A[i] : 0"
        elif op == "Tanh":
            impl = "tanh(A[i])"
        elif op == "Sigmoid":
            impl = "1.0f / (1.0f + exp(-A[i]))"
        elif op == "Clip":  # TODO: test!
            finfo = np.finfo(dtype=np.float32)
            min = get_attribute(self.node, "min", finfo.min)
            max = get_attribute(self.node, "max", finfo.max)
            impl = "A[i] < {} ? {} : A[i] > {} ? {} : A[i]".format(min, min, max, max)
        else:
            raise RuntimeError(f"Unsupported elementwise: {op}")

        source = f"""
        for(int i = 0; i < {size}; i++) {{
            B[i] = {impl};
        }}
        """

        return OpImpl(lang="c", source=source)