
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
        self.current_action = None

        if env:
            assert isinstance(env, (tuple, list))
            for name, value in env:
                self.add_env(name, value)

    def add_env(self, name, value):
        v = value
        if isinstance(v, str):
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

    def add_action(self, action):
        assert action is not None

        action.context = self
        if self.current_action:
            self.current_action.add_action(action)
        else:
            self.action_list.append(action)
        return self

    def action(self, name, action, env={}, before=None, after=None):

        ac = actions.Action(name, action)

        ac.init(self, env, before, after)

        self.add_action(ac)

        return self

    def start_composite(self, condition=None, env={}):
        ac = actions.CompositeAction(condition)
        ac.init(self, env)

        self.current_action = ac
        return self

    def stop_composite(self):
        if self.current_action is None:
            return self

        self.action_list.append(self.current_action)
        self.current_action = None
        return self

    def func_action(self, func, *args, **kwargs):
        ac = actions.FuncAction(func, *args, **kwargs)
        ac.init(self, {})

        self.add_action(ac)
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
        if self.current_action is not None:
            self.action_list.append(self.current_action)
            self.current_action = None

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

        self.add_action(ac)
        return self

    def prepare_dir(self, dir_list, env={}, before=None, after=None):
        ac = actions.PrepareDirAction(dir_list)
        ac.init(self, env, before, after)

        self.add_action(ac)
        return self

    def ask(self, ask_list, env={}):
        ac = actions.AskAction(ask_list)
        ac.init(self, env)

        self.add_action(ac)
        return self

    def copy(self, copy_list, work_dir=None, env={}):
        ac = actions.CopyAction(copy_list, work_dir)
        ac.init(self, env)

        self.add_action(ac)
        return self

    def exec_cmd(self, cmd, work_dir=None, env_name=None, handle_func=None, encoding='utf-8', env={}, **kwargs):
        ac = actions.ExecCmdAction(
                cmd, work_dir,
                env_name, handle_func, **kwargs
        )
        ac.init(self, env)

        self.add_action(ac)
        return self

    def zip(self, src_dir, zip_path, zip_path_prefix=None, fmt='%Y-%m-%d', env_name=None):
        ac = actions.ZipAction(
            src_dir, zip_path,
            zip_path_prefix, fmt, env_name
        )

        ac.init(self)

        self.add_action(ac)
        return self

    def unzip(self, zip_path, out_put_dir, create_sub_dir=True, env_name=None):
        ac = actions.UnZipAction(
            zip_path, out_put_dir,
            create_sub_dir, env_name
        )

        ac.init(self)

        self.add_action(ac)
        return self

    def targz(self, src_dir, compress_path, fmt='%Y-%m-%d', env_name=None):
        ac = actions.TargzAction(
            src_dir, compress_path,
            fmt, env_name
        )
        ac.init(self)

        self.add_action(ac)
        return self

    def untargz(self, compress_path, out_put_dir, create_sub_dir=False, env_name=None):
        ac = actions.UnTargzAction(
            compress_path, out_put_dir,
            create_sub_dir, env_name
        )

        ac.init(self)

        self.add_action(ac)
        return self
