/*
 * Copyright 2013 Heena Mahour <heena393@gmail.com>
 * Copyright 2013 Sebastian Kügler <sebas@kde.org>
 * Copyright 2013 Martin Klapetek <mklapetek@kde.org>
 * Copyright 2014 David Edmundson <davidedmundson@kde.org>
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 2 of
 * the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

import QtQuick 2.6
import QtQuick.Layouts 1.1
import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.plasma.components 2.0 as Components
import org.kde.plasma.private.digitalclock 1.0

Item {
    id: main

    property string timeFormat
    property date currentTime

    property bool showSeconds: plasmoid.configuration.showSeconds
    property bool showDate: plasmoid.configuration.showDate
    property int dateFormat: {
        if (plasmoid.configuration.dateFormat === "longDate") {
            return  Qt.SystemLocaleLongDate;
        } else if (plasmoid.configuration.dateFormat === "isoDate") {
            return Qt.ISODate;
        }

        return Qt.SystemLocaleShortDate;
    }

    property int use24hFormat: plasmoid.configuration.use24hFormat

    property string lastDate: ""




    onDateFormatChanged: {
        setupLabels();
    }

    onStateChanged: { setupLabels(); }


    onShowSecondsChanged:          { timeFormatCorrection(Qt.locale().timeFormat(Locale.ShortFormat)) }

    onShowDateChanged:             { timeFormatCorrection(Qt.locale().timeFormat(Locale.ShortFormat)) }
    onUse24hFormatChanged:         { timeFormatCorrection(Qt.locale().timeFormat(Locale.ShortFormat)) }



    states: [

        State {
            name: "other"
            when: plasmoid.formFactor != PlasmaCore.Types.Vertical && plasmoid.formFactor != PlasmaCore.Types.Horizontal

            PropertyChanges {
                target: main
                Layout.fillHeight: false
                Layout.fillWidth: false
                Layout.minimumWidth: units.gridUnit * 3
                Layout.minimumHeight: units.gridUnit * 3
            }

            PropertyChanges {
                target: contentItem

                height: main.height
                width: main.width
            }

            PropertyChanges {
                target: labelsGrid

                rows: 2
            }

            PropertyChanges {
                target: timeLabel

                height: sizehelper.height
                width: main.width

                fontSizeMode: Text.Fit
            }

            PropertyChanges {
                target: timezoneLabel

                height: 0.7 * timeLabel.height
                width: main.width

                fontSizeMode: Text.Fit
                minimumPixelSize: 1
            }

            PropertyChanges {
                target: dateLabel

                height: 0.8 * timeLabel.height
                width: Math.max(timeLabel.contentWidth, units.gridUnit * 3)

                fontSizeMode: Text.Fit
                minimumPixelSize: 1
            }

            AnchorChanges {
                target: dateLabel

                anchors.top: labelsGrid.bottom
                anchors.horizontalCenter: labelsGrid.horizontalCenter
            }

            PropertyChanges {
                target: sizehelper

                height: {
                    if (main.showDate) {
                        if (timezoneLabel.visible) {
                            return 0.4 * main.height
                        }
                        return 0.56 * main.height
                    } else if (timezoneLabel.visible) {
                        return 0.59 * main.height
                    }
                    return main.height
                }
                width: main.width

                fontSizeMode: Text.Fit
                font.pixelSize: 1024
            }
        }
    ]

  

   /*
    * Visible elements
    *
    */
    Item {
        id: contentItem
        anchors.verticalCenter: main.verticalCenter

        Grid {
            id: labelsGrid

            rows: 1
            horizontalItemAlignment: Grid.AlignHCenter
            verticalItemAlignment: Grid.AlignVCenter

            flow: Grid.TopToBottom
            columnSpacing: units.smallSpacing

            Rectangle {
                height: 0.8 * sizehelper.height
                width: 1
                visible: main.showDate && main.oneLineMode

                color: theme.textColor
                opacity: 0.4
            }

            Components.Label  {
                id: timeLabel

                font {
                    family: plasmoid.configuration.fontFamily || theme.defaultFont.family
                    weight: plasmoid.configuration.boldText ? Font.Bold : theme.defaultFont.weight
                    italic: plasmoid.configuration.italicText
                    pixelSize: 1024
                }
                minimumPixelSize: 1

                text: {

                    main.currentTime = new Date(dataSource.data["Local"]["DateTime"].getTime());
                    return Qt.formatTime(currentTime, main.timeFormat);
                }

                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
            }

            Components.Label {
                id: timezoneLabel

                font.weight: timeLabel.font.weight
                font.italic: timeLabel.font.italic
                font.pixelSize: 1024
                minimumPixelSize: 1

                visible: text.length > 0
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }

        Components.Label {
            id: dateLabel

            visible: main.showDate

            font.family: timeLabel.font.family
            font.weight: timeLabel.font.weight
            font.italic: timeLabel.font.italic
            font.pixelSize: 1024
            minimumPixelSize: 1

            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }
    /*
     * end: Visible Elements
     *
     */

    Components.Label {
        id: sizehelper

        font.family: timeLabel.font.family
        font.weight: timeLabel.font.weight
        font.italic: timeLabel.font.italic
        minimumPixelSize: 1

        visible: false
    }


    // Qt's QLocale does not offer any modular time creating like Klocale did
    // eg. no "gimme time with seconds" or "gimme time without seconds and with timezone".
    // QLocale supports only two formats - Long and Short. Long is unusable in many situations
    // and Short does not provide seconds. So if seconds are enabled, we need to add it here.
    //
    // What happens here is that it looks for the delimiter between "h" and "m", takes it
    // and appends it after "mm" and then appends "ss" for the seconds.
    function timeFormatCorrection(timeFormatString) {
        var regexp = /(hh*)(.+)(mm)/i
        var match = regexp.exec(timeFormatString);

        var hours = match[1];
        var delimiter = match[2];
        var minutes = match[3]
        var seconds = "ss";
        var amPm = "AP";
        var uses24hFormatByDefault = timeFormatString.toLowerCase().indexOf("ap") == -1;

        // because QLocale is incredibly stupid and does not convert 12h/24h clock format
        // when uppercase H is used for hours, needs to be h or hh, so toLowerCase()
        var result = hours.toLowerCase() + delimiter + minutes;

        if (main.showSeconds) {
            result += delimiter + seconds;
        }

        // add "AM/PM" either if the setting is the default and locale uses it OR if the user unchecked "use 24h format"
        if ((main.use24hFormat == Qt.PartiallyChecked && !uses24hFormatByDefault) || main.use24hFormat == Qt.Unchecked) {
            result += " " + amPm;
        }

        main.timeFormat = result;
        setupLabels();
    }

    function setupLabels() {
        




        if (main.showDate) {
            dateLabel.text = Qt.formatDate(main.currentTime, main.dateFormat);
        } else {
            // clear it so it doesn't take space in the layout
            dateLabel.text = "";
        }

        // find widest character between 0 and 9
        var maximumWidthNumber = 0;
        var maximumAdvanceWidth = 0;

        // replace all placeholders with the widest number (two digits)
        var format = main.timeFormat.replace(/(h+|m+|s+)/g, "" + maximumWidthNumber + maximumWidthNumber); // make sure maximumWidthNumber is formatted as string
        // build the time string twice, once with an AM time and once with a PM time
        var date = new Date(2000, 0, 1, 1, 0, 0);
        // set the sizehelper's text to the widest time string

    }

    function dateTimeChanged()
    {
        var doCorrections = false;

        if (main.showDate) {
            // If the date has changed, force size recalculation, because the day name
            // or the month name can now be longer/shorter, so we need to adjust applet size
            var currentDate = Qt.formatDateTime(dataSource.data["Local"]["DateTime"], "yyyy-mm-dd");
            if (main.lastDate != currentDate) {
                doCorrections = true;
                main.lastDate = currentDate
            }
        }

    }




}
