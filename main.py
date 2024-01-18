from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.shortcuts import ProgressBar
from prompt_toolkit.completion import NestedCompleter

from datetime import datetime
import json
import translators as ts

MainFilePath = None
TranslatedText = {}
NotTranslatedText = {}

mainCompleter = NestedCompleter.from_nested_dict(
    {'run': None, 'stop': None, 'exit': None, 'load': None, 'resume': None, 'save': None})


mainCompleter.ignore_case = True



def Translating(ObjToTranlate=None):
    try:
        completeObj = {}
        for i in ObjToTranlate:
            completeObj[i] = None
        translateCompleter = NestedCompleter.from_nested_dict({'/save': None, '/edit': completeObj})
        translateCompleter.ignore_case = True
        MainText = ObjToTranlate
        for line in MainText:

            print(
                f'{line}:{MainText[line]}:{ts.translate_text(MainText[line], translator="bing", to_language="ru")}')
            command = prompt('> ',
                            completer=translateCompleter,
                            auto_suggest=AutoSuggestFromHistory()).split(' ')
            match command[0]:
                case '/stop':
                    print("Tranlating stoped")
                    break
                case '':
                    TranslatedText[line] = ts.translate_text(MainText[line], translator="bing", to_language="ru")
                case '/edit':
                    try:
                        LastTranslatedText = TranslatedText[command[1]]
                        TranslatedText[command[1]] = command[2]
                        print(f"{command[1]}:{LastTranslatedText} -> {command[2]}")
                    except:
                        print("Line not found")

                case _:
                    TranslatedText[line] = ' '.join(command)
    except Exception as e:
        print(f"Unknown ERROR {e}")


def StartTranslate(path=None):
    try:
        with open(path, 'r') as file:
            Translating(json.loads(file.read()))




    except:
        print("File not found")


def ResumeTranslate():
    with open('translation.unf', 'r') as file:
        TranslatedText = json.loads(file.read())
    with open('translation.inc', 'r') as file:
        NotTranslatedText = json.loads(file.read())
    Translating(NotTranslatedText)


def main():
    global MainFilePath
    while True:
        text = prompt('> ',
                      completer=mainCompleter,
                      auto_suggest=AutoSuggestFromHistory()).split(' ')
        match text[0]:
            case 'stop' | 'exit':
                exit(0)
            case 'load':
                MainFilePath = text[1]
                print(f"File {MainFilePath} selected as Main")
            case 'run':
                StartTranslate(path=MainFilePath)
            case 'resume':
                ResumeTranslate()
            case 'save':
                if TranslatedText and not NotTranslatedText:
                    with open(f'{text[1]}.json', 'w') as file:
                        file.write(json.dumps(TranslatedText, indent=4))
                        break
                if TranslatedText and NotTranslatedText:
                    with open('translation.unf', 'w') as file:
                        file.write(json.dumps(TranslatedText, indent=4))
                    with open('translation.inc', 'w') as file:
                        file.write(json.dumps(NotTranslatedText, indent=4))
                if not TranslatedText:
                    print('No translation yet')


if __name__ == "__main__":
    main()
