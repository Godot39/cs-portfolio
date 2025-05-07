'''A text-based fantasy RPG built in Python with ASCII art, turn-based combat, and player progression.'''

import random, time, sys

# print text slowly when called
def slow_print(text, delay=0.01): 
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()
    
# ascii art dictionary for enemies and locations
ascii_art = {"death": r'''
__   __            ____  _          _ 
\ \ / /__  _   _  |  _ \(_) ___  __| |
 \ V / _ \| | | | | | | | |/ _ \/ _` |
  | | (_) | |_| | | |_| | |  __/ (_| |
  |_|\___/ \__,_| |____/|_|\___|\__,_|
  ''',
  "title": r'''
 ____  _                 _    ___     ____                 _   _     
| __ )| | ___   ___   __| |  ( _ )   | __ ) _ __ ___  __ _| |_| |__  
|  _ \| |/ _ \ / _ \ / _` |  / _ \/\ |  _ \| '__/ _ \/ _` | __| '_ \ 
| |_) | | (_) | (_) | (_| | | (_>  < | |_) | | |  __/ (_| | |_| | | |
|____/|_|\___/ \___/ \__,_|  \___/\/ |____/|_|  \___|\__,_|\__|_| |_|
    ''',
    "town": r'''
                   \  |  /         ___________
    ____________  \ \_# /         |  ___      |       _________
   |            |  \  #/          | |   |     |      | = = = = |
   | |   |   |  |   \\#           | |`v'|     |      |         |
   |            |    \#  //       |  --- ___  |      | |  || | |
   | |   |   |  |     #_//        |     |   | |      |         |
   |            |  \\ #_/_______  |     |   | |      | |  || | |
   | |   |   |  |   \\# /_____/ \ |      ---  |      |         |
   |            |    \# |+ ++|  | |  |^^^^^^| |      | |  || | |
   |            |    \# |+ ++|  | |  |^^^^^^| |      | |  || | |
^^^|    (^^^^^) |^^^^^#^| H  |_ |^|  | |||| | |^^^^^^|         |
   |    ( ||| ) |     # ^^^^^^    |  | |||| | |      | ||||||| |
   ^^^^^^^^^^^^^________/  /_____ |  | |||| | |      | ||||||| |
        `v'-                      ^^^^^^^^^^^^^      | ||||||| |
         || |`.      (__)    (__)                          ( )
                     (oo)    (oo)                       /---V
              /-------\/      \/ --------\             * |  |
             / |     ||        ||_______| \
            *  ||W---||        ||      ||  *
               ^^    ^^        ^^      ^^
    ''',
    "forest": r'''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠓⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠀⠀⠀⠀⠀⢠⢤⣤⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠔⠒⠒⠲⠎⠀⠀⢹⡃⢀⣀⠀⠑⠃⠀⠈⢀⠔⠒⢢⠀⠀⠀⡖⠉⠉⠉⠒⢤⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠔⠚⠙⠒⠒⠒⠤⡎⠀⠀⠀⠀⢀⣠⣴⣦⠀⠈⠘⣦⠑⠢⡀⠀⢰⠁⠀⠀⠀⠑⠰⠋⠁⠀⠀⠀⠀⠀⠈⢦⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠁⠀⠀⠀⠀⠀⠀⢰⠃⠀⣀⣀⡠⣞⣉⡀⡜⡟⣷⢟⠟⡀⣀⡸⠀⡎⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⣻⠀⠀⠀⠀
⢰⠂⠀⠀⠀⠀⠀⠀⠀⣗⠀⠀⢀⣀⣀⣀⣀⣀⣓⡞⢽⡚⣑⣛⡇⢸⣷⠓⢻⣟⡿⠻⣝⢢⠀⢇⣀⡀⠀⠀⠀⢈⠗⠒⢶⣶⣶⡾⠋⠉⠀⠀⠀⠀⠀
⠈⠉⠀⠀⠀⠀⠀⢀⠀⠈⠒⠊⠻⣷⣿⣚⡽⠃⠉⠀⠀⠙⠿⣌⠳⣼⡇⠀⣸⣟⡑⢄⠘⢸⢀⣾⠾⠥⣀⠤⠖⠁⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⢀⠀⠀
⠀⠀⠀⢰⢆⠀⢀⠏⡇⠀⡀⠀⠀⠀⣿⠉⠀⠀⠀⠀⠀⠀⠀⠈⢧⣸⡇⢐⡟⠀⠙⢎⢣⣿⣾⡷⠊⠉⠙⠢⠀⠀⠀⠀⠀⢸⡇⢀⠀⠀⠀⠀⠈⠣⡀
⠀⠀⠀⠘⡌⢣⣸⠀⣧⢺⢃⡤⢶⠆⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣟⠋⢀⠔⣒⣚⡋⠉⣡⠔⠋⠉⢰⡤⣇⠀⠀⠀⠀⢸⡇⡇⠀⠀⠀⠀⠀⠀⠸
⠀⠀⠀⠀⠑⢄⢹⡆⠁⠛⣁⠔⠁⠀⣿⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⣿⢠⡷⠋⠁⠀⠈⣿⡇⠀⠀⠀⠈⡇⠉⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠑⣦⡔⠋⠁⠀⠀⠀⣿⠀⠀⢠⡀⢰⣼⡇⠀⡀⠀⠀⣿⠀⠁⠀⠀⠀⠀⣿⣷⠀⠀⠀⠀⡇⠀⠀⢴⣤⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢰⣿⡇⠀⠀⠀⠀⠀⣿⡀⠀⢨⣧⡿⠋⠀⠘⠛⠀⠀⣿⠀⠀⢀⠀⠀⠀⣿⣿⠀⠀⠀⠀⢲⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀⠀⠀⠀⢸⡧⡄⠀⠹⣇⡆⠀⠀⠀⠀⠀⣿⠀⢰⣏⠀⣿⣸⣿⣿⠀⠀⠀⠀⣼⠀⠀⠰⠗⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⠀⠀⠀⠀⢸⡇⣷⣛⣦⣿⢀⠈⠑⠀⢠⡆⣿⠐⢠⣟⠁⢸⠸⣿⣿⢱⣤⢀⠀⣼⠀⠀⢀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⣿⡇⠀⢀⠀⠀⠀⢸⡇⠘⠫⣟⡇⠊⣣⠘⠛⣾⡆⢿⠀⠙⣿⢀⣘⡃⣿⣿⡏⠉⠒⠂⡿⠀⠰⣾⡄⠀⢸⡟⣽⣀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠸⣿⡇⠀⠘⣾⠀⠀⢸⡇⢸⣇⡙⠣⠀⣹⣇⠀⠈⠧⢀⣀⣀⡏⣸⣿⣇⢹⣿⡇⢴⣴⣄⣀⡀⢰⣿⡇⠀⢸⣇⢿⡿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠓⠁⠈⠻⢷⠾⠦⠤⠬⣅⣹⣿⣖⣶⣲⣈⡥⠤⠶⡖⠛⠒⠛⠁⠉⠛⠮⠐⢛⡓⠒⢛⠚⠒⠒⠒⠛⣚⣫⡼⠿⠿⣯⠛⠤⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⡉⠉⠁⠀⠀⠘⠓⠀⠀⠀⠀⠀⣀⣞⡿⡉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣶⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ''',
    "cave": r'''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣷⣄⠙⠛⠛⠿⠿⠿⠟⢁⡄⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⠘⠛⠿⢿⣿⠿⠻⣿⣿⣿⣿⣶⣶⣶⣦⣴⣿⣷⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⣶⣿⣿⣷⣶⣤⣤⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀
⠀⠀⠀⠀⠐⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢋⣀⠈⢿⣿⡟⢻⣿⣿⠀
⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⣠⣤⣼⣿⣿⠀
⠀⠀⠀⢀⣠⣤⠈⠿⠿⠟⢋⣠⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀
⠀⠀⠐⣿⣿⣿⣷⣶⣤⣶⣿⣿⣿⣿⣿⣿⠟⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀
⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠈⠙⠻⠿⠿⠿⣿⡿⣿⣿⣿⠀
⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⠛⠀⠀⠀⠀⠀⠀⢤⣶⣦⣀⣤⣿⣿⣿⠀
⠀⣠⣾⣿⡿⠿⠿⠿⠛⠋⠙⠋⠀⠸⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⠀
⠀⣿⣿⣿⣿⣶⣶⣶⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⢋⣡⠀
⠀⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠛⠛⠛⠛⠛⠛⠀
    ''',
    "merchant": r'''
                        ;;\\/;;;;;;;;
                   ;;;;;;;;;;;;;;;;;
                ;;;;;;;;;;;;     ;;;;;
               ;;;;;    ;;;         \;;
              ;;;;;      ;;          |;
             ;;;;         ;          |
             ;;;                     |
              ;;                     )
               \    ~~~~ ~~~~~~~    /
                \    ~~~~~~~  ~~   /
              |\ \                / /|
               \\| %%%%%    %%%%% |//
              [[====================]]
               | |  ^          ^  |
               | | :@: |/  \| :@: | |
                \______/\  /\______/
                 |     (@\/@)     |
                /                  \
               /  ;-----\  ______;  \
               \         \/         /
                )                  (
               /                    \
               \__                  /
                \_                _/
                 \______/\/\______/
                  _|    /--\    |_
                 /%%\  /"'"'\  /%%\
  ______________/%%%%\/\'"'"/\/%%%%\______________
 / :  :  :  /  .\%%%%%%%\"'/%%%%%%%/.  \  :  :  : \
)  :  :  :  \.  .\%%%%%%/'"\%%%%%%/.  ./  :  :  :  (
    ''',
    "Skeleton": r'''
                              _.--""-._
  .                         ."         ".
 / \    ,^.         /(     Y             |      )\
/   `---. |--'\    (  \__..'--   -   -- -'""-.-'  )
|        :|    `>   '.     l_..-------.._l      .'
|      __l;__ .'      "-.__.||_.-'v'-._||`"----"
 \  .-' | |  `              l._       _.'
  \/    | |                   l`^^'^^'j
        | |                _   \_____/     _
        j |               l `--__)-'(__.--' |
        | |               | /`---``-----'"1 |  ,-----.
        | |               )/  `--' '---'   \'-'  ___  `-.
        | |              //  `-'  '`----'  /  ,-'   I`.  \
      _ L |_            //  `-.-.'`-----' /  /  |   |  `. \
     '._' / \         _/(   `/   )- ---' ;  /__.J   L.__.\ :
      `._;/7(-.......'  /        ) (     |  |            | |
      `._;l _'--------_/        )-'/     :  |___.    _._./ ;
        | |                 .__ )-'\  __  \  \  I   1   / /
        `-'                /   `-\-(-'   \ \  `.|   | ,' /
                           \__  `-'    __/  `-. `---'',-'
                              )-._.-- (        `-----'
                             )(  l\ o ('..-.
                       _..--' _'-' '--'.-. |
                __,,-'' _,,-''            \ \
               f'. _,,-'                   \ \
              ()--  |                       \ \
                \.  |                       /  \
                  \ \                      |._  |
                   \ \                     |  ()|
                    \ \                     \  /
                     ) `-.                   | |
                    // .__)                  | |
                 _.//7'                      | |
               '---'                         j_| `
                                            (| |
                                             |  \
                                             |lllj
                                             |||||  
    ''',
    "Zombie": r'''
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠯⣤⠼⣳⣄⠠⠴⢆⠹⣾⣥⠏⣱⡼⣿⣿⣿⣽⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⡴⣿⡛⢧⡀⢊⡷⣾⠟⣀⣴⣿⣾⣿⣿⣽⣿⣿⡌⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡓⣦⠆⢠⣄⢛⡒⣉⠀⠃⢀⠉⢉⣿⢿⣿⣿⣿⣿⣿⣿⠇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠡⡏⠀⡀⣀⣲⣿⣄⠀⠀⠀⡴⢿⣿⣿⣏⣻⠹⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣙⢹⣿⡐⠀⣤⣿⡏⠃⠹⣿⣿⣦⠀⢷⣿⣿⠁⠈⠹⣿⣿⣿⡏⠀⣿⠛⣄⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⢮⡷⠀⡀⢻⣿⣧⣤⣴⣿⣿⡟⠀⢻⣿⣿⡷⣶⣾⣿⣿⣿⡇⡕⣺⢀⣿⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡦⠁⣿⠰⣅⠹⣿⣿⣾⣿⣿⣿⣿⣧⣾⣿⣿⡟⠿⠿⢻⣽⣿⡇⠐⣿⠀⢿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢀⣿⡀⢌⣃⢸⣉⠉⣲⣿⣿⡿⠀⣿⡀⣙⢻⡦⣄⡀⠈⣿⣿⣌⣿⣀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡾⢿⣇⣾⣿⣰⡏⠹⣩⣿⣿⡿⠀⣽⣧⠈⣿⣷⣿⠀⠀⣻⡟⣰⡿⢿⢌⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡌⣿⣿⣿⢿⡇⣼⣿⡿⢿⡗⠀⢹⣿⠆⠹⣿⡧⠠⠀⢸⡇⣿⢣⡜⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣿⣿⡿⢻⡇⣿⣿⣿⣽⣷⣦⣿⣿⡆⠀⠈⢹⠄⢠⣼⡇⣿⣆⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣇⣿⣠⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⡀⠈⠃⣨⣿⢟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣭⠛⢿⠿⡿⢿⣿⡿⣿⣆⡀⠘⠃⢸⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣶⣧⣼⣿⣿⣿⣾⡇⢰⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣼⣿⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⡻⣏⡶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣓⢻⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣧⣻⣿⣿⣾⣿⣽⡛⣿⣿⣿⡏⠌⣿⠏⢼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⡌⠙⢿⣷⣿⣿⣾⣿⣿⣿⣿⣿⢡⡾⠃⢈⠨⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠐⡀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⡴⠀⠐⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡻⠍⢠⣝⢿⡇⠠⠁⠄⣀⣿⣿⣿⣿⣿⣿⣿⡏⠀⠄⡔⠰⢀⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⡼⠛⢇⣱⣏⡾⣿⣿⡄⠀⣾⢿⣿⣿⣿⣿⣿⣿⣿⡇⠀⣄⠀⢀⣾⣿⣿⣿⡟⣻⣯⣺⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠙⠦⣱⣾⣿⣿⣿⣿⣿⣷⣾⣿⢡⣿⣿⣿⣿⣿⣿⣿⠿⠿⣿⣠⣾⣿⣿⣟⣿⡷⣶⣿⣿⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⢐⣿⣿⣯⣿⣿⣻⣝⣩⣿⣷⡄⢹⣿⣿⣿⣿⣿⣿⣾⣦⣿⣿⣿⣿⣿⠟⠛⣷⣿⣿⣼⣿⣿⣿⡟⣫⠛⡽⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⢿⡴⣽⣿⣿⡹⣟⣾⣷⣿⡿⣟⡿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⡟⣽⣿⠛⠁⠠⣰⣿⣿⡿⣿⠿⣋⢳⠑⡈⠭⠲⣽⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿
⡿⠟⠋⠩⠌⢁⠀⠀⠀⠀⡁⢋⡿⣘⠻⡷⣯⣽⣍⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣷⣶⣿⣿⣿⡟⠁⠣⠐⢠⠃⠡⣐⢣⣿⣿⡿⠛⠉⠃⠀⠀⣾⡿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠀⣐⠉⣷⢻⡵⣫⠞⡈⢿⡿⣿⣗⣻⣯⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠏⠀⠀⠀⠀⢈⠀⠒⢠⣺⣽⠟⢀⠄⠀⠀⠀⠀⡽⣃⠞
⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠈⢎⣻⣼⠅⠈⣔⠻⡼⢻⡿⡿⡕⢻⣿⣿⣿⣿⣿⣿⣿⣇⣈⣿⣷⣿⣿⡿⢏⠀⠁⠁⠀⠀⠀⠀⠈⠀⣀⢚⢛⠁⠀⣆⠀⠀⠀⠀⢀⣷⡍⠊
⠀⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣘⠐⠎⣠⠈⣇⠈⠀⢀⣶⣻⢿⢀⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡹⣿⣿⢻⠿⡄⠈⠛⠀⠀⠀⠀⠀⠈⠈⠁⣨⠂⠁⢸⠯⡄⠀⠀⠀⣼⠟⠀⠁
⣰⠀⠀⠀⠀⠀⠀⠀⢀⠀⠠⠄⢨⡙⠲⠄⣿⢿⡿⣷⡾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣴⣿⣽⣫⢾⣽⣆⣥⣼⣤⣤⣤⣦⣲⡀⠐⠀⠀⢀⡞⢠⠇⠀⢠⣾⠏⠀⠀⠀
⢐⠁⠀⠀⠀⠀⠀⠀⠀⠂⠄⠠⠀⠀⠑⠆⢿⡳⣹⢖⡿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⡟⣿⣻⠞⣧⣿⣟⣿⣿⣿⣙⣏⣏⣧⡟⢻⡗⠀⠀⣘⠀⣿⠀⠀⣾⠃⠀⠀⠀⠀
    ''',
    "Slime": r'''
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⠻⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⡀⠈⠛⢿⣿⣿⣁⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⠟⠛⠛⠿⡄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⡟⢡⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⠀⣀⣉⣤⣤⣤⡀⣤⣄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠻⣿⣦⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣠⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⣽⣿⣷⣄⠀⠀⠀⠀
⠀⠀⣾⡿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣿⣿⣿⣿⣷⣄⠀⠀
⠀⢀⣼⡀⠀⠀⠈⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⣿⠃⠀
⠀⠘⠟⠁⠀⠀⠀⠀⢿⣿⣿⡿⠟⠋⠉⠉⠉⠙⢿⣿⣿⣿⡟⠁⠀⠀⢠⣿⡄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⢿⣿⣿⡦⠀⠙⠻⠟⠁⠀⠀⠀⠈⠛⠃⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ''',
    "dragon_rest": r'''
⠀⠀⠀⠀⠀⠀⣰⠂⠀⣼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡟⢆⢠⢣⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡘⡇⠹⢦⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠹⣦⣹⢸⡖⠤⢀⠀⠘⢿⠛⢔⠢⡀⠃⠣⠀⠇⢡⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠹⠀⡷⣄⠠⡈⠑⠢⢧⠀⢢⠰⣼⢶⣷⣾⠀⠃⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠤⢖⡆⠰⡙⢕⢬⡢⣄⠀⠑⢼⠀⠚⣿⢆⠀⠱⣸⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣤⡶⠮⢧⡀⠑⡈⢢⣕⡌⢶⠀⠀⣱⣠⠉⢺⡄⠀⢹⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⡸⠀⠈⡗⢄⡈⢆⠙⠿⣶⣿⠿⢿⣷⣴⠉⠹⢶⢾⡆⠀⠀⠀
⠀⠀⠀⢠⠶⠿⡉⠉⠉⠙⢻⣮⡙⢦⣱⡐⣌⠿⡄⢁⠄⠑⢤⣀⠐⢻⡇⠀⠀⠀
⠀⠀⠀⢀⣠⠾⠖⠛⢻⠟⠁⢘⣿⣆⠹⢷⡏⠀⠈⢻⣤⡆⠀⠑⢴⠉⢿⣄⠀⠀
⠀⠀⢠⠞⢃⢀⣠⡴⠋⠀⠈⠁⠉⢻⣷⣤⠧⡀⠀⠈⢻⠿⣿⡀⠀⢀⡀⣸⠀⠀
⠀⠀⢀⠔⠋⠁⡰⠁⠀⢀⠠⣤⣶⠞⢻⡙⠀⠙⢦⠀⠈⠓⢾⡟⡖⠊⡏⡟⠀⠀
⠀⢠⣋⢀⣠⡞⠁⠀⠔⣡⣾⠋⠉⢆⡀⢱⡀⠀⠀⠀⠀⠀⠀⢿⡄⠀⢇⠇⠀⠀
⠀⠎⣴⠛⢡⠃⠀⠀⣴⡏⠈⠢⣀⣸⣉⠦⣬⠦⣀⠀⣄⠀⠀⠈⠃⠀⠀⠙⡀⠀
⠀⡸⡁⣠⡆⠀⠀⣾⠋⠑⢄⣀⣠⡤⢕⡶⠁⠀⠀⠁⢪⠑⠤⡀⠀⢰⡐⠂⠑⢀
⠀⠏⡼⢋⠇⠀⣸⣟⣄⠀⠀⢠⡠⠓⣿⠇⠀⠀⠀⠀⠀⠑⢄⡌⠆⢰⣷⣀⡀⢸
⠀⣸⠁⢸⠀⢀⡿⡀⠀⠈⢇⡀⠗⢲⡟⠀⠀⠀⠀⠀⠀⠀⠀⠹⡜⠦⣈⠀⣸⡄
⠀⣧⠤⣼⠀⢸⠇⠉⠂⠔⠘⢄⣀⢼⠃⡇⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⠚⠳⠋⠀
⠐⠇⣰⢿⠀⣾⢂⣀⣀⡸⠆⠁⠀⣹⠀⢡⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢀⡏⣸⠀⣟⠁⠀⠙⢄⠼⠁⠈⢺⠀⠘⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠈⡏⣸⢰⡯⠆⢤⠔⠊⢢⣀⣀⡼⡇⠀⠹⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢠⢻⢸⡇⠀⠀⠑⣤⠊⠀⠀⠈⣧⠀⠀⠙⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠸⣼⢸⠟⠑⠺⡉⠈⢑⠆⠠⠐⢻⡄⠀⠀⠈⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⡟⣸⡀⠀⠀⣈⣶⡁⠀⠀⠀⢠⢻⡄⠀⠀⠀⠑⠤⣄⡀⠀⠀⠀⠀⠀⠀
⠀⠀⢰⠁⣿⡿⠟⢏⠁⠀⢈⠖⠒⠊⠉⠉⠹⣄⠀⠀⠀⠀⠀⠈⠑⠢⡀⠀⠀⠀
⠀⣀⠟⢰⡇⠀⠀⠈⢢⡴⠊⠀⠀⠀⠀⠀⣸⢙⣷⠄⢀⠀⠠⠄⠐⠒⠚⠀⠀⠀
⠘⠹⠤⠛⠛⠲⢤⠐⠊⠈⠂⢤⢀⠠⠔⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠣⢀⡀⠔⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ''',
    "Dragon": r'''
⠤⢁⠄⠀⠀⠀⠀⠈⠙⠛⠷⣦⡄⡀⠀⠀⠀⠀⠀⠀⠤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⠀⠀⢀⣴⠟⠁⠀⠀
⣶⢦⣦⣤⣤⣤⣤⣤⣄⣀⣀⣀⣉⠛⠳⣔⣤⡀⠀⠀⠀⣿⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣇⡀⣠⡿⠋⣀⣴⠶⠛
⠠⠀⠀⠀⠀⠀⠈⠀⠀⠀⠉⠈⠉⠉⠉⢛⣻⣿⣷⣶⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢙⣿⣿⣿⡟⣛⠁⠀⠀⠀
⢂⠡⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡴⠾⠛⠉⣹⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣀⣀⣤⣤⣤⣶⣶⢶⣤⣀⣀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⢯⣍⠙⠛⠛⠛⠛
⠀⠄⠀⠀⠀⠀⢀⣀⣤⡼⠿⠟⠃⠀⠀⠀⣠⡿⢻⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⠿⠿⢿⢻⣿⣿⢿⣿⢿⣼⣿⡀⠀⠀⠀⠀⠀⠀⠀⢿⣿⠀⠘⢿⣄⠀⠀⠀
⠈⢄⣶⣶⣶⠿⠟⠋⠉⠀⠀⠀⠀⠀⠀⣼⠟⠅⢸⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣾⢷⡯⢗⣻⡖⠓⢒⣃⣤⣄⣠⣾⣿⡇⠀⠀⠀⠀⠀⠀⠀⣿⣿⠀⠀⠀⠙⢻⣦⡄
⣼⡿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⠃⠰⠀⣿⣿⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡺⣻⣯⣿⣙⣾⡟⢸⠺⣿⣿⣿⡟⢉⠏⠉⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⡄⠀⠀⠀⠀⠙⢿
⢡⠀⠄⠀⢀⠀⠀⠀⠀⠀⠀⠀⣴⡿⠁⠀⠀⢰⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢼⣇⠎⣸⢣⡟⢃⣏⣓⢷⡹⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⡇⠀⠀⠄⠀⠀⠌
⢢⢉⠄⠃⢄⠀⠂⠀⠀⠀⠀⣼⡟⠁⠀⠀⠀⣾⣿⣽⠨⠀⡀⠀⠀⠀⠀⠀⠀⠀⠠⢿⠀⠁⣇⠊⠠⢞⠋⠉⠉⠑⣽⢿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⡄⠀⠀⡜⢠⡉⠖
⠥⣊⠌⡅⢢⠈⢅⠂⠄⠂⣸⡿⢁⠀⠤⠀⠀⣿⣿⠇⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⣿⣁⡆⡟⠀⠀⢲⠀⠀⠀⠀⠈⠪⠾⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⡤⣿⣿⠂⡀⡐⣌⠣⡜⣩
⢒⡡⢊⠴⣁⠚⣄⠊⠤⣡⣿⠁⠆⡈⠔⠀⠀⣿⣿⢇⠀⠀⠀⠀⠀⠑⠀⠀⠀⠀⠈⢙⣏⣴⠹⡠⢀⠠⠐⠠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡐⠤⡑⣌⠳⣜⡵
⢢⠘⣌⠲⢌⡓⡌⣍⢲⡿⡡⢎⡐⠬⠀⠐⠀⣿⣯⢧⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠹⣖⡆⠈⠢⡢⠀⠀⠈⠐⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⣾⡿⣿⢀⠧⣑⠮⣝⢮⣳
⢀⢉⡀⢷⡈⢶⢱⣈⣿⢇⡱⢆⡸⠆⠀⠁⠀⣿⣏⢿⠀⠀⠀⠀⠀⠀⠆⠀⠀⠀⠀⠀⠀⠈⢿⣇⠁⣀⠆⠆⠀⠀⠀⠰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣾⣿⡇⡎⢶⣉⡾⣹⡾⢷
⢈⠢⡘⢆⡙⣆⢧⣿⣏⠞⣔⠣⡜⢡⠂⡁⠀⢿⣿⣟⡀⠄⠂⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⣬⠦⠀⢄⠀⠀⠀⠀⠢⠀⠀⠀⠀⠀⠀⠀⢰⣟⣾⡿⢱⡘⢦⡻⣼⣳⢟⡿
⠀⢢⠑⡎⣵⢪⣿⣟⣬⢻⣌⠷⣌⢣⡘⠀⠀⢸⣿⣿⡷⣈⠁⠈⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⣮⠠⡵⠀⠀⠀⠀⢁⠀⠀⠀⠀⢀⠴⢋⣿⢻⢃⠧⣜⢧⣟⣳⢯⣿⠙
⠀⢢⡙⡜⣶⣻⣟⡾⣼⢳⣎⢷⣊⢦⡙⠤⠀⣼⣿⣿⣿⣦⡑⠀⠄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣷⣷⡀⠀⠀⠀⠘⠀⠀⢀⠴⡁⣰⠞⣿⣿⢘⢮⡝⣾⡽⣫⠟⠁⠀
⠀⢥⢪⢵⣣⣿⣻⢾⣽⣳⣻⢮⣝⡮⡵⣉⢦⣿⡿⠀⠈⠙⠻⢷⣦⣀⡅⢠⠐⠠⠄⣀⠀⣠⠄⠢⠂⠝⠋⢻⣿⡒⠠⠄⣀⠀⢐⠆⠂⠐⣴⠟⠉⠀⣿⣏⢞⣮⣽⣳⡟⠁⠀⠀⠀
⠣⣎⢮⣳⣿⣻⣽⣻⣞⡷⣯⣟⡾⣵⡳⣕⣾⣿⠃⡄⠀⠀⠀⠀⠈⠉⠛⠿⢶⣥⣴⣠⡞⠀⠂⠀⣥⠈⡁⡢⠗⣀⠠⠀⡀⠀⢸⢘⡼⠟⠁⠀⢠⠌⣿⣏⡾⣮⢷⡛⠁⠀⠀⠀⠀
⠀⠻⣮⢷⣿⣳⢯⡷⣯⣟⡷⣯⣟⣷⣻⢞⣿⢧⣋⠴⡩⢔⢢⡐⡀⠄⡀⢀⠀⣤⣾⢻⠄⠒⡉⠐⡬⠐⠈⠊⡀⠀⠡⠁⠒⠐⠻⣨⠇⣠⢂⡍⢦⡙⣿⣯⢷⣯⡟⠀⠀⠀⠀⠀⠀
⠀⠀⢫⣿⢷⣯⠿⠙⠓⠯⣟⣷⣻⢾⣽⣻⣟⣳⣎⢷⣙⣎⢦⡱⣍⣶⡷⣞⢿⣛⣬⡻⡌⠡⡀⣷⠇⠁⢀⠀⠈⠂⢁⣐⡀⡼⢨⢈⡗⣦⢳⡜⣧⣻⣽⣯⣟⡞⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢺⣿⠋⠀⠀⠀⠀⠀⠘⣷⣯⣿⣾⣿⣽⢳⡞⣯⣾⣼⢣⣷⣾⣯⣷⠛⡏⢹⡌⡆⢱⣤⡞⡍⠈⡄⠀⠑⡄⠈⡄⠀⠀⠀⢸⡌⢹⡞⣧⡟⣷⢻⣾⢳⣯⠃⠀⠀⠀⠀⠀⠀⠀
⠀⢀⡿⠉⠀⠀⠀⠀⠀⠀⠀⣿⣞⡷⣿⣯⣟⣯⢿⡽⣞⣧⣿⡿⣫⣿⢶⣎⣳⡼⣷⢿⠛⢡⠀⠱⡀⢈⠢⡀⢈⠠⠐⠀⠀⠈⣟⠁⣼⡿⣽⣻⣽⣻⢾⣟⡏⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠸⠁⠀⠀⠀⠀⠀⠀⠀⠀⢸⣯⢿⣟⣾⡽⣞⣯⢿⡽⣞⣯⣿⣟⣯⣿⡿⠿⡽⢃⠁⢃⠀⠳⠀⡑⢄⠀⠉⠐⠠⠤⠄⠐⣸⢧⣾⢿⣽⣳⣟⡾⣽⣻⣟⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⠂⠀⠀⠀⠀⢸⣯⣿⣟⡾⣽⣻⣞⣯⢿⡽⣿⣻⡿⣾⣿⣵⢐⢳⡘⡄⠘⡂⠄⡑⢄⠠⠑⠪⠄⢀⠀⢀⣾⣽⣻⣞⡿⣞⡷⣯⣟⣷⣻⡝⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠀⠀⠀⠈⠀⠀⣼⣻⣷⢯⡿⣽⣳⣟⡾⣯⣟⡷⣯⢿⡿⡟⣿⠘⡴⡅⠘⢄⠐⠠⢀⡂⢈⠐⢠⣐⣤⣾⣟⡽⣞⡷⣯⢿⣽⣻⢷⣻⢾⣽⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ''',
    "dragon_death": r'''
    .    .
    \\  //  .''-.     .-.
    \ \/ /.'     '-.-'   '.
~__\(    )/ __~            '.    ..~
(  . \!!/    . )     .-''-.  '..~~~~
 \ | (--)---| /'-..-'BP    '-..-~'
  ^^^ ''   ^^^
    '''
    }

