from javax.swing import JFrame
from javax.swing import JPanel
from javax.swing.border import EmptyBorder
from java.awt import BorderLayout
from java.awt import Dimension
import utils

WINDOW_WIDTH=1100

class MainFrame(JFrame):

    def __init__(self):
        super(MainFrame, self).__init__()
        self.initUI()

    def initUI(self):
        if utils.isMac():
			self.setMinimumSize(Dimension(750, 600))
        else:
			self.setMinimumSize(Dimension(750, 700))
        self.setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE)
        self.setLocationRelativeTo(None)

        self.setBounds(100, 100, WINDOW_WIDTH, 600);
        self.content_pane = JPanel();
        self.content_pane.setBorder(EmptyBorder(0, 0, 0, 0));
        self.setContentPane(self.content_pane);
        self.content_pane.setLayout(BorderLayout(0, 0));

        self.setVisible(True)

def launch():
    MainFrame()

