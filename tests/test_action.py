
import pybee


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


def test_composite_action(capsys):
    ac = pybee.action.ActionContext()
    ac.start_composite()
    ac.check_bin(bin_list=[
        ('git', 'please install git')
    ])
    ac.prepare_dir(dir_list=[
        '$CURRENT_DIR/tmp'
    ])
    ac.stop_composite()

    assert len(ac.action_list) == 1
    assert len(ac.last_action().action_list) == 2