class Location(object):
    '''A base class containing all future locations'''
    def __init__(self, name, description="", art=""):
        self.name = name
        self.description = description
        self.art = art

class Town(Location):
    '''A town class inherited from Entity'''
    
    def __init__(self, name, description="", art=""):
        super().__init__(name, description, art)
        
    def __str__(self):
        rep = self.name
        return rep

class Forest(Location):
    '''A forest class inherited from Entity'''
    
    def __init__(self, name, description="", art=""):
        super().__init__(name, description, art)
        
    def __str__(self):
        rep = self.name
        return rep

class Cave(Location):
    '''A cave class inherited from Entity'''
    
    def __init__(self, name, description="", art=""):
        super().__init__(name, description, art)
    
    def __str__(self):
        rep = self.name
        return rep

class Entity(object):
    '''A base class containing all future game entities'''

    def __init__(self, name, damage, health):
        self.damage = damage
        self.health = health
        self.name = name
        
    # POLYMORPHISM !!! death method is overridden in inherited classes: player, boss
    def death(self):
        slow_print(f"\n{self.name} felled.")

class Player(Entity):
    '''A player class inherited from Entity'''

    def __init__(self, name, damage, max_health, current_health, current_location, potions, coins, xp, level = 1):
        self.name = name
        self.damage = damage
        self.max_health = max_health
        self.current_health = current_health
        self.current_location = current_location
        self.potions = potions
        self.coins = coins
        self.level = level
        self.xp = xp
        self.xp_to_level_up = 40
        
    def gain_xp(self):
        # player gains xp when defeating an enemy
        self.xp += 15
        if (self.xp >= self.xp_to_level_up):
            self.level_up()
            self.xp = 0
        
    def level_up(self):
        # player levels up when reaching certain xp 
        self.level += 1
        self.damage += 3
        self.max_health += 15
        self.current_health += 15
        self.xp_to_level_up = int(self.xp_to_level_up * 1.15)
        slow_print(f"You leveled up and are now level {self.level}!")
        slow_print(f"You now deal {self.damage} damage and have a max health of {self.max_health}.")
        
    def buy_potion(self):
        # buys potions if player has 15 coins
        if (self.coins >= 15):
            if (self.potions < 5):
                self.potions += 1
                self.coins -= 15
                slow_print("You purchase the potion from the merchant.")
                slow_print(f"You now have {self.potions} potion(s) and {self.coins} coin(s) remaining.")
            else:
                slow_print("You already have the max amount of potions you can carry.")
        
    def use_potion(self):      
        # use potion if the player has one
        if (self.potions > 0) and (self.current_health < self.max_health):
            self.current_health += 20
            if (self.current_health > self.max_health):
                self.current_health = self.max_health
            self.potions -= 1
            slow_print("You used a potion and healed 20 HP.")
            slow_print(f"You have {self.potions} potions remaining.")
            slow_print(f"You now have {self.current_health} HP")
        elif (self.potions <= 0):
            slow_print("You do not have any potions left!")
        elif (self.current_health >= self.max_health):
            slow_print("You are already at max HP!")
        
    def death(self):
        # called from enemy and boss's attack methods when player (target) current health equals 0 --- also an overridden method from entity class
        slow_print(ascii_art["death"], delay = 0.001)
        sys.exit()
        
    def talk(self):
        # speak to an npc if any at current player location
        buy = None
        while (buy != 2):
            slow_print("\n======================================\n")
            slow_print(ascii_art["merchant"], delay = 0.001)
            slow_print("A merchant offers you a strange-looking potion for 15 coins")
            slow_print(f"You have {self.coins} coin(s).")
            slow_print("Will you buy one?")
            slow_print('''
1 - Yes
2 - No
''')
            try:
                buy = int(input(""))
            except ValueError:
                slow_print("Invalid selection. Please try again.")
            if (buy == 1):
                if (self.coins >= 15):
                    self.buy_potion()
                else:
                    slow_print("You do not have enough coins. Come back later.")
                    break
            elif (buy == 2):
                slow_print("You do not purchase a potion. Maybe that was a good choice.")
                break

    def attack(self, target):
        # attack the player's target if the player is alive
        if (self.current_health <= 0):
            return
        else:
            target.health -= self.damage

        if (target.health <= 0):
            target.health = 0

        slow_print(f"{self.name} attacks {target.name} for {self.damage} damage")
        slow_print(f"{target.name} is at {target.health} HP\n")

        # kill the target if health is below 0
        if (target.health <= 0):
            target.death()
            self.coins += 10
            slow_print(f"You collect 10 coins and now have a total of {self.coins} coin(s).")
            self.gain_xp()
            self.xp_needed = self.xp_to_level_up - self.xp
            slow_print(f"You gain 15 XP and need {self.xp_needed} more XP to level up.")

