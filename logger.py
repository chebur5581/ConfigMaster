from colorama import Fore
from colorama import init
from settings import logging, debug

init()


# Словарь для логов
warn_status = {'error': f'{Fore.RESET}[{Fore.RED}!{Fore.RESET}]{Fore.RED}',
               'warning': f'{Fore.RESET}[{Fore.YELLOW}Warn{Fore.RESET}]{Fore.YELLOW} ',
               'success': f'{Fore.RESET}[{Fore.GREEN}+{Fore.RESET}]{Fore.GREEN}',
               'info': f'{Fore.RESET}[{Fore.LIGHTBLUE_EX}i{Fore.RESET}]{Fore.LIGHTBLUE_EX}',
               'debug': f'{Fore.RESET}[{Fore.MAGENTA}debug{Fore.RESET}]{Fore.MAGENTA}'}


def log(text, status='debug'):  # логи в консоль
    if not debug and status == 'debug':
        return 0
    if logging:
        print(warn_status[status], str(text) + Fore.RESET)
