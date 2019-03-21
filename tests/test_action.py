
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