class Enemy(Entity):
    '''An enemy class inherited from Entity'''
    
    # list of enemies to fight
    enemies = ["Skeleton", "Slime", "Zombie"]

    def __init__(self, name, damage, health):
        super().__init__(name, damage, health)

    # called from player's attack method when enemy (target) health equals 0
    def death(self):
        slow_print(f"\n{self.name} felled.")
        
    # attack the player if enemy is still alive
    def attack(self, target):
        if (self.health <= 0):
            return
        else:
            target.current_health -= self.damage

        if (target.current_health <= 0):
            target.current_health = 0

        slow_print(f"{self.name} attacks {target.name} for {self.damage} damage")
        slow_print(f"{target.name} is at {target.current_health} HP\n")

        # kill the player if health is below 0
        if (target.current_health <= 0):
            target.death()
            
class Boss(Entity):
    '''A boss class inherited from Entity'''
    
    def __init__(self, name, damage, health):
        super().__init__(name, damage, health)

    # called from player's attack method when boss (target) health equals 0 --- also an overridden method from entity class
    def death(self):
        slow_print(f"\nThe ancient dragon falls to the soggy, bleak stone inside the cave. The dragon begins to breathe slower and slower and you see the terror")
        slow_print("in its eyes. Yet, it seems proud to have fought someone as strong as you. But are you proud? Do you feel acomplished at what")
        slow_print("you have achieved, for better, or for worse? Was everything you killed worth it? All of the pain you have caused other creatures?")
        slow_print(f"Once more, that is for you to decide. You live with your decisions. Each... and every one...")
        slow_print(ascii_art["dragon_death"], delay = 0.0001)
        sys.exit()
        
    # attack the player if enemy is still alive
    def attack(self, target):
        if (self.health <= 0):
            return
        else:
            target.current_health -= self.damage

        if (target.current_health <= 0):
            target.current_health = 0

        slow_print(f"{self.name} attacks {target.name} for {self.damage} damage")
        slow_print(f"{target.name} is at {target.current_health} HP\n")

        # kill the target if health is below 0
        if (target.current_health <= 0):
            slow_print("Very disappointing... I thought you were.. stronger..", delay = 0.1)
            target.death()

