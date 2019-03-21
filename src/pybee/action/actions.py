
import os
import sys
import shutil
from datetime import datetime
from string import Template
import pybee
from pathlib import Path


class Action(object):
    def __init__(self, name, action):
        self.name = name
        self.action = action
        self.context = None
        assert callable(action)

        self.env = {}
        self.before = None
        self.after = None

    def init(self, context, env={}, before=None, after=None):
        self.before = before
        self.after = after
        self.context = context
        self.add_env(env)

        return self

    def add_env(self, name, value):
        t = Template(value)
        v = t.substitute(self.context.env, **self.env)
        self.env[name] = v

        return self


    def add_env(self, env):
        for name, value in env:
            self.add_env(name, value)

        return self

    def action(self, name, action, env={}, before=None, after=None):
        return self.cotext.action(
            name, action, env,
            before, after
        )

    def get_env(self, name):
        v = self.env.get(name, None)
        if v is None:
            v = self.context.env.get(name, None)

        return v

    def execute(self):
        rs = True
        if self.before:
            assert callable(self.before)
            rs = self.before(self)

        if rs is not True:
            return rs

        rs = self.action(self)

        if self.after:
            assert callable(self.after)
            self.after(self, rs)

        return rs


class ConditionAction(Action):
    def __init__(self, name, condition, action):
        super().__init__(name, action)
        assert callable(condition)

        self.condition = condition

    def execute(self):
        if not self.condition(self):
            print('ignore action %s' % self.name)
            return True

        return super().execute(self)


class CheckBinAction(Action):
    def __init__(self, bin_list):
        super().__init__('check_bin', self.do_action)

        self.bin_list = bin_list

    def do_action(self, *args):
        succ = True
        env_name = None
        for item in self.bin_list:
            if isinstance(item, (tuple, list)):
                bin = item[0]
                msg = item[1]
                if len(item) > 2:
                    env_name = item[2]
            else:
                bin = item
                msg = '%s is not exist' % bin

            t = shutil.which(bin)
            if t:
                if env_name:
                    self.context.env[env_name] = t
            else:
                succ = False
                print(msg)

        return succ


class PrepareDirAction(Action):
    def __init__(self, dir_list):
        super().__init__('prepare_dir', self.do_action)

        self.dir_list = dir_list

    def do_action(self, *args):
        l = []
        for d in self.dir_list:
            t = Template(d)
            s = t.substitute(self.context.env, **self.env)
            l.append(s)

        for d in l:
            if os.path.isdir(d):
                pybee.path.rmtree(d)
            else:
                pybee.path.mkdir(d, True)

        return True


class AskAction(Action):
    def __init__(self, ask_list):
        super().__init__('ask', self.do_action)
        self.ask_list = ask_list

    def do_action(self, *args):
        for item in self.ask_list:
            env_name = item[0]
            ask_type = item[1]
            env_value = self.get_env(env_name)
            msg = item[2]
            if env_value is not None:
                msg = msg.format(env_value)

            m = {}
            if len(item) > 3:
                m = item[3]

            ask_func = pybee.action.ask.get_ask_func(ask_type)
            if ask_func is None:
                print('not support ask type %s' % ask_type)
                return False

            value = ask_func(msg, env_value, **m)
            if env_value != value:
                self.context.env[env_name] = value

        return True


class CopyAction(Action):
    def __init__(self, copy_list, work_dir=None):
        super().__init__('copy', self.do_action)
        self.copy_list = copy_list
        self.work_dir = work_dir

    def do_action(self, *args):
        if self.work_dir:
            t = Template(self.work_dir)
            self.work_dir = t.substitute(self.context.env, **self.env)

        new_copy_list = []
        for item in self.copy_list:
            src = item[0]
            dest = item[1]
            m = {}
            if len(item) > 2:
                m = item[2]

            t = Template(src)
            src = t.substitute(self.context.env, **self.env)

            t = Template(dest)
            dest = t.substitute(self.context.env, **self.env)
            new_copy_list.append((src, dest, m))


        prev_cwd = os.getcwd()
        if self.work_dir:
            os.chdir(self.work_dir)

        try:
            for src, dest, m in new_copy_list:
                self.copy(src, dest, **m)
        finally:
            if self.work_dir:
                os.chdir(prev_cwd)

        return True


    def copy(self, src, dest, **kwargs):
        if os.path.isdir(src):
            name = os.path.basename(src)
            dest = os.path.join(dest, name)
            pybee.path.copytree(src, dest, **kwargs)
        else:
            pybee.path.copyfiles(
                [src, ], dest
            )


