import QtQuick 2.6
import QtQuick.Layouts 1.1
import org.kde.plasma.core 2.0 as PlasmaCore
import org.kde.plasma.components 2.0 as Components
import org.kde.plasma.private.digitalclock 1.0

Item {
    id: main

    property string timeFormat
    property date currentTime


    states: [

        State {
            name: "other"
            when: plasmoid.formFactor != PlasmaCore.Types.Vertical && plasmoid.formFactor != PlasmaCore.Types.Horizontal
            
            PropertyChanges {
                target: contentItem

                height: main.height
                width: main.width
            }

            PropertyChanges {
                target: timeLabel

                height: sizehelper.height
                width: main.width

                fontSizeMode: Text.Fit
            }






            PropertyChanges {
                target: sizehelper

                height: main.height
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
                    return "hahaha " + Qt.formatTime(currentTime, "hh:mm:ss");
                }

                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
            }

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

}