# CLIENT !!!!
def main():
    incorrect_spellings = ["Devin", "Devon", "Devyn", "Devan", 
                       "devin", "devon", "devyn", "devan",
                       "DEVIN", "DEVON", "DEVYN", "DEVAN"]
    
    unique_names = ["KENNON", "kennon", "Kennon"]
        
    slow_print(ascii_art["title"], delay = 0.001)
    
    slow_print("What is your name, adventurer?")
    user_name = input("").strip()
    
    if (user_name in incorrect_spellings):
        slow_print("You spelled your name wrong. Let me help you, \'Deven.\'\n")
        user_name = "Deven"
    elif (user_name in unique_names):
        slow_print("Thou art a man of monstrous girth.\n")
    
    # define locations + descriptions
    town = Town("Town", "A small, secluded town.", ascii_art["town"])
    forest = Forest("Forest", "A dark, deep forest.", ascii_art["forest"])
    cave = Cave("Cave", "A cave filled with various ore... and monsters.", ascii_art["cave"])
    
    # define player and enemy + attributes
    player = Player(name = user_name, damage = 10, max_health = 100, current_health = 100, current_location = town, potions = 0, coins = 0, xp = 0, level = 1)
    enemy = Enemy(name = random.choice(Enemy.enemies), damage = random.randrange(4, 6), health = random.randrange(45, 55))
    boss = Boss(name = "Ancient Dragon", damage = 30, health = 200)

    slow_print("All around is a quaint, secluded town set in an expansive field. The sound of merchants being haggled by travelers and")
    slow_print("blacksmiths slaving away in the heat of the sun overpowers the sound of birds chirping from within the trees nearby.")
    slow_print("There is an extensive, hefty fence surrounding various types of livestock all awaiting their communal deaths.")
    slow_print("It appears to be a safe place to rest, but it is almost uncanny in nature and essence; a very familiar sight.")
    slow_print(ascii_art["town"], delay = 0.0001)

    # game loop
    user_input = None
    while (True):
            # initial player choice
            slow_print("\n======================================\n")
            slow_print(f"You are currently at {player.current_location}")
            slow_print('''
1 - Fight
2 - Travel
3 - Talk
''')
            try:
                user_input = int(input(""))
            except ValueError:
                print("Try again")
                continue
            if (user_input == 1) and (player.current_location == forest):
                slow_print(ascii_art[enemy.name], delay = 0.0001)
                slow_print(f"You encounter {enemy.name}. The foe has {enemy.health} HP and inflicts {enemy.damage} damage.")
                slow_print(f'''
Your stats -
Level: {player.level}
Max HP: {player.max_health}
Current HP: {player.current_health}
Damage per attack: {player.damage}
Potions: {player.potions}
Coins: {player.coins}''')
                while (enemy.health > 0):
                    # forest enemy fight
                    slow_print("\n======================================\n")
                    slow_print(f"{enemy.name} stares menacingly.")
                    slow_print('''
1 - Attack
2 - Use Potion (20 HP)
3 - Flee
''')
                    try:
                        combat_input = int(input(""))
                    except ValueError:
                        slow_print("Invalid selection. Please try again.")
                        continue
                    if (combat_input == 1):
                        player.attack(enemy)
                        enemy.attack(player)
                    elif (combat_input == 2):
                        player.use_potion()
                    elif (combat_input == 3):
                        slow_print("You decide to flee the battle you chose to take.")
                        enemy = Enemy(name = random.choice(Enemy.enemies), damage = random.randrange(4, 6), health = random.randrange(45, 55))
                        break
                if (enemy.health <= 0):
                    enemy = Enemy(name = random.choice(Enemy.enemies), damage = random.randrange(4, 6), health = random.randrange(45, 55))
            elif (user_input == 1) and (player.current_location == town):
                slow_print("You glance around and find no enemies to fight. There are only townspeople roaming about.")
                continue
            elif (user_input == 1) and (player.current_location == cave):
                if (player.level < 5):
                    slow_print(ascii_art["dragon_rest"], delay = 0.0001)
                    slow_print("I will not battle an unworthy, worthless, dishonorable adversary... It would not be entertaining.. for me...", delay = 0.1)
                if (player.level >= 5):
                    slow_print(ascii_art["Dragon"], delay = 0.0001)
                    slow_print("Finally! A worthy opponent has come upon my sight!", delay = 0.1)
                    slow_print(f"You stand before the {boss.name}. This malicious creature has {boss.health} HP and inflicts {boss.damage} damage.")
                    slow_print(f'''
Your stats -
Level: {player.level}
Max HP: {player.max_health}
Current HP: {player.current_health}
Damage per attack: {player.damage}
Potions: {player.potions}
Coins: {player.coins}''')
                    while (boss.health > 0):
                        # final boss fight 
                        slow_print("\n======================================\n")
                        slow_print("The ancient dragon breathes heavily.")
                        slow_print('''
1 - Attack
2 - Use Potion (20 HP)
3 - Flee
''')
                        try:
                            combat_input = int(input(""))
                        except ValueError:
                            slow_print("Invalid selection. Please try again.")
                            continue
                        if (combat_input == 1):
                            player.attack(boss)
                            boss.attack(player)
                        elif (combat_input == 2):
                            player.use_potion()
                        elif (combat_input == 3):
                            slow_print("You cannot run away this time.")
                            continue
            elif (user_input == 2):
                # traveling between locations
                slow_print("\n======================================\n")
                slow_print("Where would you like to travel?")
                slow_print('''
1 - Town
2 - Forest
3 - Cave
''')
                try:
                    destination_input = int(input(""))
                except ValueError:
                    slow_print("Invalid selection. Please try again.")
                    continue
                if (destination_input == 1) and (player.current_location != town):
                    player.current_location = town
                elif (destination_input == 2) and (player.current_location != forest):
                    player.current_location = forest
                elif (destination_input == 3) and (player.current_location != cave):
                    player.current_location = cave
                elif (destination_input == 1) and (player.current_location == town):
                    slow_print("You are already at this location!")
                    continue
                elif (destination_input == 2) and (player.current_location == forest):
                    slow_print("You are already at this location!")
                    continue
                elif (destination_input == 3) and (player.current_location == cave):
                    slow_print("You are already at this location!")
                    continue
                else:
                    slow_print("Invalid destination. Try again.")
                    continue
                slow_print(player.current_location.art, delay = 0.0001)
                slow_print(f"You travel to {player.current_location.name}.")
                slow_print(player.current_location.description)
            elif (user_input == 3) and (player.current_location == forest) or (player.current_location == cave):
                slow_print("You look around and find not a single being to speak to.")
                continue
            elif (user_input == 3) and (player.current_location == town):
                player.talk()
            else:
                slow_print("Invalid selection. Please try again.")
                continue

main()