from palantir.program import Program


class TestProgram:

    def test_basic(self, program):
        program = program.programs[0]
        assert isinstance(program, Program)
