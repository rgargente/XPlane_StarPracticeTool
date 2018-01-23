VERSION = "0.9.0"

import os
from datetime import datetime

from PythonScriptMessaging import *
from SandyBarbourUtilities import *
from XPLMDataAccess import *
from XPLMDefs import *
from XPLMDisplay import *
from XPLMGraphics import *
from XPLMMenus import *
from XPLMNavigation import *
from XPLMProcessing import *
from XPLMUtilities import *
from XPStandardWidgets import *
from XPWidgetDefs import *
from XPWidgets import *

import starpracticetool_lib.mathlib as mathlib
from starpracticetool_lib.cifplib import Cifp
from starpracticetool_lib.xplm_wrapper import XplmWrapper

FILE_LOG = "STAR_Practice_Tool.log"
FILE_PRE = "STAR_Practice_Tool.prf"

SHOW_SPT_PANEL_MENUITEMREF = 1

MARGIN_W = 30
MARGIN_H = 30
WINDOW_W = 350
WINDOW_H = 220


# noinspection PyUnresolvedReferences
class PythonInterface:
    def XPluginStart(self):
        self.Name = "STAR Practice Tool v" + VERSION
        self.Sig = "rgargente.spt"
        self.Desc = "Set up your plane to practice IFR STAR arrivals procedures"

        self.xplm = XplmWrapper()
        self.cifp = None

        self.spt_window = None
        self.is_translucent = True

        self.debug_file = None
        self.is_debugging_to_file = False

        # Load preferences
        self.LoadPrefs()

        # Debug
        self.init_debugging()

        # Menus
        plugins_menu = XPLMFindPluginsMenu()
        self.spt_menu_index = XPLMAppendMenuItem(plugins_menu, "STAR Practice Tool", 0, 1)
        self.menu_handler_cb = self.menu_handler  # For some reason this silly thing is needed (see PythonInterface_SDKGuide.pdf)
        self.main_menu = XPLMCreateMenu(self, "SPT", plugins_menu, self.spt_menu_index, self.menu_handler_cb, 0)
        XPLMAppendMenuItem(self.main_menu, "Show SPT panel", SHOW_SPT_PANEL_MENUITEMREF, 1)

        # Done with start, return identity
        return self.Name, self.Sig, self.Desc

    def destroy_window(self):
        if self.spt_window:
            XPDestroyWidget(self, self.spt_window, 1)

    def XPluginStop(self):
        self.destroy_window()
        if self.debug_file is not None:
            self.debug_file.close()

        XPLMDestroyMenu(self, self.main_menu)
        XPLMRemoveMenuItem(XPLMFindPluginsMenu(), self.spt_menu_index)

    def XPluginEnable(self):
        return 1

    def XPluginDisable(self):
        pass

    def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
        pass

    def debug_print(self, Msg):
        message = str(datetime.now()) + " " + self.Name + ": " + Msg
        # SandyBarbourPrint(Msg)
        print message
        if self.is_debugging_to_file and self.debug_file:
            self.debug_file.write(message + os.linesep)
            self.debug_file.flush()

    def init_debugging(self):
        log_path = os.path.join(XPLMGetSystemPath(), "Resources", "plugins", "PythonScripts", FILE_LOG)
        try:
            self.debug_file = open(log_path, 'w')
            self.is_debugging_to_file = True
        except:
            self.debug_print("Failed to open debug log file, forcing debug to console.")
            self.debug_print("-> {}".format(log_path))

    def menu_handler(self, menu_ref, item_ref):
        if item_ref == SHOW_SPT_PANEL_MENUITEMREF:
            if not self.spt_window:
                self.create_window()
            else:
                if not XPIsWidgetVisible(self.spt_window):
                    XPShowWidget(self.spt_window)
        else:
            self.debug_print("Unknown menu option " + str(item_ref))

    def create_window(self):
        self.destroy_window()

        screen_w, screen_h = [], []
        XPLMGetScreenSize(screen_w, screen_h)
        left_window = int(screen_w[0]) - WINDOW_W - MARGIN_W
        top_window = int(screen_h[0]) - MARGIN_H
        right_window = left_window + WINDOW_W
        bottom_window = top_window - WINDOW_H

        # Create the Main Widget window
        # XPCreateWidget(inLeft, inTop, inRight, inBottom,
        #                inVisible, inDescriptor, inIsRoot,
        #                XPWidgetID inContainer, XPWidgetClass inClass);
        self.spt_window = XPCreateWidget(left_window, top_window, right_window, bottom_window,
                                         1, self.Name, 1, 0, xpWidgetClass_MainWindow)
        XPSetWidgetProperty(self.spt_window, xpProperty_MainWindowHasCloseBoxes, 1)

        row_h = 20
        padding = 5

        left_col_1 = left_window + padding
        right_col_1 = left_col_1 + 50
        left_col_2 = right_col_1 + padding
        right_col_2 = left_col_2 + 50
        left_col_3 = right_col_2 + padding
        right_col_3 = left_col_3 + 50

        # Airport ICAO
        top_row = top_window - 22
        self.icao_caption = XPCreateWidget(left_col_1, top_row, left_col_1 + 50, top_row - row_h,
                                           1, "Airport ICAO", 0, self.spt_window, xpWidgetClass_Caption)
        top_row -= row_h
        self.icao_tf = XPCreateWidget(left_col_1, top_row, right_col_1, top_row - row_h,
                                      1, "", 0, self.spt_window, xpWidgetClass_TextField)
        self.search_airpot_btn = XPCreateWidget(left_col_2, top_row, right_col_2, top_row - row_h,
                                                1, "Search", 0, self.spt_window, xpWidgetClass_Button)
        self.search_airpot_btn = XPCreateWidget(left_col_3, top_row, right_col_3, top_row - row_h,
                                                1, "Nearest", 0, self.spt_window, xpWidgetClass_Button)

        # STAR
        top_row -= row_h
        self.star_caption = XPCreateWidget(left_col_1, top_row, left_col_1 + 50, top_row - row_h,
                                           1, "STAR", 0, self.spt_window, xpWidgetClass_Caption)
        top_row -= row_h
        self.star_tf = XPCreateWidget(left_col_1, top_row, right_col_1, top_row - row_h,
                                      1, "", 0, self.spt_window, xpWidgetClass_TextField)
        self.star_prev_btn = XPCreateWidget(left_col_2, top_row, right_col_2, top_row - row_h,
                                            1, "Prev", 0, self.spt_window, xpWidgetClass_Button)
        self.star_next_btn = XPCreateWidget(left_col_3, top_row, right_col_3, top_row - row_h,
                                            1, "Next", 0, self.spt_window, xpWidgetClass_Button)

        # Message textbox and clear button
        top_row -= row_h + padding
        self.message_caption = XPCreateWidget(left_col_1, top_row, right_window - padding, top_row - row_h,
                                              1, "", 0, self.spt_window, xpWidgetClass_Caption)

        # GO! button
        top_row -= row_h
        self.go_btn = XPCreateWidget(left_col_1, top_row, right_window - padding, top_row - row_h,
                                     1, "GO!", 0, self.spt_window, xpWidgetClass_Button)

        # Register the widget handler
        self.window_handler_cb = self.window_handler
        XPAddWidgetCallback(self, self.spt_window, self.window_handler_cb)

        # Translucent window
        top_row -= row_h
        x_pos = left_window + 210
        self.translucent_button = XPCreateWidget(x_pos, top_row, x_pos + 5, top_row - row_h,
                                                 1, "", 0, self.spt_window, xpWidgetClass_Button)
        self.translucent_caption = XPCreateWidget(x_pos + 15, top_row, right_window, top_row - row_h + 2,
                                                  1, "Translucent window", 0, self.spt_window, xpWidgetClass_Caption)

        XPSetWidgetProperty(self.translucent_button, xpProperty_ButtonType, xpRadioButton)
        XPSetWidgetProperty(self.translucent_button, xpProperty_ButtonBehavior, xpButtonBehaviorCheckBox)
        XPSetWidgetProperty(self.translucent_button, xpProperty_ButtonState, self.is_translucent)

        self.set_translucency()
        self.init_data()

    def set_translucency(self):
        if self.is_translucent:
            XPSetWidgetProperty(self.spt_window, xpProperty_MainWindowType, xpMainWindowStyle_Translucent)
        else:
            XPSetWidgetProperty(self.spt_window, xpProperty_MainWindowType, xpMainWindowStyle_MainWindow)
        XPSetWidgetProperty(self.icao_caption, xpProperty_CaptionLit, self.is_translucent)
        XPSetWidgetProperty(self.star_caption, xpProperty_CaptionLit, self.is_translucent)
        XPSetWidgetProperty(self.message_caption, xpProperty_CaptionLit, self.is_translucent)
        XPSetWidgetProperty(self.translucent_caption, xpProperty_CaptionLit, self.is_translucent)

    def init_data(self):
        self.debug_print("InitData")
        airport_icao, airport_name, airport_lat, airport_lon = self.xplm.get_nearest_airport()
        XPSetWidgetDescriptor(self.icao_tf, airport_icao)
        self.debug_print("{} - {}".format(airport_icao, airport_name))
        self.debug_print("XP Path: {}".format(XPLMGetSystemPath()))
        self.cifp = Cifp(self.xplm, airport_icao, XPLMGetSystemPath())
        XPSetWidgetDescriptor(self.star_tf, list(self.cifp.star_names)[0])
        self.print_selected_star()

    def window_handler(self, message, widget, param1, param2):
        # Close button will only hide window
        if message == xpMessage_CloseButtonPushed:
            if self.spt_window:
                XPHideWidget(self.spt_window)
            return 1

        # Handle all button pushes
        if message == xpMsg_PushButtonPressed:
            if param1 == self.go_btn:
                self.go()
                return 1

        elif message == xpMsg_ButtonStateChanged:
            if param1 == self.translucent_button:
                self.is_translucent = bool(XPGetWidgetProperty(self.translucent_button, xpProperty_ButtonState, None))
                self.set_translucency()
                self.SavePrefs()
                return 1
        return 0

    def print_message(self, text):
        XPSetWidgetDescriptor(self.message_caption, text)

    def print_selected_star(self):
        out_airport_icao = []
        XPGetWidgetDescriptor(self.icao_tf, out_airport_icao, 10)
        out_star_name = []
        XPGetWidgetDescriptor(self.star_tf, out_star_name, 20)
        self.print_message("{} STAR {} selected".format(out_airport_icao[0], out_star_name[0]))

    # TODO Handle this properly
    def SavePrefs(self):
        baseDir = os.path.join(XPLMGetSystemPath(), "Output", "preferences")
        filePre = os.path.join(baseDir, FILE_PRE)
        with open(filePre, "w") as fh:
            fh.write("# Simple Warp preferences" + os.linesep)
            fh.write("Translucent {}".format(self.is_translucent) + os.linesep)

    def LoadPrefs(self):
        self.is_translucent = True
        self.debug_file = None

        baseDir = os.path.join(XPLMGetSystemPath(), "Output", "preferences")
        filePre = os.path.join(baseDir, FILE_PRE)
        try:
            with open(filePre, "rU") as fh:
                lines = fh.read().splitlines()
                self.debug_print("Reading preferences from Output/preferences/{}".format(FILE_PRE))
                for line in lines:
                    fields = line.upper().strip().split()
                    if len(fields) != 2: continue
                    if fields[0] == "TRANSLUCENT" and str(fields[1]) in ['1', 'YES', 'TRUE']:
                        self.is_translucent = True

        except:
            self.debug_print("Caught top level exception in LoadPrefs")
            pass
        self.SavePrefs()

    def go(self):
        star = self.cifp.stars['DGO1T']
        x, y, z = XPLMWorldToLocal(star.init_lat, star.init_lon, 3048)

        drx = XPLMFindDataRef("sim/flightmodel/position/local_x")
        dry = XPLMFindDataRef("sim/flightmodel/position/local_y")
        drz = XPLMFindDataRef("sim/flightmodel/position/local_z")
        XPLMSetDatad(drx, x)
        XPLMSetDatad(dry, y)
        XPLMSetDatad(drz, z)

        # Stop the flight model
        # dr_override = XPLMFindDataRef("sim/operation/override/override_planepath")
        # override_values = [1]
        # XPLMSetDatavi(dr_override, override_values, 0, 1)

        # Set heading
        # dr_heading = XPLMFindDataRef("sim/flightmodel/position/magpsi")
        # XPLMSetDataf(dr_heading, 90)

        # Set q
        q = mathlib.hpr_to_quaternion(90, 0, 0)
        dr_q = XPLMFindDataRef("sim/flightmodel/position/q")
        XPLMSetDatavf(dr_q, q, 0, 4)

        x, y, z = mathlib.heading_and_speed_to_xyz_vector(90, mathlib.knots_to_m_sec(120))
        dr_vx = XPLMFindDataRef("sim/flightmodel/position/local_vx")
        dr_vy = XPLMFindDataRef("sim/flightmodel/position/local_vy")
        dr_vz = XPLMFindDataRef("sim/flightmodel/position/local_vz")
        XPLMSetDataf(dr_vx, x)
        XPLMSetDataf(dr_vy, y)
        XPLMSetDataf(dr_vz, z)

        # # Set speed
        # dr_speed = XPLMFindDataRef("sim/flightmodel/position/indicated_airspeed")
        # XPLMSetDataf(dr_speed, 120)



        # Resume the flight model
        # override_values = [0]
        # XPLMSetDatavi(dr_override, override_values, 0, 1)
