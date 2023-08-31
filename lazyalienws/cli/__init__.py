import argparse
from lazyalienws.constants.core_constants import NAME, PACKAGE_NAME, VERSION, VERSION_CLIENT, AUTHOR
from lazyalienws.cli.cmd_start import server_start
from lazyalienws.cli.cmd_client import create_client_file

def cmd():
    parsers = argparse.ArgumentParser(usage=f'python -m {PACKAGE_NAME} [args]',description = NAME,epilog = f'create by {",".join(AUTHOR)}')

    parsers.add_argument('-v', '--version', help=f'Show {NAME} version', action='store_true')

    subparsers = parsers.add_subparsers(title='Command', help='Available commands', dest='subparser_name')

    subparsers.add_parser('start', help=f'Start {NAME} server.')
    subparsers.add_parser('client', help=f'Generate a MCDR plugin of {NAME} client. Ensure you run this command under your MCDR plugins dictionary.')


    args = parsers.parse_args()
    
    if args.version:
        print(f"{NAME} v{VERSION} (Server&Package)\n{NAME} v{VERSION_CLIENT} (MCDR plugin)")
        return

    match args.subparser_name:

        case "start" | None:
            server_start()
        
        case "client":
            create_client_file()
        
        case _:
            print(">{}<".format(args.subparser_name))