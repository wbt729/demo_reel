import QtQuick 2.12
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.12
import QtQuick.Controls.Material 2.12

ToolBar {
    Material.primary: "#3d3d3b"
        Row {
            anchors {
                left: parent.left
                verticalCenter: parent.verticalCenter
                rightMargin: 16
            }

        ToolButton {
            icon.source: "qrc:/icons/menu.svg"
            anchors.verticalCenter: parent.verticalCenter
            onClicked: {
                drawer.visible = !drawer.visible
            }
            icon.color: "white"
        }

        Label {
            text: drawer.pageName
            anchors.verticalCenter: parent.verticalCenter
            font.pointSize: 12
            font.bold: true
            color: "white"
        }
    }
}