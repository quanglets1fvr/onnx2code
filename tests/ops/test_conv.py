import pytest
import tensorflow as tf

from ..util import check_keras

# @pytest.mark.parametrize("shape", [(4, 3, 1), (3, 4, 3), (10, 10, 5), (32, 32, 3)])
# @pytest.mark.parametrize("kernel_size", [1, 2, 3])
# @pytest.mark.parametrize("filters", [1, 2, 3, 10])
# @pytest.mark.parametrize("padding", ["valid", "same"])
# @pytest.mark.parametrize(
#     "stride_and_dilation",
#     [
#         (1, 1),
#         (2, 1),
#         (1, 2),
#     ],
#     ids=lambda x: f"s{x[0]}d{x[1]}",
# )
# @pytest.mark.parametrize("use_bias", [False, True], ids=["no_bias", "bias"])


@pytest.mark.parametrize("shape", [(28, 28, 1), (14, 14, 8)])
@pytest.mark.parametrize("kernel_size", [5])
@pytest.mark.parametrize("filters", [8, 16])
@pytest.mark.parametrize("padding", ["same"])
@pytest.mark.parametrize(
    "stride_and_dilation",
    [
        (1, 1),
    ],
    ids=lambda x: f"s{x[0]}d{x[1]}",
)
@pytest.mark.parametrize("use_bias", [False], ids=["no_bias"])
def test_conv(
    shape: list[int],
    kernel_size: int,
    filters: int,
    padding: str,
    stride_and_dilation: tuple[int, int],
    use_bias: bool,
) -> None:
    try:
        input = tf.keras.Input(shape=shape)
        output = tf.keras.layers.Conv2D(
            filters=filters,
            padding=padding,
            kernel_size=kernel_size,
            strides=stride_and_dilation[0],
            dilation_rate=stride_and_dilation[1],
            use_bias=use_bias,
            bias_initializer="random_normal",
        )(input)
        model = tf.keras.Model(inputs=[input], outputs=[output])
    except Exception:
        pytest.skip("incompatible configuration")

    check_keras(model)
