import api_wrapper as api

import sys

def main(debug):
    api.debug = debug
    api.files.debug = debug
    
    name = input('Name: ')
    if name == 'exit':
        sys.exit()
    
    result = api.get_summoner_by_name(name)
    result = api.get_recent_games(result['id'])
    print([i for i in result['games'].pop()])
    
    return
    api.files.close()
    
if __name__ == '__main__':
    debug = True
    try:
        while True:
            main(debug)
    except (KeyboardInterrupt, SystemExit) as e:
        print('\nClosing up shop...')
        api.files.close()
        print('Bye bye!')
    except EOFError as e:
        print('\nClosing without saving... :(')
