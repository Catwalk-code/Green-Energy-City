"""Swipeable card widget for Green Energy City."""

from kivy.uix.floatlayout import FloatLayout
from kivy.properties import (
    NumericProperty,
    StringProperty,
    ListProperty,
)
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.lang import Builder

Builder.load_string("""
<SwipeCard>:
    size_hint: None, None
    size: dp(300), dp(390)

    # ── Card background (rotated) ───────────────────────────────────
    canvas.before:
        PushMatrix
        Rotate:
            angle: root.card_rotation
            origin: root.center
        # Soft drop-shadow
        Color:
            rgba: 0, 0, 0, 0.18
        RoundedRectangle:
            pos: root.x + 4, root.y - 4
            size: root.size
            radius: [dp(18)]
        # Card face
        Color:
            rgba: root.card_color
        RoundedRectangle:
            pos: root.pos
            size: root.size
            radius: [dp(18)]
    canvas.after:
        PopMatrix

    # ── Character name ───────────────────────────────────────────────
    Label:
        text: root.character_name
        font_size: sp(16)
        bold: True
        color: 0.15, 0.45, 0.15, 1
        size_hint: None, None
        size: root.width - dp(32), dp(38)
        pos: root.x + dp(16), root.top - dp(52)
        halign: 'center'
        valign: 'middle'
        text_size: self.size

    # ── Horizontal divider ───────────────────────────────────────────
    Widget:
        size_hint: None, None
        size: root.width - dp(32), dp(1)
        pos: root.x + dp(16), root.top - dp(56)
        canvas:
            Color:
                rgba: 0.75, 0.9, 0.75, 1
            Rectangle:
                pos: self.pos
                size: self.size

    # ── Card body text ───────────────────────────────────────────────
    Label:
        text: root.card_text
        font_size: sp(14)
        color: 0.12, 0.12, 0.12, 1
        size_hint: None, None
        size: root.width - dp(32), root.height - dp(130)
        pos: root.x + dp(16), root.y + dp(55)
        text_size: self.size
        halign: 'center'
        valign: 'middle'

    # ── Left choice label ────────────────────────────────────────────
    Label:
        text: root.left_text
        font_size: sp(12)
        bold: True
        color: 0.85, 0.15, 0.15, root.left_alpha
        opacity: root.left_alpha
        size_hint: None, None
        size: root.width * 0.42, dp(32)
        pos: root.x + dp(10), root.center_y - dp(16)
        halign: 'center'
        valign: 'middle'
        text_size: self.size
        canvas.before:
            Color:
                rgba: 1, 0.85, 0.85, root.left_alpha * 0.55
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(8)]

    # ── Right choice label ───────────────────────────────────────────
    Label:
        text: root.right_text
        font_size: sp(12)
        bold: True
        color: 0.1, 0.65, 0.1, root.right_alpha
        opacity: root.right_alpha
        size_hint: None, None
        size: root.width * 0.42, dp(32)
        pos: root.right - root.width * 0.42 - dp(10), root.center_y - dp(16)
        halign: 'center'
        valign: 'middle'
        text_size: self.size
        canvas.before:
            Color:
                rgba: 0.85, 1, 0.85, root.right_alpha * 0.55
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(8)]

    # ── Swipe hint ───────────────────────────────────────────────────
    Label:
        text: '← swipe to decide →'
        font_size: sp(11)
        color: 0.5, 0.5, 0.5, 0.75
        size_hint: None, None
        size: root.width, dp(24)
        pos: root.x, root.y + dp(14)
        halign: 'center'
""")


class SwipeCard(FloatLayout):
    """A card widget that can be swiped left or right to make a choice."""

    card_rotation = NumericProperty(0)
    card_color = ListProperty([1, 1, 1, 1])
    character_name = StringProperty("Character")
    card_text = StringProperty("Card text goes here.")
    left_text = StringProperty("No")
    right_text = StringProperty("Yes")
    left_alpha = NumericProperty(0)
    right_alpha = NumericProperty(0)

    # Pixels of horizontal travel required to commit to a swipe decision
    SWIPE_THRESHOLD = 100
    # Maximum card tilt angle (degrees) during a drag; keeps text readable
    MAX_ROTATION = 10

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._touch_start = None
        self._orig_pos = None
        self.swipe_callback = None
        self._animating = False

    # ------------------------------------------------------------------
    # Touch handling
    # ------------------------------------------------------------------

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and not self._animating:
            touch.grab(self)
            self._touch_start = (touch.x, touch.y)
            self._orig_pos = list(self.pos)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is not self:
            return super().on_touch_move(touch)

        dx = touch.x - self._touch_start[0]
        dy = touch.y - self._touch_start[1]

        # Translate card (vertical movement dampened)
        self.x = self._orig_pos[0] + dx
        self.y = self._orig_pos[1] + dy * 0.25

        # Tilt proportional to horizontal travel
        self.card_rotation = -(dx / Window.width) * self.MAX_ROTATION * 2.5

        # Update choice hint overlays
        hint_start = self.SWIPE_THRESHOLD * 0.35
        hint_range = self.SWIPE_THRESHOLD * 0.65

        if dx > hint_start:
            alpha = min(1.0, (dx - hint_start) / hint_range)
            self.right_alpha = alpha
            self.left_alpha = 0
            g = 1.0
            rb = 1.0 - alpha * 0.07
            self.card_color = [rb, g, rb, 1]
        elif dx < -hint_start:
            alpha = min(1.0, (-dx - hint_start) / hint_range)
            self.left_alpha = alpha
            self.right_alpha = 0
            r = 1.0
            gb = 1.0 - alpha * 0.07
            self.card_color = [r, gb, gb, 1]
        else:
            self.left_alpha = 0
            self.right_alpha = 0
            self.card_color = [1, 1, 1, 1]

        return True

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return super().on_touch_up(touch)

        touch.ungrab(self)
        dx = touch.x - self._touch_start[0]

        if dx >= self.SWIPE_THRESHOLD:
            self._swipe_out("right")
        elif dx <= -self.SWIPE_THRESHOLD:
            self._swipe_out("left")
        else:
            self._snap_back()

        return True

    # ------------------------------------------------------------------
    # Animations
    # ------------------------------------------------------------------

    def _swipe_out(self, direction):
        self._animating = True
        target_x = (Window.width * 1.4) if direction == "right" else (-self.width * 1.4)
        end_angle = self.MAX_ROTATION * 2 if direction == "right" else -self.MAX_ROTATION * 2

        anim = Animation(
            x=target_x,
            card_rotation=end_angle,
            opacity=0,
            duration=0.30,
            t="out_quad",
        )
        anim.bind(on_complete=lambda *_: self._on_swipe_done(direction))
        anim.start(self)

    def _snap_back(self):
        if self._orig_pos is None:
            return
        anim = Animation(
            x=self._orig_pos[0],
            y=self._orig_pos[1],
            card_rotation=0,
            duration=0.22,
            t="out_elastic",
        )
        anim.bind(on_complete=lambda *_: self._reset_tint())
        anim.start(self)

    def _reset_tint(self):
        self.card_color = [1, 1, 1, 1]
        self.left_alpha = 0
        self.right_alpha = 0

    def _on_swipe_done(self, direction):
        self._animating = False
        if self.swipe_callback:
            self.swipe_callback(direction)
