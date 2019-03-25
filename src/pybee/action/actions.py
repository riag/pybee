
import os
import sys
import shutil
from datetime import datetime
from string import Template
import pybee
from pathlib import Path


class Action(object):
    def __init__(self, name, action_func):
        self.name = name
        self.action_func = action_func
        self.context = None
        assert callable(action_func)

        self.env = {}
        self.before_func = None
        self.after_func = None

    def init(self, context, env={}, before_func=None, after_func=None):
        self.before_func = before_func
        self.after_func = after_func
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

    def render_str(self, s):
        if '$' not in s:
            return s

        t = Template(s)
        return t.substitute(self.context.env, **self.env)

    def get_env(self, name):
        v = self.env.get(name, None)
        if v is None:
            v = self.context.env.get(name, None)

        return v

    def execute(self):
        rs = True
        if self.before_func:
            assert callable(self.before_func)
            rs = self.before_func(self)

        if rs is not True:
            return rs

        rs = self.action_func(self)

        if self.after_func:
            assert callable(self.after_func)
            self.after_func(self, rs)

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


class FuncAction(Action):
    '''
        执行普通的 python 的函数
    '''
    def __init__(self, func, *args, **kwargs):
        super().__init__('func', self.do_action)

        self.func = func
        self.args = args
        self.kwargs = kwargs

    def do_action(self, *args):
        self.func(*self.args, **self.kwargs)
        return True


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
            s = self.render_str(d)
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
            self.work_dir = self.render_str(self.work_dir)

        new_copy_list = []
        for item in self.copy_list:
            src = item[0]
            dest = item[1]
            m = {}
            if len(item) > 2:
                m = item[2]

            src = self.render_str(src)
            dest = self.render_str(dest)
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
            create_sub_dir = kwargs.pop('create_sub_dir', True)
            if create_sub_dir:
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
            self.work_dir = self.render_str(self.work_dir)

        shell = False
        if isinstance(self.cmd, str):
            shell = True
            self.cmd = self.render_str(self.cmd)
        else:
            c = self.cmd[0]
            c = self.render_str(c)
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


class CompressAction(Action):
    def __init__(self, name, src_dir, dest_path, fmt='%Y-%m-%d', env_name=None):
        super().__init__(name, self.do_action)

        self.dest_path = dest_path
        self.src_dir = src_dir
        self.fmt = fmt

        self.env_name = env_name

    def do_action(self, *args):
        v = self.render_str(self.dest_path)

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

        self.src_dir = self.render_str(self.src_dir)

        name = os.path.basename(self.src_dir)
        work_dir = os.path.dirname(self.src_dir)

        self.compress(work_dir, name)

        if self.env_name:
            self.context.env[self.env_name] = self.dest_path

        return True

    def compress(self, work_dir, src_dir_name):
        pass


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


class DeCompressAction(Action):
    def __init__(self, name, src_path, out_put_dir, create_sub_dir=True, env_name=None):
        super().__init__(name, self.do_action)

        self.src_path = src_path
        self.out_put_dir = out_put_dir
        self.env_name = env_name
        self.create_sub_dir = create_sub_dir

    def get_file_name(self, p):
        name = os.path.basename(p)
        suffix = ''.join(Path(p).suffixes)
        if suffix:
            return name.rstrip(suffix)
        return name

    def do_action(self, *args):
        self.src_path = self.render_str(self.src_path)
        self.out_put_dir = self.render_str(self.out_put_dir)

        dest_path = self.out_put_dir
        if self.create_sub_dir:
            name = self.get_file_name(self.src_path)
            dest_path = os.path.join(dest_path, name)
            pybee.path.mkdir(dest_path, True)

        self.decompress(self.src_path, dest_path)

        if self.env_name:
            self.context.env[self.env_name] = dest_path

        return True

    def decompress(self, src_path, dest_path):
        pass


class ZipAction(CompressAction):
    def __init__(self, src_dir, dest_path, zip_path_prefix=None, fmt='%Y-%m-%d', env_name=None):
        super().__init__('zip', src_dir, dest_path, fmt, env_name)

        self.zip_path_prefix = zip_path_prefix


    def compress(self, work_dir, src_dir_name):

        with pybee.path.working_dir(work_dir):
            pybee.compress.zip(
                self.dest_path, src_dir_name, self.zip_path_prefix
            )

        return True


class UnZipAction(DeCompressAction):
    def __init__(self, zip_path, out_put_dir, create_sub_dir=True, env_name=None):
        super().__init__('unzip', zip_path, out_put_dir, create_sub_dir, env_name)

    def decompress(self, src_path, dest_path):
        pybee.compress.unzip(src_path, dest_path)


class TargzAction(CompressAction):
    def __init__(self, src_dir, dest_path, fmt='%Y-%m-%d', env_name=None):
        super().__init__('targz', src_dir, dest_path, fmt, env_name)

    def compress(self, work_dir, src_dir_name):
        with pybee.path.working_dir(work_dir):
            pybee.shell.exec([
                'tar', 'cfz', self.dest_path, src_dir_name,
            ])

        return True


class UnTargzAction(DeCompressAction):
    def __init__(self, zip_path, out_put_dir, create_sub_dir=True, env_name=None):
        super().__init__('untargz', zip_path, out_put_dir, create_sub_dir, env_name)

    def decompress(self, src_path, dest_path):
        pybee.shell.exec([
            'tar', 'xfz', src_path, '-C', dest_path
        ])


class DownloadAction(Action):
    def __init__(self, url, out_put_path, env_name=None, **kwargs):
        super().__init__('download', self.do_action)

        self.url = url
        self.out_put_path = out_put_path
        self.env_name = env_name
        self.kwargs = kwargs

    def do_action(self, *args):
        out = self.render_str(self.out_put_path)
        dest_file = pybee.download.download(
            self.url, out,
            **self.kwargs
        )
        if self.env_name:
            self.context.env[self.env_name] = dest_file

        return True
