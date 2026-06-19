# player_style_page.py — "播放器" 导航页
"""播放器样式配置：颜色选择、歌词位置、静默/结束显示。"""

from typing import Optional

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QColorDialog,
)
from PySide6.QtCore import Qt

from qfluentwidgets import (
    LineEdit, PushButton, ComboBox,
    BodyLabel, StrongBodyLabel, HorizontalSeparator,
)

from ustPlayer.core.settings_manager import SettingsManager


def _hex_to_qss(hex_color: str) -> str:
    """确保颜色以 # 开头。"""
    hex_color = hex_color.strip()
    if not hex_color.startswith("#"):
        hex_color = "#" + hex_color
    return hex_color


class PlayerStylePage(QWidget):
    """播放器样式标签页 — 5 个颜色选择 + 歌词位置 + 静默/结束显示。"""

    def __init__(self, settings: SettingsManager, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._s = settings
        self._setup_ui()
        self._connect_signals()

    # ===================== UI 构建 =====================

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(10)

        layout.addWidget(StrongBodyLabel("/ 播放器样式"))

        # ---- 颜色选择行 ----
        self._add_color_row(layout, "背景色:", "bg_color", self._s.bg_color)
        self._add_color_row(layout, "音名色:", "note_color", self._s.note_color)
        self._add_color_row(layout, "歌字色:", "lyric_color", self._s.lyric_color)
        self._add_color_row(layout, "歌词色:", "lyric_text_color", self._s.lyric_text_color)
        self._add_color_row(layout, "其他文字色:", "other_text_color", self._s.other_text_color)

        # 歌词位置
        row_lyric = QHBoxLayout()
        row_lyric.setSpacing(8)
        row_lyric.addWidget(BodyLabel("歌词位置:"))
        self.lyric_pos_combo = ComboBox()
        self.lyric_pos_combo.addItems(["上", "下"])
        row_lyric.addWidget(self.lyric_pos_combo)
        row_lyric.addStretch()
        layout.addLayout(row_lyric)

        layout.addWidget(HorizontalSeparator())

        # ---- 其他显示设置 ----
        layout.addWidget(StrongBodyLabel("/ 其他显示设置"))

        # 音高占位符
        self._add_combo_with_custom(
            layout, "音高间占位符:", "pitch_placeholder",
            ["无", "-", "自定义文字"],
            self._s.pitch_placeholder, "pitch_custom",
        )

        # 静默时显示
        self._add_combo_with_custom(
            layout, "静默时显示:", "silent_display",
            ["R", "-", "自定义文字", "什么都不显示"],
            self._s.silent_display, "silent_custom",
        )

        # 结束时显示
        self._add_combo_with_custom(
            layout, "结束时显示:", "end_display",
            ["END", "-", "自定义文字", "什么都不显示"],
            self._s.end_display, "end_custom",
        )

        layout.addStretch()

    def _add_color_row(self, parent: QVBoxLayout, label: str, attr: str, init_color: str):
        """颜色选择行：标签 + 输入框 + 更改按钮。"""
        row = QHBoxLayout()
        row.setSpacing(8)

        row.addWidget(BodyLabel(label))

        edit = LineEdit()
        edit.setText(init_color)
        edit.setMaximumWidth(100)
        setattr(self, f"edit_{attr}", edit)
        row.addWidget(edit)

        btn = PushButton("更改")
        btn.clicked.connect(lambda: self._pick_color(attr))
        row.addWidget(btn)
        row.addStretch()

        parent.addLayout(row)

    def _add_combo_with_custom(
        self, parent: QVBoxLayout, label: str, attr: str,
        options: list, init_value: str, custom_attr: str,
    ):
        """下拉框 + 可选的自定义文字输入框。"""
        row = QHBoxLayout()
        row.setSpacing(8)

        row.addWidget(BodyLabel(label))

        combo = ComboBox()
        combo.addItems(options)
        combo.setCurrentText(init_value)
        setattr(self, f"combo_{attr}", combo)
        row.addWidget(combo)

        # 自定义文字输入框（默认隐藏）
        custom_edit = LineEdit()
        custom_edit.setPlaceholderText("自定义文字...")
        custom_edit.setMaximumWidth(150)
        custom_edit.setVisible(init_value == "自定义文字")
        setattr(self, f"edit_{custom_attr}", custom_edit)
        setattr(self, f"_custom_attr_{attr}", custom_attr)
        row.addWidget(custom_edit)

        row.addStretch()
        parent.addLayout(row)

    # ===================== 信号绑定 =====================

    def _connect_signals(self):
        s = self._s

        # 颜色输入框
        self.edit_bg_color.textChanged.connect(lambda v: setattr(s, "bg_color", v))
        self.edit_note_color.textChanged.connect(lambda v: setattr(s, "note_color", v))
        self.edit_lyric_color.textChanged.connect(lambda v: setattr(s, "lyric_color", v))
        self.edit_lyric_text_color.textChanged.connect(lambda v: setattr(s, "lyric_text_color", v))
        self.edit_other_text_color.textChanged.connect(lambda v: setattr(s, "other_text_color", v))

        # 歌词位置
        self.lyric_pos_combo.currentTextChanged.connect(lambda v: setattr(s, "lyric_pos", v))
        self.lyric_pos_combo.setCurrentText(s.lyric_pos)

        # 下拉框 + 自定义文字联动
        self._bind_combo_with_custom("pitch_placeholder", "pitch_custom")
        self._bind_combo_with_custom("silent_display", "silent_custom")
        self._bind_combo_with_custom("end_display", "end_custom")

        # 自定义文字初始化
        edit_pitch = getattr(self, "edit_pitch_custom")
        edit_pitch.setText(s.pitch_custom_text)
        edit_pitch.textChanged.connect(lambda v: setattr(s, "pitch_custom_text", v))

        edit_silent = getattr(self, "edit_silent_custom")
        edit_silent.setText(s.silent_custom_text)
        edit_silent.textChanged.connect(lambda v: setattr(s, "silent_custom_text", v))

        edit_end = getattr(self, "edit_end_custom")
        edit_end.setText(s.end_custom_text)
        edit_end.textChanged.connect(lambda v: setattr(s, "end_custom_text", v))

    def _bind_combo_with_custom(self, attr: str, custom_attr: str):
        """下拉框选择变更时，显示/隐藏自定义输入框并同步 settings。"""
        combo: ComboBox = getattr(self, f"combo_{attr}")
        custom_edit: LineEdit = getattr(self, f"edit_{custom_attr}")

        def on_change(value: str):
            setattr(self._s, attr, value)
            custom_edit.setVisible(value == "自定义文字")

        combo.currentTextChanged.connect(on_change)
        # 初始化 visibility
        custom_edit.setVisible(combo.currentText() == "自定义文字")

    # ===================== 颜色选择器 =====================

    def _pick_color(self, attr: str):
        edit: LineEdit = getattr(self, f"edit_{attr}")
        current = edit.text().strip() or "#FFFFFF"
        color = QColorDialog.getColor(Qt.GlobalColor.white if not current.startswith("#") else current, self)
        if color.isValid():
            edit.setText(color.name())
            setattr(self._s, attr, color.name())

    # ===================== 同步 =====================

    def sync_all_from_settings(self):
        """导入 uplr 后同步 UI。"""
        s = self._s
        self.edit_bg_color.setText(s.bg_color)
        self.edit_note_color.setText(s.note_color)
        self.edit_lyric_color.setText(s.lyric_color)
        self.edit_lyric_text_color.setText(s.lyric_text_color)
        self.edit_other_text_color.setText(s.other_text_color)
        self.lyric_pos_combo.setCurrentText(s.lyric_pos)
        getattr(self, "combo_pitch_placeholder").setCurrentText(s.pitch_placeholder)
        getattr(self, "edit_pitch_custom").setText(s.pitch_custom_text)
        getattr(self, "combo_silent_display").setCurrentText(s.silent_display)
        getattr(self, "edit_silent_custom").setText(s.silent_custom_text)
        getattr(self, "combo_end_display").setCurrentText(s.end_display)
        getattr(self, "edit_end_custom").setText(s.end_custom_text)