class ExecCmdAction(Action):
    def __init__(self, cmd, work_dir=None, encoding=sys.stdout.encoding, env_name=None):

        super().__init__('exec_cmd', self.do_action)
        self.cmd = cmd
        self.work_dir = work_dir
        self.env_name = env_name

    def do_action(self, *args):
        if self.work_dir:
            t = Template(self.work_dir)
            self.work_dir = t.substitute(self.context.env, **self.env)

        shell = False
        if isinstance(self.cmd, str):
            shell = True
            t = Template(self.cmd)
            self.cmd = t.substitute(self.context.env, **self.env)
        else:
            c = self.cmd[0]
            t = Template(c)
            c = t.substitute(self.context.env, **self.env)
            self.cmd[0] = c

        env = self.env if self.env else None

        if self.env_name:
            value = pybee.shell.get_output(
                self.cmd, shell=shell,
                cwd=self.work_dir,
                env=env
            )
            self.context.env[self.env_name] = value
        else:
            pybee.shell.exec(
                self.cmd, shell=shell,
                cwd=self.work_dir,
                env=env
                )

        return True


class ZipAction(Action):
    def __init__(self, dest_path, src_dir, zip_path_prefix=None, fmt='%Y-%m-%d', env_name=None):
        super().__init__('zip', self.do_action)

        self.dest_path = dest_path
        self.src_dir = src_dir
        self.zip_path_prefix = zip_path_prefix
        self.fmt = fmt

        self.env_name = env_name

    def get_git_branch(self):
        current_dir = self.get_env('CURRENT_DIR')
        if not pybee.git.is_git_repo(current_dir):
            return ''

        git_bin = shutil.which('git')
        if not git_bin:
            return ''

        branch = pybee.git.get_current_branch(current_dir)
        branch = (branch == 'master') and 'release' or branch
        return branch



    def do_action(self, *args):
        t = Template(self.dest_path)
        v = t.substitute(self.context.env, **self.env)

        now = datetime.now()
        d = pybee.datetime.to_str(now, self.fmt)
        v_map = {
            'datetime': d,
        }
        branch = self.get_git_branch()
        if branch:
            v_map['branch'] = branch
        self.dest_path = v.format(
            **v_map
        )

        t = Template(self.src_dir)
        self.src_dir = t.substitute(self.context.env, **self.env)

        name = os.path.basename(self.dest_path)
        work_dir = os.path.dirname(self.src_dir)
        with pybee.path.working_dir(work_dir):
            pybee.compress.zip(
                name, self.src_dir, self.zip_path_prefix
            )

        if self.env_name:
            self.context.env[self.env_name] = self.dest_path

        return True


class UnZipAction(Action):
    def __init__(self, zip_path, out_put_dir, create_sub_dir=True):
        super().__init__('unzip', self.do_action)

        self.zip_path = zip_path
        self.out_put_dir = out_put_dir
        self.create_sub_dir = create_sub_dir

    def do_action(self, *args):
        t = Template(self.zip_path)
        self.zip_path = t.substitute(self.context.env, **self.env)

        t = Template(self.out_put_dir)
        self.out_put_dir = t.substitute(self.context.env, **self.env)

        dest_path = self.out_put_dir
        if self.create_sub_dir:
            name = Path(self.zip_path).stem
            dest_path = os.path.join(dest_path, name)

        pybee.compress.unzip(self.zip_path, dest_path)
        return True
