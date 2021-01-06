// main.qml

import QtQuick 2.6
import QtQuick.Layouts 1.1
import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.plasma.components 2.0 as Components
import org.kde.plasma.private.digitalclock 1.0


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
                // get the time for the given timezone from the dataengine
                var now = dataSource.data[plasmoid.configuration.lastSelectedTimezone]["DateTime"];
                // get current UTC time
                var msUTC = now.getTime() + (now.getTimezoneOffset() * 60000);
                // add the dataengine TZ offset to it
                var currentTime = new Date(msUTC + (dataSource.data[plasmoid.configuration.lastSelectedTimezone]["Offset"] * 1000));

                main.currentTime = currentTime;
                return Qt.formatTime(currentTime, main.timeFormat);
            }

            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
        }

    }

}
