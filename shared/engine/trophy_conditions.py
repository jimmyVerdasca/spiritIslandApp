CONDITIONS = {}


def trophy_condition(name):

    def decorator(function):
        CONDITIONS[name] = function
        return function

    return decorator



@trophy_condition("five_win_streak")
def five_win_streak(games):

    streak = 0

    for game in games:

        if game.result == "Victory":

            streak += 1

            if streak >= 5:
                return True

        else:

            streak = 0

    return False