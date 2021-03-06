import edge
import random
import numpy as np

from matrix_size import MatrixSize


class Mul(edge.Edge):
    num_inputs = 2
    expression = "{} = {}*{}"
    op_name = "mul"
    _reassignable = False
    options = ['dot_d']

    def __init__(self, program_index, output, inputs):
        super(Mul, self).__init__(program_index, output, inputs)

    @staticmethod
    def output_size(operands):
        assert len(operands) == 2, 'Matrix multiplication takes two arguments'
        lhs_size = operands[0][0]
        rhs_size = operands[1][0]
        out_size = None
        if lhs_size == MatrixSize.large_large:
            if rhs_size == MatrixSize.large_large:
                out_size = MatrixSize.large_large
            elif rhs_size == MatrixSize.large_small:
                out_size = MatrixSize.large_small
        elif lhs_size == MatrixSize.large_small:
            if rhs_size == MatrixSize.small_large:
                out_size = MatrixSize.large_large
            elif rhs_size == MatrixSize.small_small:
                out_size = MatrixSize.large_small
        elif lhs_size == MatrixSize.small_large:
            if rhs_size == MatrixSize.large_large:
                out_size = MatrixSize.small_large
            elif rhs_size == MatrixSize.large_small:
                out_size = MatrixSize.small_small
        elif lhs_size == MatrixSize.small_small:
            if rhs_size == MatrixSize.small_large:
                out_size = MatrixSize.small_large
            elif rhs_size == MatrixSize.small_small:
                out_size = MatrixSize.small_small
        if out_size is None:
            raise ValueError('Matrix size mismatch {0}, {1}'.format(lhs_size, rhs_size))
        else:
            # Copy tiling from LHS
            return out_size, operands[0][1]

    @staticmethod
    def valid_input_sizes():
        return [(MatrixSize.large_large, MatrixSize.large_large),
                (MatrixSize.small_small, MatrixSize.small_small),
                (MatrixSize.large_small, MatrixSize.small_large),
                (MatrixSize.small_large, MatrixSize.large_small)]

    @staticmethod
    def mul_dot_d_cost():
        return np.array([[[6, 1], [20, 12]],
                         [[10, 3], [25, 12]]])

    @staticmethod
    def get_cost_dict():
        return {'dot_d': Mul.mul_dot_d_cost}

    @staticmethod
    def num_implementations():
        return 1

    @staticmethod
    def random_imp():
        return random.choice(["dot_d"])

    def expression_weight(self):
        return 1.0

    def get_acceptable_tilings(self):
        r = "row"
        c = "col"

        # Dot_d
        acceptable = [[r, r, r],
                      [r, r, c],
                      [c, r, c],
                      [c, c, c]]
        return acceptable
