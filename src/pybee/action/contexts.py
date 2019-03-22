
import traceback
import sys
from string import Template

import pybee
from pybee.action import actions


class BaseActionContext(object):
    def __init__(self, env=None):
        self.env = {
            'CURRENT_DIR': pybee.path.get_work_path()
        }
        self.action_list = []

        if env:
            assert isinstance(env, (tuple, list))
            for name, value in env:
                self.add_env(name, value)

    def add_env(self, name, value):
        v = self.render_str(value)
        self.env[name] = v

        return self

    def get_env(self, name):
        return self.env.get(name, None)

    def render_str(self, s):
        if '$' not in s:
            return s

        t = Template(s)
        return t.substitute(self.env)

    def action(self, name, action, env={}, before=None, after=None):

        ac = actions.Action(self, name, action)

        ac.init(self, env, before, after)

        self.action_list.append(ac)

        return self

    def action(self, action):
        assert action is not None
        assert action.actioin is not None

        action.context = self.context
        self.action_list.append(action)
        return self

    def last_action(self):
        if not self.action_list:
            return None

        return self.action_list[-1]

    def first_action(self):
        if not self.action_list:
            return None

        return self.action_list[0]

    def execute(self, succ_func=None):
        all_succ = True
        for action in self.action_list:
            print('start execte action %s' % action.name)
            succ = False
            try:
                succ = action.execute()
            except Exception:
                traceback.print_exc()

            if succ is not True:
                all_succ = False
                break
            print('finish execte action %s' % action.name)

        if all_succ and succ_func and callable(succ_func):
            succ_func(self)

        return all_succ


class ActionContext(BaseActionContext):
    def __init__(self, env=None):
        super().__init__(env)

    def check_bin(self, bin_list, env={}, before=None, after=None):
        ac = actions.CheckBinAction(bin_list)
        ac.init(self, env, before, after)

        self.action_list.append(ac)
        return self

    def prepare_dir(self, dir_list, env={}, before=None, after=None):
        ac = actions.PrepareDirAction(dir_list)
        ac.init(self, env, before, after)

        self.action_list.append(ac)
        return self

    def ask(self, ask_list, env={}):
        ac = actions.AskAction(ask_list)
        ac.init(self, env)

        self.action_list.append(ac)
        return self

    def copy(self, copy_list, work_dir=None, env={}):
        ac = actions.CopyAction(copy_list, work_dir)
        ac.init(self, env)

        self.action_list.append(ac)
        return self

    def exec_cmd(self, cmd, work_dir=None, encoding=sys.stdout.encoding, env_name=None, env={}):
        ac = actions.ExecCmdAction(
                cmd, work_dir, encoding,
                env_name
        )
        ac.init(self, env)

        self.action_list.append(ac)
        return self

    def zip(self, src_dir, zip_path, zip_path_prefix=None, fmt='%Y-%m-%d', env_name=None):
        ac = actions.ZipAction(
            src_dir, zip_path,
            zip_path_prefix, fmt, env_name
        )

        ac.init(self)

        self.action_list.append(ac)
        return self

    def unzip(self, zip_path, out_put_dir, create_sub_dir=True, env_name=None):
        ac = actions.UnZipAction(
            zip_path, out_put_dir,
            create_sub_dir, env_name
        )

        ac.init(self)

        self.action_list.append(ac)
        return self

    def targz(self, src_dir, compress_path, fmt='%Y-%m-%d', env_name=None):
        ac = actions.TargzAction(
            src_dir, compress_path,
            fmt, env_name
        )
        ac.init(self)

        self.action_list.append(ac)
        return self

    def untargz(self, compress_path, out_put_dir, create_sub_dir=False, env_name=None):
        ac = actions.UnTargzAction(
            compress_path, out_put_dir,
            create_sub_dir, env_name
        )

        ac.init(self)

        self.action_list.append(ac)
        return self
