import tkinter as tk
class PolicyGUI(tk.Tk):
    """
    GUI for Figure 4.1
    """

    def __init__(self, env, agent, data_parser, n_steps=5):
        self.env = env
        self.agent = agent
        self.data_parser = data_parser

        self.step = 0
        self.cache = []

        # Precompute state values
        for _ in range(n_steps):
            self.cache.append(agent.v)
            agent.update(data_parser)

        tk.Tk.__init__(self)
        print(self.cache)
        self._update_canvas()

    
    def keymax(dict_):
        """
        Get list of keys in a dictionary with maximum value.
        """
        max_v = max(dict_.values())
        return [key for key in dict_.keys() if dict_[key] == max_v]

    def _update_canvas(self):
        """
        Updates the canvas.
        """
        v = self.cache[self.step]
        print(v)

        # Update V
        for state in enumerate(v):
            print(format(v[state]))
