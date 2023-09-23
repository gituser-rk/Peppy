/* Copyright 2019-2023 Peppy Player peppy.player@gmail.com
 
This file is part of Peppy Player.
 
Peppy Player is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
 
Peppy Player is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
 
You should have received a copy of the GNU General Public License
along with Peppy Player. If not, see <http://www.gnu.org/licenses/>.
*/

export const COLOR_WEB_BGR = "rgb(0,38,40)";
export const COLOR_DARK = "rgb(0,70,75)";
export const COLOR_DARK_LIGHT = "rgb(20,90,100)";
export const COLOR_MEDIUM = "rgb(70,140,150)";
export const COLOR_BRIGHT = "rgb(160,190,210)";
export const COLOR_CONTRAST = "rgb(255,190,120)";
export const COLOR_LOGO = "rgb(20,190,160)";
export const COLOR_MUTE = "rgb(242,107,106)";
export const COLOR_WHITE = "rgb(255,255,255)";
export const COLOR_BLACK = "rgb(0,0,0)";

export const COLOR_PANEL = "rgb(180,210,222)";
export const COLOR_SUCCESS = "rgb(30, 140, 30)";
export const COLOR_WARNING = "rgb(220, 120, 0)";
export const COLOR_ERROR = "rgb(200, 20, 30)";
export const COLOR_INFO = "rgb(20, 100, 230)";
export const COLOR_CHIP = "rgb(213,243,255)";
export const COLOR_CHIP_CONTRAST = "rgb(255,210,140)";

