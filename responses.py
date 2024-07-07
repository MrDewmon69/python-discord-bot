from random import choice, randint

def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return "Well you're pretty quiet"
    elif 'hello' in lowered:
        return 'Hello there!'
    else:
        return choice(['Your done kid', 'womp womp', 'I\'m stupid! yay'])