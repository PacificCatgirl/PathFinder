import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import networkx as nx
import wikipediaapi
import algorithm


class GraphCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=8, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)
        self.ax = self.fig.add_subplot(111)

    def draw_graph(self, edges):
        self.ax.clear()
        G = nx.Graph()
        G.add_edges_from(edges)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, ax=self.ax, with_labels=True, node_size=700, font_size=8)
        self.draw()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Найти путь в Википедии")
        layout = QVBoxLayout()

        self.startPageInput = QLineEdit(self)
        self.startPageInput.setPlaceholderText("Откуда")
        layout.addWidget(self.startPageInput)

        self.endPageInput = QLineEdit(self)
        self.endPageInput.setPlaceholderText("Куда")
        layout.addWidget(self.endPageInput)

        self.button = QPushButton("Искать", self)
        self.button.clicked.connect(self.find)
        layout.addWidget(self.button)

        self.canvas = GraphCanvas(self)
        layout.addWidget(self.canvas)

        self.setLayout(layout)
        self.resize(1200, 800)

    def find(self):
        start_page = self.startPageInput.text()
        end_page = self.endPageInput.text()

        wiki = wikipediaapi.Wikipedia(
            language='ru',
            user_agent='WikiPathFinder/1.0 (contact@example.com)'
        )

        page_start = wiki.page(start_page)
        page_finish = wiki.page(end_page)

        if not page_start.exists():
            print("Стартовая страница не существует")
            return

        if not page_finish.exists():
            print("Целевая страница не существует")
            return

        graph = algorithm.create_graph(page_start, page_finish, 500)
        path = algorithm.dijkstra(graph, page_start.title, page_finish.title)

        if not path:
            print("Путь не найден")
            return

        edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        self.canvas.draw_graph(edges)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())