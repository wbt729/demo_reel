import QtQuick 2.12
import QtQuick.Controls 2.12

Drawer {
    id: root

//    property string pageSource: "qrc:/qml/PageSettings.qml"
//      property string pageSource: "qrc:/qml/PageAbout.qml"
//    property string pageSource: "qrc:/qml/PageDebug.qml"
    property string pageSource: "qrc:/qml/PageScan.qml"
//    property string pageSource: "qrc:/qml/PageScanHistory.qml"
//    property string pageSource: "qrc:/qml/PageCalibrate.qml"
    property string pageName: qsTr("Scan")

    ListModel {
        id: pagesModel
        ListElement {
            name: qsTr("Hands")
            icon: "qrc:/icons/hand.svg"
            page: "qrc:/qml/PageScan.qml"
        }
        ListElement {
            name: qsTr("Pose")
            icon: "qrc:/icons/people.svg"
            page: "qrc:/qml/PageSettings.qml"
        }
        ListElement {
            name: qsTr("Calibrate")
            icon: "qrc:/icons/agriculture.svg"
            page: "qrc:/qml/PageCalibrate.qml"
        }
    }

    ListView {
        id: listView
        anchors.fill: parent
        model: pagesModel
        interactive: false

        header: Pane {
            anchors { left: parent.left; right: parent.right }
            contentHeight: logo.height + 32

            Image {
                id: logo
                anchors.margins: 16
                anchors { left: parent.left; right: parent.right; top: parent.top }
                source: "qrc:/img/logo.png"
                fillMode: Image.PreserveAspectFit
            }
        }

        delegate: ItemDelegate {
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.leftMargin: 16
            text: model.name
            icon.source: model.icon
            onClicked: {
                listView.currentIndex = index
                root.visible = false
                pageSource = model.page
                pageName = model.name
            }
        }
    }
}
