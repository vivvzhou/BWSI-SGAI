import math
import tkinter as tk
from ui_elements.button_menu import ButtonMenu
from ui_elements.capacity_meter import CapacityMeter
from ui_elements.clock import Clock
from endpoints.machine_interface import MachineInterface
from ui_elements.game_viewer import GameViewer
from ui_elements.machine_menu import MachineMenu
from ui_elements.role_tracker import RoleTracker
from ui_elements.injured_chance import InjuredChance
from ui_elements.hp_bar import HpBar
from os.path import join
from playsound import playsound


class UI(object):
    def __init__(self, data_parser, scorekeeper, data_fp, is_disable):
        #  Base window setup
        w, h = 1280, 800
        self.root = tk.Tk()
        self.root.title("Beaverworks SGAI 2023 - Dead or Alive")
        self.root.geometry(str(w) + 'x' + str(h))
        self.root.resizable(False, False)
        self.humanoid = data_parser.get_random()
        if not is_disable:
            self.machine_interface = MachineInterface(self.root, w, h)

        #  Add buttons and logo
        user_buttons = [("Skip", lambda: [scorekeeper.skip(self.humanoid),
                                          self.update_ui(scorekeeper),
                                          self.get_next(
                                            data_fp,
                                            data_parser,
                                            scorekeeper, playsound('skipSound.wav'))]),
                        ("Squish", lambda: [self.injured_chance.convertHypothetical(self.humanoid),
                                            scorekeeper.squish(self.humanoid),
                                            self.update_ui(scorekeeper),
                                            self.get_next(
                                                data_fp,
                                                data_parser,
                                                scorekeeper, playsound('362335__balloonhead__ow.wav')),]),
                        ("Cure", lambda: [scorekeeper.save(self.humanoid, True),
                                          self.update_ui(scorekeeper),
                                          self.get_next(
                                              data_fp,
                                              data_parser,
                                              scorekeeper, playsound('345503__robinhood76__06624-taking-pills-sounds.wav')), ]),
                        ("Save", lambda: [self.injured_chance.convert(self.humanoid),
                                          scorekeeper.save(self.humanoid, False),
                                          self.update_ui(scorekeeper),
                                          self.get_next(
                                              data_fp,
                                              data_parser,
                                              scorekeeper, playsound('448908__daniel-cabanas__sliding-door.wav')), ]),
                        ("Scram", lambda: [scorekeeper.scram(),
                                           self.update_ui(scorekeeper),
                                           self.get_next(
                                               data_fp,
                                               data_parser,
                                               scorekeeper, playsound('345335__willybilly1984__rfx_car-engine-acelerator-and-switch-off.wav')), ])]
        
        role_indicator = [True, True, True, True]
        
        self.button_menu = ButtonMenu(self.root, user_buttons)
        self.role_tracker = RoleTracker(self.root, role_indicator)
        #self.cure = InjuredChance(self.humanoid, self.root)
        self.injured_chance = InjuredChance(self.humanoid, self.root)
        self.role_tracker.create_role(self.humanoid.profession, self.humanoid.age)

        if not is_disable:
            machine_buttons = [("Suggest", lambda: [self.machine_interface.suggest(self.humanoid)]),
                               ("Act", lambda: [self.machine_interface.act(scorekeeper, self.humanoid),
                                                self.update_ui(scorekeeper),
                                                self.get_next(
                                                    data_fp,
                                                    data_parser,
                                                    scorekeeper)])]
            self.machine_menu = MachineMenu(self.root, machine_buttons)

        #  Display central photo
        self.game_viewer = GameViewer(self.root, w, h, data_fp, self.humanoid)
        self.root.bind("<Delete>", self.game_viewer.delete_photo)

        # Display the countdown
        init_h = (12 - (math.floor(scorekeeper.remaining_time / 60.0)))
        init_m = 60 - (scorekeeper.remaining_time % 60)
        self.clock = Clock(self.root, w, h, init_h, init_m)
        
        self.hp_bar = HpBar(self.root, data_parser.hp)

        # Display ambulance capacity
        self.capacity_meter = CapacityMeter(self.root, w, h, data_parser.capacity)
        
        # Display hp bar
        self.hp_bar = HpBar(self.root, data_parser.hp)

        self.root.mainloop()

    def update_ui(self, scorekeeper):
        h = (12 - (math.floor(scorekeeper.remaining_time / 60.0)))
        m = 60 - (scorekeeper.remaining_time % 60)
        self.clock.update_time(h, m)
        self.capacity_meter.update_fill(scorekeeper.get_current_capacity())
        self.hp_bar.update_hp(scorekeeper.get_hp())

    def on_resize(self, event):
        w, h = 0.6 * self.root.winfo_width(), 0.7 * self.root.winfo_height()
        self.game_viewer.canvas.config(width=w, height=h)

    def get_next(self, data_fp, data_parser, scorekeeper, next_song):
        remaining = len(data_parser.unvisited)
        # Ran out of humanoids? Disable skip/save/squish
        if remaining == 0 or scorekeeper.remaining_time <= 0:
            self.capacity_meter.update_fill(0)
            self.game_viewer.delete_photo(None)
            self.game_viewer.display_score(scorekeeper.get_score(), scorekeeper.totalKilled, scorekeeper.totalSaved)
            self.role_tracker.delete_role()
        else:
            humanoid = data_parser.get_random()
            # Update visual display
            self.humanoid = humanoid
            fp = join(data_fp, self.humanoid.fp)
            self.game_viewer.create_photo(fp)
            self.role_tracker.update_role_tracker(scorekeeper.remaining_roles)
            self.role_tracker.create_role(self.humanoid.profession, self.humanoid.age)
            self.injured_chance.update(self.humanoid)

        # Disable button(s) if options are no longer possible
        self.button_menu.disable_buttons(scorekeeper.remaining_time, remaining, scorekeeper.at_capacity(), scorekeeper.get_hp())