const theme = () => ({
  topContainer: {
    display: "flex",
    flexDirection: "row",
    flexWrap: "nowrap",
    alignItems: "stretch",
    alignContent: "stretch",
    justifyContent: "flex-start",
    width: "100vw",
    height: "100vh",
    margin: 0,
    padding: 0,
    overflow: "auto"
  },
  leftContainer: {
    display: "flex",
    flexDirection: "column",
    width: "23rem",
    minWidth: "16rem",
    backgroundColor: COLOR_PANEL,
    borderRight: "1px solid black",
    overflowY: "auto",
    color: COLOR_DARK
  },
  listItemText: {
    whiteSpace: "nowrap",
    paddingLeft: "2rem"
  },
  rightContainer: {
    display: "flex",
    flexDirection: "column",
    alignItems: "space-between",
    alignContent: "space-between",
    justifyContent: "flex-start",
    width: "100%",
    height: "100%",
    overflowY: "auto"
  },
  headerContainer: {
    display: "flex",
    flexDirection: "column",
    width: "100%",
    height: "5rem",
    background: "black",
    borderBottom: "1px solid black"
  },
  headerLanguage: {
    width: "99%",
    height: "2rem"
  },
  headerTabs: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "flex-end",
    background: COLOR_DARK,
    width: "100%",
    height: "3rem",
    color: COLOR_WHITE
  },
  headerSubTabs: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "flex-end",
    background: COLOR_PANEL,
    width: "100%",
    height: "3rem",
    marginTop: "1px",
    color: COLOR_BLACK
  },
  tabSelection: {
    height: "3px",
    background: COLOR_WHITE
  },
  playlistTabSelection: {
    height: "3px",
    background: COLOR_DARK
  },
  footerContainer: {
    alignSelf: "flex-end",
    display: "flex",
    flexDirection: "column",
    width: "100%",
    height: "6.1rem"
  },
  footerProgress: {
    height: "0.2rem",
    width: "100%"
  },
  footerCopyright: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    background: "black",
    width: "100%",
    height: "2rem",
    paddingBottom: "0.1rem",
    color: COLOR_MEDIUM
  },
  footerButtons: {
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "flex-start",
    height: "4rem",
    paddingLeft: "1rem",
    background: COLOR_DARK
  },
  button: {
    marginRight: "1rem",
    color: COLOR_WEB_BGR,
    background: COLOR_PANEL,
  },
  addButton: {
    marginBottom: "1rem",
    color: COLOR_WEB_BGR,
    background: COLOR_PANEL,
    '&:hover': {
      background: COLOR_BRIGHT
    }
  },
  language: {
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "flex-end",
    background: "black",
    height: "1.98rem",
    width: "100%",
    color: "rgb(255,190,120)"
  },
  languageStyle: {
    width: "1rem",
    marginRight: "0.5rem",
    border: "1px solid " + COLOR_CONTRAST
  },
  languageFont: {
    fontSize: "0.8rem"
  },
  select: {
    '&:before': {
      borderColor: "black",
    },
    '&:after': {
      borderColor: "black",
    },
    color: COLOR_CONTRAST
  },
  icon: {
    fill: "rgb(255,190,120)"
  },
  cssLabel: {
    color: COLOR_DARK
  },
  notchedOutline: {
    color: COLOR_DARK,
    borderWidth: '1px',
    borderColor: COLOR_DARK + ' !important'
  },
  floatingLabelFocusStyle: {
    color: COLOR_DARK
  },
  content: {
    display: "flex",
    flexDirection: "column",
    alignItems: "flex-start",
    alignContent: "flex-start",
    justifyContent: "space-between",
    width: "100%",
    height: "100%"
  },
  contentMargin: {
    margin: "2rem"
  },
  notification: {
    display: "flex",
    flexDirection: "column",
    alignItems: "stretch",
    justifyContent: "space-between",
    width: "100%",
    height: "6rem",
    position: "fixed",
    bottom: 0,
    background: "black",
    color: "white"
  },
  notificationMsg: {
    display: "flex",
    alignItems: "center"
  },
  notificationIcon: {
    marginRight: "1rem"
  },
  actionText: {
    display: "flex",
    flexDirection: "row",
    flexWrap: "nowrap",
    alignItems: "center",
    alignContent: "center",
    justifyContent: "center",
    width: "100vw",
    minWidth: "100vw",
    height: "100vh",
    minHeight: "100vh",
    margin: 0,
    padding: 0,
    overflow: "hidden",
    fontSize: "50px",
    color: COLOR_DARK_LIGHT
  },
  success: {
    backgroundColor: COLOR_SUCCESS
  },
  warning: {
    backgroundColor: COLOR_WARNING
  },
  error: {
    backgroundColor: COLOR_ERROR
  },
  info: {
    backgroundColor: COLOR_INFO
  },
  dialogTitle: {
    display: "flex",
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    height: "1.4rem",
    margin: 0
  },
  dialogIcon: {
    marginLeft: "auto",
    margin: 0
  },
  dialogContent: {
    display: "flex",
    height: "5rem",
    alignItems: "center"
  },
  logoContainer: {
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    alignContent: "center",
    justifyContent: "center",
    width: "100%",
    height: "5rem",
    backgroundColor: COLOR_DARK_LIGHT,
    borderBottom: "1px solid black",
    color: COLOR_CONTRAST,
    textShadow: "2px 2px 2px black"
  },
  logoLink: {
    textDecoration: "none",
    color: COLOR_CONTRAST,
    outline: 0
  },
  logoIcon: {
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    alignContent: "center",
    justifyContent: "flex-end",
    width: "35%",
    filter: "drop-shadow(2px 2px 3px rgba(0,0,0,.5))"
  },
  logoText: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    width: "65%",
    marginLeft: "1rem",
    textDecoration: "none",
    color: COLOR_CONTRAST
  },
  logoNameText: {
    display: "flex",
    justifyContent: "flex-start"
  },
  logoEditionText: {
    fontSize: "70%"
  },
  paletteContainer: {
    display: "flex",
    flexDirection: "column"
  },
  paletteRow: {
    display: "flex",
    flexDirection: "row",
    cursor: "pointer"
  },
  sliderContainer: {
    display: "flex",
    flexDirection: "row",
    alignItems: "center"
  },
  sliderText: {
    width: "7rem",
    marginLeft: "1.4rem"
  },
  playersAudioContainer: {
    display: "flex",
    flexDirection: "column"
  },
  playersAudioTextContainer: {
    display: "flex",
    flexDirection: "column"
  },
  colorsContainer: {
    display: "flex",
    flexDirection: "column",
    marginTop: "-2rem"
  },
  colorsHeader: {
    display: "flex",
    alignItems: "center",
    marginBottom: "0.6rem"
  },
  colorsDivider: {
    marginBottom: "1rem"
  },
  colorsPaletteRow: {
    display: "flex",
    flexDirection: "row"
  },
  colorsCurrentPaletteContainer: {
    height: "160px",
    display: "flex",
    flexDirection: "column"
  },
  colorsResetButton: {
    width: "320px",
    height: "40px",
    color: COLOR_CONTRAST,
    backgroundColor: COLOR_DARK_LIGHT,
    marginTop: "0.5rem",
    '&:hover': {
      background: COLOR_DARK
    }
  },
  slidersContainer: {
    display: "flex", 
    flexDirection: "column", 
    justifyContent: "space-between", 
    marginLeft: "1rem"
  },
  colorsPalette: {
    marginLeft: "1.3rem"
  },
  screenExamplesContainer: {
    display: "flex", 
    flexDirection: "row"
  },
  exampleContainer: {
    display: "flex", 
    flexDirection: "column"
  },
  red: {
    backgroundColor: "red"
  },
  green: {
    backgroundColor: "green"
  },
  blue: {
    backgroundColor: "blue"
  }
});

export default theme;
