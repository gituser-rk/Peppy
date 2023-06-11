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

import React from "react";
import Display from "../config/Display";
import Usage from "../config/Usage";
import Logging from "../config/Logging";
import FileBrowser from "../config/FileBrowser";
import WebServer from "../config/WebServer";
import StreamServer from "../config/StreamServer";
import Podcasts from "../config/Podcasts";
import HomeMenu from "../config/HomeMenu";
import HomeNavigator from "../config/HomeNavigator";
import ScreensaverMenu from "../config/ScreensaverMenu";
import ScreensaverDelay from "../config/ScreensaverDelay";
import LanguagesMenu from "../config/LanguagesMenu";
import Collection from "../config/Collection";
import CollectionMenu from "../config/CollectionMenu";
import DiskMount from "../config/DiskMount";
import Colors from "../config/Colors";
import Icons from "../config/Icons";
import Background from "../config/Background";
import Font from "../config/Font";
import VolumeControl from "../config/VolumeControl";
import PlayerScreen from "../config/PlayerScreen";
import DisplayBacklight from "../config/DisplayBacklight";
import Scripts from "../config/Scripts";
import Gpio from "../config/Gpio";
import I2C from "../config/I2C";

export const configSections = [
  "screen.info", "usage", "logging", "file.browser", "web.server", "stream.server", "podcasts", "home.menu",
  "home.navigator", "screensaver.menu", "screensaver.delay", "languages.menu", "collection", "collection.menu", "disk.mount", 
  "colors", "icons", "background", "font", "volume.control", "player.screen", "display.backlight", "scripts", "gpio", "i2c"
];

export default class ConfigTab extends React.Component {
  render() {
    const { params, classes, topic, updateState, labels, background, fonts, languages, language, uploadFont } = this.props;
    let p = params[configSections[topic]];

    return (
      <main className={classes.content}>
        <div className={classes.toolbar} />
        {topic === 0 && <Display params={p} labels={labels} classes={classes} updateState={updateState} />}
        {topic === 1 && <Usage params={p} labels={labels} classes={classes} updateState={updateState} />}
        {topic === 2 && <Logging params={p} labels={labels} classes={classes} updateState={updateState} />}
        {topic === 3 && <FileBrowser params={p} labels={labels} classes={classes} updateState={updateState} />}
        {topic === 4 && <WebServer params={p} labels={labels} classes={classes} updateState={updateState} />}
        {topic === 5 && <StreamServer params={p} labels={labels} classes={classes} updateState={updateState} />}
        {topic === 6 && <Podcasts params={p} labels={labels} classes={classes} updateState={updateState} />}
        {topic === 7 && <HomeMenu params={p} labels={labels} classes={classes} updateState={updateState} />}
        {topic === 8 && <HomeNavigator params={p} labels={labels} classes={classes} updateState={updateState} />}
        {topic === 9 && <ScreensaverMenu params={p} labels={labels} classes={classes} updateState={updateState} />}
        {topic === 10 && <ScreensaverDelay params={p} labels={labels} classes={classes} updateState={updateState} />}
        {topic === 11 && <LanguagesMenu params={p} labels={labels} classes={classes} updateState={updateState} languages={languages} language={language} />}
        {topic === 12 && <Collection params={p} labels={labels} classes={classes} updateState={updateState} />}
        {topic === 13 && <CollectionMenu params={p} labels={labels} classes={classes} updateState={updateState} />}
        {topic === 14 && <DiskMount params={p} labels={labels} classes={classes} updateState={updateState} />}
        {topic === 15 && <Colors params={p} labels={labels} reset={this.props.reset} classes={classes}
          updateState={updateState} setPalette={this.props.setPalette} setColor={this.props.setColor} />}
        {topic === 16 && <Icons params={p} labels={labels} classes={classes} updateState={updateState} />}
        {topic === 17 && <Background params={background} labels={labels} classes={classes} updateState={updateState} />}
        {topic === 18 && <Font params={p} labels={labels} classes={classes} updateState={updateState} fonts={fonts} uploadFont={uploadFont} />}
        {topic === 19 && <VolumeControl params={p} labels={labels} classes={classes} updateState={updateState} />}
        {topic === 20 && <PlayerScreen params={p} labels={labels} classes={classes} updateState={updateState} />}
        {topic === 21 && <DisplayBacklight params={p} labels={labels} classes={classes} updateState={updateState} />}
        {topic === 22 && <Scripts params={p} labels={labels} classes={classes} updateState={updateState} />}
        {topic === 23 && <Gpio params={p} labels={labels} classes={classes} updateState={updateState} />}
        {topic === 24 && <I2C params={p} labels={labels} classes={classes} updateState={updateState} />}
      </main>
    );
  }
}
