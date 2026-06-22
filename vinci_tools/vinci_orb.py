import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPainter, QColor, QRadialGradient, QBrush, QPen, QPainterPath
import math
import random

class GargantuaPyQt(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vinci Gargantua Supernova")
        self.setFixedSize(600, 600)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.angle = 0
        self.particles = []
        self.plane_tilt = 0.3 
        self.is_locked = False
        
        for _ in range(80):
            self.particles.append({
                "angle": random.uniform(0, 2 * math.pi),
                "dist": random.uniform(50, 180),
                "speed": random.uniform(0.02, 0.05),
                "size": random.uniform(1.5, 3),
                "color": random.choice([QColor(255, 255, 255), QColor(255, 255, 200), QColor(255, 200, 50), QColor(255, 150, 0)])
            })

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)

        self.old_pos = None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F10:
            self.toggle_lock()

    def toggle_lock(self):
        self.is_locked = not self.is_locked
        if self.is_locked:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos is not None:
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    def update_animation(self):
        self.angle += 0.03
        for p in self.particles:
            p["angle"] += p["speed"]
        self.update()

    def draw_ring(self, painter, cx, cy, ring_dist, ring_tilt, is_front):
        clip_rect = QPainterPath()
        if is_front:
            clip_rect.addRect(0, cy, 600, 600 - cy)
        else:
            clip_rect.addRect(0, 0, 600, cy)

        painter.save()
        painter.setClipPath(clip_rect)
        painter.setBrush(Qt.NoBrush)

        glow_pen = QPen(QColor(255, 180, 0, 80))
        glow_pen.setWidth(6)
        painter.setPen(glow_pen)
        painter.drawEllipse(int(cx - ring_dist), int(cy - ring_dist * ring_tilt), int(ring_dist * 2), int(ring_dist * 2 * ring_tilt))

        core_pen = QPen(QColor(255, 255, 255, 200))
        core_pen.setWidth(2)
        painter.setPen(core_pen)
        painter.drawEllipse(int(cx - ring_dist), int(cy - ring_dist * ring_tilt), int(ring_dist * 2), int(ring_dist * 2 * ring_tilt))

        painter.restore()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        cx, cy = 300, 300

        bloom = QRadialGradient(cx, cy, 250)
        bloom.setColorAt(0, QColor(255, 120, 0, 100))
        bloom.setColorAt(0.4, QColor(150, 50, 0, 60))
        bloom.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(QBrush(bloom))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(cx - 250, cy - 250, 500, 500)

        for p in self.particles:
            px = cx + p["dist"] * math.cos(p["angle"])
            py = cy + (p["dist"] * self.plane_tilt) * math.sin(p["angle"])
            if py < cy:
                self.draw_particle(painter, px, py, p)

        for i in range(1, 4):
            ring_angle = self.angle * (0.5 / i)
            ring_dist = 60 + (i * 25)
            ring_tilt = math.sin(ring_angle) * 0.3
            self.draw_ring(painter, cx, cy, ring_dist, ring_tilt, is_front=False)

        core_glow = QRadialGradient(cx, cy, 45)
        core_glow.setColorAt(0, QColor(0, 0, 0))
        core_glow.setColorAt(0.1, QColor(0, 0, 0))
        core_glow.setColorAt(0.15, QColor(255, 255, 255))
        core_glow.setColorAt(0.25, QColor(255, 255, 150))
        core_glow.setColorAt(0.4, QColor(255, 180, 0))
        core_glow.setColorAt(0.7, QColor(255, 80, 0, 200))
        core_glow.setColorAt(1, QColor(0, 0, 0, 0))

        painter.setBrush(QBrush(core_glow))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(cx - 100, cy - 100, 200, 200)

        painter.setBrush(QBrush(QColor(0, 0, 0)))
        painter.drawEllipse(cx - 30, cy - 30, 60, 60)

        for i in range(1, 4):
            ring_angle = self.angle * (0.5 / i)
            ring_dist = 60 + (i * 25)
            ring_tilt = math.sin(ring_angle) * 0.3
            self.draw_ring(painter, cx, cy, ring_dist, ring_tilt, is_front=True)

        for p in self.particles:
            px = cx + p["dist"] * math.cos(p["angle"])
            py = cy + (p["dist"] * self.plane_tilt) * math.sin(p["angle"])
            if py >= cy:
                self.draw_particle(painter, px, py, p)

    def draw_particle(self, painter, px, py, p):
        glow_color = QColor(p["color"].red(), p["color"].green(), p["color"].blue(), 100)
        painter.setBrush(QBrush(glow_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(int(px - p["size"]), int(py - p["size"]), int(p["size"]*2), int(p["size"]*2))
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        painter.drawEllipse(int(px - p["size"]/2), int(py - p["size"]/2), int(p["size"]), int(p["size"]))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GargantuaPyQt()
    window.show()
    sys.exit(app.exec_())
