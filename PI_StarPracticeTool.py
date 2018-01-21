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
        left = int(screen_w[0]) - WINDOW_W - MARGIN_W
        top = int(screen_h[0]) - MARGIN_H

        right = left + WINDOW_W
        bottom = top - WINDOW_H

        # Create the Main Widget window
        # XPCreateWidget(inLeft, inTop, inRight, inBottom,
        #                inVisible, inDescriptor, inIsRoot,
        #                XPWidgetID inContainer, XPWidgetClass inClass);
        self.spt_window = XPCreateWidget(left, top, right, bottom,
                                         1, self.Name, 1, 0, xpWidgetClass_MainWindow)
        XPSetWidgetProperty(self.spt_window, xpProperty_MainWindowHasCloseBoxes, 1)

        row_h, spx, spy = 20, 15, 20
        ww1, ww2, ww3, ww4, ww5, ww6, ww7 = 10, 85, 30, 40, 60, 65, 30

        padding = 5
        left_col_1 = left + padding
        right_col_1 = left_col_1 + 50
        left_col_2 = right_col_1 + padding
        right_col_2 = left_col_2 + 50
        left_col_3 = right_col_2 + padding
        right_col_3 = left_col_3 + 50

        left_col_4 = left + 170
        right_col_4 = left_col_4 + 50
        left_col_5 = right_col_4 + padding
        right_col_5 = left_col_5 + 50
        left_col_6 = right_col_5 + padding
        right_col_6 = left_col_6 + 50

        # xx2 = left_col_1 + ww1 + spx
        # xx3 = xx2 + ww2 + spx
        # xx4 = xx3 + ww3 + spx
        # xx5 = xx4 + ww4 + spx
        # xx6 = xx5 + ww5 + spx

        # Airport ICAO
        top_row = top - 22
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

        top_row -= spy

        # Message textbox and clear button
        self.WarnMsg = XPCreateWidget(left_col_1, top_row, right - 60, top_row - row_h,
                                      1, "Welcome to Simple Warp", 0, self.spt_window, xpWidgetClass_Caption)
        self.BtnWarn = XPCreateWidget(right - 50, top_row, right - 5, top_row - row_h,
                                      1, "Clear", 0, self.spt_window, xpWidgetClass_Button)
        XPSetWidgetProperty(self.BtnWarn, xpProperty_ButtonType, xpPushButton)
        top_row -= spy
        top_row -= int(spy / 2)

        self.WrpFix = XPCreateWidget(left_col_1, top_row, left_col_1 + 40, top_row - row_h, 1, "", 0, self.spt_window,
                                     xpWidgetClass_TextField)
        self.BtnFind = XPCreateWidget(left_col_1 + 45, top_row, left_col_1 + 85, top_row - row_h, 1, "Find", 0,
                                      self.spt_window,
                                      xpWidgetClass_Button)
        self.BtnNext = XPCreateWidget(left_col_1 + 90, top_row, left_col_1 + 130, top_row - row_h, 1, "Next", 0,
                                      self.spt_window,
                                      xpWidgetClass_Button)
        self.WrpLb0 = XPCreateWidget(left_col_1 + 135, top_row, left_col_1 + 250, top_row - row_h, 1,
                                     "Navaid ID (empty for FMS)",
                                     0,
                                     self.spt_window, xpWidgetClass_Caption)
        self.BtnWarp = XPCreateWidget(right - 50, top_row, right - 5, top_row - row_h, 1, "!Warp!", 0,
                                      self.spt_window,
                                      xpWidgetClass_Button)
        XPSetWidgetProperty(self.BtnFind, xpProperty_ButtonType, xpPushButton)
        XPSetWidgetProperty(self.BtnNext, xpProperty_ButtonType, xpPushButton)
        XPSetWidgetProperty(self.BtnWarp, xpProperty_ButtonType, xpPushButton)
        top_row -= spy

        self.WrpDst = XPCreateWidget(left_col_1, top_row, left_col_1 + 40, top_row - row_h, 1, "", 0, self.spt_window,
                                     xpWidgetClass_TextField)
        self.WrpLb1 = XPCreateWidget(left_col_1 + 45, top_row, left_col_1 + 250, top_row - row_h, 1,
                                     "Warp as close as ... (min=1nm, default=10nm)", 0, self.spt_window,
                                     xpWidgetClass_Caption)
        XPSetWidgetDescriptor(self.WrpDst, str(self.warp_Dst))

        top_row -= spy
        self.Pref1Btn = XPCreateWidget(left_col_1 + 30, top_row, left_col_1 + 40, top_row - row_h, 1, "", 0,
                                       self.spt_window,
                                       xpWidgetClass_Button)
        self.Pref1Lbl = XPCreateWidget(left_col_1 + 45, top_row, left_col_1 + 250, top_row - row_h, 1,
                                       "Translucent window", 0,
                                       self.spt_window,
                                       xpWidgetClass_Caption)
        XPSetWidgetProperty(self.Pref1Btn, xpProperty_ButtonType, xpRadioButton)
        XPSetWidgetProperty(self.Pref1Btn, xpProperty_ButtonBehavior, xpButtonBehaviorCheckBox)
        XPSetWidgetProperty(self.Pref1Btn, xpProperty_ButtonState, self.Translucent)
        XPSetWidgetProperty(self.Pref1Btn, xpProperty_Enabled, 1)

        top_row -= spy
        self.go_btn = XPCreateWidget(left_col_1, top_row, right - padding, top_row - row_h,
                                     1, "GO!", 0, self.spt_window, xpWidgetClass_Button)

        # Register the widget handler
        self.SWWindowHandlerCB = self.SWWindowHandler
        XPAddWidgetCallback(self, self.spt_window, self.SWWindowHandlerCB)
        self.SetTranslucency()

        self.init_data()

    def init_data(self):
        self.debug_print("InitData")
        airport_icao, airport_name, airport_lat, airport_lon = self.xplm.get_nearest_airport()
        XPSetWidgetDescriptor(self.icao_tf, airport_icao)
        self.debug_print("{} - {}".format(airport_icao, airport_name))
        self.debug_print("XP Path: {}".format(XPLMGetSystemPath()))
        self.cifp = Cifp(self.xplm, airport_icao, XPLMGetSystemPath())
        XPSetWidgetDescriptor(self.star_tf, list(self.cifp.star_names)[0])

    def SWWindowHandler(self, inMessage, inWidget, inParam1, inParam2):
        # Close button will only hide window
        if inMessage == xpMessage_CloseButtonPushed:
            if self.spt_window:
                XPHideWidget(self.spt_window)
            return 1

        # Handle all button pushes
        if inMessage == xpMsg_PushButtonPressed:
            if inParam1 == self.BtnWarp:
                self.WarpAircraft()
                return 1
            if inParam1 == self.BtnWarn:
                self.CmdClearWarning()
                return 1
            if inParam1 == self.BtnFind:
                self.CmdFindAid()
                return 1
            if inParam1 == self.BtnNext:
                self.CmdNextAid()
                return 1
            if inParam1 == self.go_btn:
                self.go()
                return 1

        elif inMessage == xpMsg_ButtonStateChanged:
            if inParam1 == self.Pref1Btn:
                self.Translucent = bool(XPGetWidgetProperty(self.Pref1Btn, xpProperty_ButtonState, None))
                self.SetTranslucency()
                self.SavePrefs()
                return 1
        return 0

    def SetTranslucency(self):
        if self.Translucent:
            XPSetWidgetProperty(self.spt_window, xpProperty_MainWindowType, xpMainWindowStyle_Translucent)
        else:
            XPSetWidgetProperty(self.spt_window, xpProperty_MainWindowType, xpMainWindowStyle_MainWindow)

        XPSetWidgetProperty(self.icao_caption, xpProperty_CaptionLit, self.Translucent)
        XPSetWidgetProperty(self.star_caption, xpProperty_CaptionLit, self.Translucent)
        XPSetWidgetProperty(self.WarnMsg, xpProperty_CaptionLit, self.Translucent)
        XPSetWidgetProperty(self.Pref1Lbl, xpProperty_CaptionLit, self.Translucent)
        XPSetWidgetProperty(self.WrpLb0, xpProperty_CaptionLit, self.Translucent)
        XPSetWidgetProperty(self.WrpLb1, xpProperty_CaptionLit, self.Translucent)

    def CmdClearWarning(self):
        XPSetWidgetDescriptor(self.WarnMsg, " ")
        XPSetWidgetProperty(self.BtnWarn, xpProperty_Enabled, 0)
        XPSetWidgetDescriptor(self.WrpFix, "")
        self.findAid = 0
        self.foundAid = False

    def CmdDisplayWarning(self, text):
        XPSetWidgetDescriptor(self.WarnMsg, text)
        XPSetWidgetProperty(self.BtnWarn, xpProperty_Enabled, 1)

    def SavePrefs(self):
        baseDir = os.path.join(XPLMGetSystemPath(), "Output", "preferences")
        filePre = os.path.join(baseDir, FILE_PRE)
        with open(filePre, "w") as fh:
            fh.write("# Simple Warp preferences" + os.linesep)
            fh.write("Translucent {}".format(self.Translucent) + os.linesep)
            fh.write("Warp_Dst {}".format(self.warp_Dst) + os.linesep)

    def LoadPrefs(self):
        self.Translucent = True
        self.debug_file = None
        self.warp_Dst = 10
        # self.warp_Alt = 200
        # self.warp_Spd = 200

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
                        self.Translucent = True
                    if fields[0] == "WARP_DST":
                        try:
                            self.warp_Dst = int(fields[1])
                        except:
                            pass

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
