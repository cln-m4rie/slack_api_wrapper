import datetime
from functools import partial


class Functions:

    class PrintFunc:
        RED = '31'
        GREEN = '32'
        YELLOW = '33'
        BLUE = '34'
        MAGENTA = '35'
        CYAN = '36'
        WHITE = '37'

        @staticmethod
        def print_colored(code, key, text, is_bold=False):
            if is_bold:
                code = '1;%s' % code

            print(
                f'[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] \033[{code}m{key}\033[0m: {text}')

        @staticmethod
        def info(text, is_bold=False):
            p = partial(
                Functions.PrintFunc.print_colored,
                Functions.PrintFunc.BLUE,
                'INFO'
            )
            p(text, is_bold)

        @staticmethod
        def success(text, is_bold=False):
            p = partial(
                Functions.PrintFunc.print_colored,
                Functions.PrintFunc.GREEN,
                'SUCCESS'
            )
            p(text, is_bold)

        @staticmethod
        def warning(text, is_bold=False):
            p = partial(
                Functions.PrintFunc.print_colored,
                Functions.PrintFunc.YELLOW,
                'WARNING'
            )
            p(text, is_bold)

        @staticmethod
        def danger(text, is_bold=False):
            p = partial(
                Functions.PrintFunc.print_colored,
                Functions.PrintFunc.RED,
                'ERROR'
            )
            p(text, is_bold)

        @staticmethod
        def print_magenda(key, text, is_bold=False):
            p = partial(
                Functions.PrintFunc.print_colored,
                Functions.PrintFunc.MAGENTA)
            p(key, text, is_bold)

        @staticmethod
        def print_cyan(key, text, is_bold=False):
            p = partial(
                Functions.PrintFunc.print_colored,
                Functions.PrintFunc.CYAN)
            p(key, text, is_bold)

        @staticmethod
        def white(key, text, is_bold=False):
            p = partial(
                Functions.PrintFunc.print_colored,
                Functions.PrintFunc.WHITE)
            p(key, text, is_bold)
