#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
X Plane STAR Practice Tool Python plugin
Copyright (C) 2018 Rafael Garcia Argente
https://github.com/rgargente/XPlaneStarPracticeTool

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import json
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

import starpracticetool_lib.version as version
import starpracticetool_lib.mathlib as mathlib
from starpracticetool_lib.cifplib import Cifp
from starpracticetool_lib.xplm_wrapper import XplmWrapper

FILE_LOG = "STAR_Practice_Tool.log"

SHOW_SPT_PANEL_MENUITEMREF = 1

MARGIN_W = 30
MARGIN_H = 30
WINDOW_W = 350
WINDOW_H = 190


# noinspection PyUnresolvedReferences
class PythonInterface:
    def XPluginStart(self):
        self.Name = "STAR Practice Tool v" + version.VERSION
        self.Sig = "rgargente.spt"
        self.Desc = "Set up your plane to practice IFR STAR arrivals procedures"

        self.xplm_wrapper = XplmWrapper()
        self.cifp = None

        self.spt_window = None

        self.fm_overriden = False

        self.debug_file = None
        self.is_debugging_to_file = False

        # Load preferences
        self.preferences = Preferences.load()

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

        if self.main_menu:
            XPLMDestroyMenu(self, self.main_menu)
        XPLMRemoveMenuItem(XPLMFindPluginsMenu(), self.spt_menu_index)

    def XPluginEnable(self):
        return 1

    def XPluginDisable(self):
        pass

    def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
        pass

    def save_prefs(self):
        self.preferences.speed = self.selected_speed
        self.preferences.save()

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

        left_half_window = left_window + WINDOW_W / 2

        # Airport ICAO
        top_row = top_window - 22
        self.icao_caption = XPCreateWidget(left_col_1, top_row, left_col_1 + 50, top_row - row_h,
                                           1, "Airport ICAO", 0, self.spt_window, xpWidgetClass_Caption)
        top_row -= row_h
        self.airport_icao_tf = XPCreateWidget(left_col_1, top_row, right_col_1, top_row - row_h,
                                              1, "", 0, self.spt_window, xpWidgetClass_TextField)
        self.search_airpot_btn = XPCreateWidget(left_col_2, top_row, right_col_2, top_row - row_h,
                                                1, "Search", 0, self.spt_window, xpWidgetClass_Button)
        self.nearest_airpot_btn = XPCreateWidget(left_col_3, top_row, right_col_3, top_row - row_h,
                                                 1, "Nearest", 0, self.spt_window, xpWidgetClass_Button)

        # STAR
        top_row -= row_h
        self.star_caption = XPCreateWidget(left_col_1, top_row, left_col_1 + 50, top_row - row_h,
                                           1, "STAR", 0, self.spt_window, xpWidgetClass_Caption)
        top_row -= row_h
        self.star_tf = XPCreateWidget(left_col_1, top_row, right_col_1, top_row - row_h,
                                      1, "", 0, self.spt_window, xpWidgetClass_TextField)
        XPSetWidgetProperty(self.star_tf, xpProperty_Enabled, 0)
        self.star_prev_btn = XPCreateWidget(left_col_2, top_row, right_col_2, top_row - row_h,
                                            1, "Prev", 0, self.spt_window, xpWidgetClass_Button)
        self.star_next_btn = XPCreateWidget(left_col_3, top_row, right_col_3, top_row - row_h,
                                            1, "Next", 0, self.spt_window, xpWidgetClass_Button)

        self.init_heading_caption = XPCreateWidget(left_half_window, top_row, left_half_window + 50, top_row - row_h,
                                                   1, "", 0, self.spt_window, xpWidgetClass_Caption)

        # Altitude and Speed
        top_row -= row_h
        self.altitude_caption = XPCreateWidget(left_col_1, top_row, right_col_1, top_row - row_h,
                                               1, "Altitude", 0, self.spt_window, xpWidgetClass_Caption)
        self.altitude_tf = XPCreateWidget(left_col_2, top_row, right_col_2, top_row - row_h,
                                          1, "10000", 0, self.spt_window, xpWidgetClass_TextField)
        self.altitude_units_caption = XPCreateWidget(right_col_2 + padding, top_row, right_col_2 + 20, top_row - row_h,
                                                     1, "ft", 0, self.spt_window, xpWidgetClass_Caption)
        right = left_half_window + 40
        self.speed_caption = XPCreateWidget(left_half_window, top_row, right, top_row - row_h,
                                            1, "Speed", 0, self.spt_window, xpWidgetClass_Caption)
        left = right + 2 * padding
        right = left + 40
        self.speed_tf = XPCreateWidget(left, top_row, right, top_row - row_h,
                                       1, str(self.preferences.speed), 0, self.spt_window, xpWidgetClass_TextField)
        self.speed_units_caption = XPCreateWidget(right + padding, top_row, right + 20, top_row - row_h,
                                                  1, "kts", 0, self.spt_window, xpWidgetClass_Caption)

        # Message textbox and clear button
        top_row -= row_h + padding
        self.message_caption = XPCreateWidget(left_col_1, top_row, right_window - padding, top_row - row_h,
                                              1, "", 0, self.spt_window, xpWidgetClass_Caption)

        # GO! button
        top_row -= row_h
        self.go_btn = XPCreateWidget(left_col_1, top_row, right_window - padding, top_row - row_h,
                                     1, "GO!", 0, self.spt_window, xpWidgetClass_Button)

        # Update caption
        top_row -= row_h
        self.update_caption = None
        if not version.is_up_to_date():
            self.update_caption = XPCreateWidget(left_col_1, top_row, right_col_2, top_row - row_h + 2,
                                                 1, "NEW PLUGIN VERSION AVAILABLE!", 0, self.spt_window,
                                                 xpWidgetClass_Caption)

        # Translucent window
        x_pos = left_window + 210
        self.translucent_button = XPCreateWidget(x_pos, top_row, x_pos + 15, top_row - row_h,
                                                 1, "", 0, self.spt_window, xpWidgetClass_Button)
        self.translucent_caption = XPCreateWidget(x_pos + 15, top_row, right_window, top_row - row_h + 2,
                                                  1, "Translucent window", 0, self.spt_window, xpWidgetClass_Caption)

        XPSetWidgetProperty(self.translucent_button, xpProperty_ButtonType, xpRadioButton)
        XPSetWidgetProperty(self.translucent_button, xpProperty_ButtonBehavior, xpButtonBehaviorCheckBox)
        XPSetWidgetProperty(self.translucent_button, xpProperty_ButtonState, self.preferences.is_translucent)

        self.set_translucency()

        # Register the widget handler
        self.window_handler_cb = self.window_handler
        XPAddWidgetCallback(self, self.spt_window, self.window_handler_cb)

        self.init_data()

    def set_translucency(self):
        if self.preferences.is_translucent:
            XPSetWidgetProperty(self.spt_window, xpProperty_MainWindowType, xpMainWindowStyle_Translucent)
        else:
            XPSetWidgetProperty(self.spt_window, xpProperty_MainWindowType, xpMainWindowStyle_MainWindow)
        XPSetWidgetProperty(self.icao_caption, xpProperty_CaptionLit, self.preferences.is_translucent)
        XPSetWidgetProperty(self.star_caption, xpProperty_CaptionLit, self.preferences.is_translucent)
        XPSetWidgetProperty(self.init_heading_caption, xpProperty_CaptionLit, self.preferences.is_translucent)
        XPSetWidgetProperty(self.altitude_caption, xpProperty_CaptionLit, self.preferences.is_translucent)
        XPSetWidgetProperty(self.altitude_units_caption, xpProperty_CaptionLit, self.preferences.is_translucent)
        XPSetWidgetProperty(self.speed_caption, xpProperty_CaptionLit, self.preferences.is_translucent)
        XPSetWidgetProperty(self.speed_units_caption, xpProperty_CaptionLit, self.preferences.is_translucent)
        XPSetWidgetProperty(self.message_caption, xpProperty_CaptionLit, self.preferences.is_translucent)
        XPSetWidgetProperty(self.translucent_caption, xpProperty_CaptionLit, self.preferences.is_translucent)
        if self.update_caption:
            XPSetWidgetProperty(self.update_caption, xpProperty_CaptionLit, self.preferences.is_translucent)

    @property
    def selected_airport_icao(self):
        out_airport_icao = []
        XPGetWidgetDescriptor(self.airport_icao_tf, out_airport_icao, 10)
        return out_airport_icao[0]

    @property
    def selected_star_name(self):
        out_star_name = []
        XPGetWidgetDescriptor(self.star_tf, out_star_name, 20)
        return out_star_name[0]

    @property
    def selected_star(self):
        return self.cifp.stars[self.selected_star_name]

    @property
    def selected_altitude(self):
        out_alt = []
        XPGetWidgetDescriptor(self.altitude_tf, out_alt, 5)
        return int(out_alt[0])

    @property
    def selected_speed(self):
        out_speed = []
        XPGetWidgetDescriptor(self.speed_tf, out_speed, 5)
        return int(out_speed[0])

    def set_go_button_enabled(self, enabled=True):
        XPSetWidgetProperty(self.go_btn, xpProperty_Enabled, enabled)
        XPSetWidgetProperty(self.star_prev_btn, xpProperty_Enabled, enabled)
        XPSetWidgetProperty(self.star_next_btn, xpProperty_Enabled, enabled)
        if not enabled:
            XPSetWidgetDescriptor(self.star_tf, "")

    def window_handler(self, message, widget, param1, param2):
        # Close button will only hide window
        if message == xpMessage_CloseButtonPushed:
            if self.spt_window:
                self.save_prefs()
                XPHideWidget(self.spt_window)
            return 1

        # Handle all button pushes
        if message == xpMsg_PushButtonPressed:
            if param1 == self.search_airpot_btn:
                self.search_airport(self.selected_airport_icao)
            elif param1 == self.nearest_airpot_btn:
                self.init_data()
            elif param1 == self.star_prev_btn:
                XPSetWidgetDescriptor(self.star_tf, self.cifp.get_prev_star(self.selected_star_name))
                self.print_selected_star()
            elif param1 == self.star_next_btn:
                XPSetWidgetDescriptor(self.star_tf, self.cifp.get_next_star(self.selected_star_name))
                self.print_selected_star()
            elif param1 == self.go_btn:
                self.go()
                return 1

        elif message == xpMsg_ButtonStateChanged:
            if param1 == self.translucent_button:
                self.preferences.is_translucent = bool(
                    XPGetWidgetProperty(self.translucent_button, xpProperty_ButtonState, None))
                self.set_translucency()
                self.save_prefs()
                return 1
        return 0

    def print_message(self, text):
        XPSetWidgetDescriptor(self.message_caption, text)

    def print_selected_star(self):
        heading = self.selected_star.init_heading
        if heading < 0:
            heading += 360
        XPSetWidgetDescriptor(self.init_heading_caption, "Initial heading {:.0f}°".format(heading))
        self.print_message("{} STAR {} selected".format(self.selected_airport_icao, self.selected_star_name))

    def init_data(self):
        airport_icao, airport_name, airport_lat, airport_lon = self.xplm_wrapper.get_nearest_airport()
        self.load_new_airport(airport_icao)

    def load_new_airport(self, airport_icao):
        XPSetWidgetDescriptor(self.airport_icao_tf, airport_icao)
        try:
            self.cifp = Cifp(self.xplm_wrapper, airport_icao, XPLMGetSystemPath())
            if self.cifp.star_names:
                XPSetWidgetDescriptor(self.star_tf, self.cifp.star_names[0])
                self.print_selected_star()
                self.set_go_button_enabled(True)
            else:
                self.print_message("No STARs found for {} airport".format(airport_icao))
                self.set_go_button_enabled(False)
        except Exception as e:
            self.print_message(str(e))
            self.set_go_button_enabled(False)

    def search_airport(self, airport_icao):
        try:
            airport_icao = airport_icao.upper()
            XPSetWidgetDescriptor(self.airport_icao_tf, airport_icao)
            self.load_new_airport(airport_icao)
        except Exception as e:
            self.print_message(str(e))
            self.set_go_button_enabled(False)

    def go(self):
        dr_override = XPLMFindDataRef("sim/operation/override/override_planepath")
        override_values = [1]
        star = self.selected_star

        if not self.fm_overriden:
            self.save_prefs()

            x, y, z = XPLMWorldToLocal(star.init_lat, star.init_lon, mathlib.feet_to_meters(self.selected_altitude))
            drx = XPLMFindDataRef("sim/flightmodel/position/local_x")
            dry = XPLMFindDataRef("sim/flightmodel/position/local_y")
            drz = XPLMFindDataRef("sim/flightmodel/position/local_z")
            XPLMSetDatad(drx, x)
            XPLMSetDatad(dry, y)
            XPLMSetDatad(drz, z)

            # Stop the flight model
            XPLMSetDatavi(dr_override, override_values, 0, 1)
            self.fm_overriden = True
            self.print_message("Set up your autopilot, gear, etc. and click GO again.")

        else:
            # All these values must be set after the "teleporting" to avoid unpredictable behaviour.
            # There can be a significant delay loading the scenery, but the script won't wait for it.

            # Set quaternion
            q = mathlib.hpr_to_quaternion(star.init_heading, 0, 0)
            dr_q = XPLMFindDataRef("sim/flightmodel/position/q")
            XPLMSetDatavf(dr_q, q, 0, 4)

            # Set velocity
            tas = mathlib.tas_to_ias(self.selected_speed, self.selected_altitude)
            vx, vy, vz = mathlib.heading_and_speed_to_xyz_vector(star.init_heading,
                                                                 mathlib.knots_to_m_sec(tas))
            dr_vx = XPLMFindDataRef("sim/flightmodel/position/local_vx")
            dr_vy = XPLMFindDataRef("sim/flightmodel/position/local_vy")
            dr_vz = XPLMFindDataRef("sim/flightmodel/position/local_vz")
            XPLMSetDataf(dr_vx, vx)
            XPLMSetDataf(dr_vy, vy)
            XPLMSetDataf(dr_vz, vz)

            # Set rotation to 0
            dr_p = XPLMFindDataRef("sim/flightmodel/position/P")
            dr_q = XPLMFindDataRef("sim/flightmodel/position/Q")
            dr_r = XPLMFindDataRef("sim/flightmodel/position/R")
            XPLMSetDataf(dr_p, 0)
            XPLMSetDataf(dr_q, 0)
            XPLMSetDataf(dr_r, 0)

            # Resume the flight model
            override_values = [0]
            XPLMSetDatavi(dr_override, override_values, 0, 1)
            self.fm_overriden = False
            self.print_selected_star()


class Preferences:
    file_path = os.path.join(XPLMGetSystemPath(), "Output", "preferences", "STAR_Practice_Tool.json")

    def __init__(self):
        self.is_translucent = True
        self.speed = 200

    def save(self):
        with open(Preferences.file_path, 'w') as f:
            json.dump(self.__dict__, f)

    @staticmethod
    def load():
        p = Preferences()
        if os.path.exists(Preferences.file_path):
            with open(Preferences.file_path, 'r') as f:
                j = json.load(f)
                p.is_translucent = j['is_translucent']
                p.speed = j['speed']
        return p
