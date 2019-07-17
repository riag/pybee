
import pybee
import os
import pytest


@pytest.fixture
def action_dir():
    p = './tmp/action'
    pybee.path.mkdir(p)
    return p

def test_action(capsys):
    ac = pybee.action.ActionContext(env=[
        ('DIST_DIR', '$CURRENT_DIR/temp/dist'),
        ('SCRIPT_DIR', '$CURRENT_DIR'),
    ])
    ac.check_bin(bin_list=[
        ('git', 'please install git'),
        ('gitx', 'please install gitx'),
    ])

    with capsys.disabled():
        print(ac.env)
        ac.execute()


def test_composite_action(action_dir, capsys):
    ac = pybee.action.ActionContext()
    ac.start_composite()
    ac.check_bin(bin_list=[
        ('git', 'please install git')
    ])
    ac.prepare_dir(dir_list=[
        action_dir
    ])
    ac.stop_composite()

    assert len(ac.action_list) == 1
    assert len(ac.last_action().action_list) == 2


class PipRunInfo(object):
    def __init__(self, run_func):
        self.in_data_list = []
        self.run_func = run_func
        self.last_result = None
        self.result_list = []

    def add_input_data(self, data):
        if data is None:
            return

        if isinstance(data, (tuple, list)):
            self.in_data_list.extend(data)
        else:
            self.in_data_list.append(data)

    def run(self):
        if len(self.in_data_list) == 0:
            return False, None

        data = self.in_data_list.pop(0)
        self.last_result = self.run_func(data)
        self.result_list.append(self.last_result)
        return True, self.last_result


class PipeRun(object):
    def __init__(self, data_list, run_func_list):
        self.data_list = data_list
        self.pip_run_list = []
        for func in run_func_list:
            self.pip_run_list.append(
                PipRunInfo(func)
            )

    def run(self):
        self.pip_run_list[0].add_input_data(self.data_list)
        while True:
            pre_result = None
            all_empty = True
            for run_info in self.pip_run_list:
                run_info.add_input_data(pre_result)
                pre_result = None

                has_run, pre_result = run_info.run()
                if has_run:
                    all_empty = False

            if all_empty:
                return self.pip_run_list[-1].result_list

        return None


def split_data(data):
    return 10, data


def add_one(data):
    return data + 1


def add_two(data):
    return data + 2


def test_pipe_run(capsys):
    p = PipeRun([1,2,3], [split_data, add_one, add_two])
    result_list = p.run()
    with capsys.disabled():
        print(result_list)

def test_insert_text_action(action_dir, capsys):
    ac = pybee.action.ActionContext(env=[
        ('OUTPUT_DIR', action_dir),
    ])
    out_file = '$OUTPUT_DIR/test_insert_text_action'
    f = ac.render_str(out_file)

    pybee.path.save_text_file(f, 
    '''test one 
test two
test third
test four
test five
    '''
    )

    line_number = 3
    a = pybee.action.actions.InsertTextAction(
        out_file, 'test insert text', line_number)
    ac.add_action(a)

    with capsys.disabled():
        print(ac.env)
        ac.execute()

        lines = pybee.path.read_lines_from_file(f)
        text = lines[line_number+1]
        print(text)
        assert text == 'test insert text\n'


def test_delete_text_action(action_dir, capsys):
    ac = pybee.action.ActionContext(env=[
        ('OUTPUT_DIR', action_dir),
    ])
    out_file = '$OUTPUT_DIR/test_delete_text_action'
    f = ac.render_str(out_file)

    pybee.path.save_text_file(f, 
    '''test one 
test two
test third
test four
test five
    '''
    )

    line_number = 3
    a = pybee.action.actions.InsertTextAction(
        out_file, 'test insert text', line_number)
    ac.add_action(a)

    with capsys.disabled():
        print(ac.env)
        ac.execute()

        lines = pybee.path.read_lines_from_file(f)
        text = lines[line_number+1]
        print(text)
        assert text == 'test insert text\n'


    ac.action_list.clear()
    a = pybee.action.actions.DeleteTextAction(out_file, line_number+1)
    ac.add_action(a)

    with capsys.disabled():
        print(ac.env)
        ac.execute()

        lines = pybee.path.read_lines_from_file(f)
        assert len(lines) == 6

    ac.action_list.clear()
    a = pybee.action.actions.DeleteTextAction(out_file, pattern='^test(\s+)four')
    ac.add_action(a)

    with capsys.disabled():
        print(ac.env)
        ac.execute()

        lines = pybee.path.read_lines_from_file(f)
        assert len(lines) == 5


def test_replace_action(action_dir, capsys):

    ac = pybee.action.ActionContext(env=[
        ('OUTPUT_DIR', action_dir),
    ])
    out_file = '$OUTPUT_DIR/test_replace_action'
    f = ac.render_str(out_file)

    pybee.path.save_text_file(f, 
    '''test one 
test two
test third
test four
test five
    '''
    )

    a = pybee.action.actions.ReplaceTextAction(
        out_file, 
        (
            ('^test(\s+)(four)', 'test\g<1>test'),
        ),
    )
    ac.add_action(a)

    with capsys.disabled():
        print(ac.env)
        ac.execute()

        lines = pybee.path.read_lines_from_file(f)

        assert lines[3] == 'test test\n'