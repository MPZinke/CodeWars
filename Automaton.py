

# https://www.codewars.com/kata/5268acac0d3f019add000203


class Automaton(object):

    def __init__(self):
        self.states = [1, 2, 3]
        self._accept_states = [2]

        self._start_state = 1
        self._current_state = self._start_state
        # {<state>: {input: <next state>, ...}, ...}
        self._transition_functions = {1: {"0": 1, "1": 2}, 2: {"0": 3, "1": 2}, 3: {"0": 2, "1": 2}}

    def read_commands(self, commands):
        for command in commands:
            self._current_state = self._transition_functions[self._current_state][command]
            
        return self._current_state in self._accept_states


my_automaton = Automaton()
