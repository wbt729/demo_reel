import QtQuick 2.12
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.12

//import ":/qml"


ApplicationWindow {
    id: mainWindow
    visible: true
    width: 1200
    height: 600

    header: ApplicationBar {
        
    }

    SidePanel {
        id: drawer
        edge: Qt.LeftEdge
        width: mainWindow.width * 0.25
        height: mainWindow.height - header.height
        y: header.height
    }

        Image {
            id: img
            // source: "image://customImageProvider/yellow"
            fillMode: Image.PreserveAspectFit
            anchors {
                top: parent.top
                bottom: parent.bottom
                left: parent.left
                right: parent.right
                horizontalCenter: parent.horizontalCenter
                margins: 16
            }

            Timer {
                running: true
                repeat: true
                interval: 50
                onTriggered: {
                    img.source = "image://customImageProvider/yellow" + Math.random()
                }
            }
            Column {
                Button {
                    text: "Pose"
                    onClicked: imgproc.start_pose()
                }
                Button {
                    text: "Hands"
                    onClicked: imgproc.start_hands()
                }
                Button {
                    text: "Screws"
                    onClicked: imgproc.start_screws()
                }
            }
        }
}