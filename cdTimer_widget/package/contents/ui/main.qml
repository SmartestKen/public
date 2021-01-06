// main.qml
import QtQuick 2.0
import org.kde.plasma.components 2.0 as PlasmaComponents
import org.kde.plasma.plasmoid 2.0

PlasmaComponents.Label {
    text: "Hello World!"

    // Always display the full view. Never show the compact icon view
    // like it does by default when shown in the panel.
    Plasmoid.preferredRepresentation: Plasmoid.fullRepresentation
}
