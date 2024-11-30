# based on Flet.dev audio player example https://github.com/flet-dev/flet-contrib/tree/main/flet_contrib/audio_player
# TO DO: the play pause is not working right the first time. Also the prev button should reset the current track and after two presses go back to the previous track.


import os
from datetime import timedelta
import flet_core as ft
from utils import format_timedelta_str_ms

class AudioPlayer(ft.Container):
    def __init__(
        self,
        page: ft.Page,
        src_dir: str | None = None,
        src: str | None = None,
        curr_idx: int = 0,
        font_family: str | None = None,
        controls_vertical_alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.START,
        controls_horizontal_alignment: ft.CrossAxisAlignment = ft.CrossAxisAlignment.START,
        playlist: list = None,
        on_track_change=None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.page_ = page
        self.font_family = font_family
        self.curr_idx = curr_idx
        self.playlist = playlist or []
        self.src_dir_contents = [track["url"] for track in self.playlist]
        self.curr_song_name = self.src_dir_contents[self.curr_idx]
        self.on_track_change = on_track_change
        self.is_request_pending = False  # Prevent race conditions
        self.duration = 0  # Audiolength

        # Logging for debugging
        print(f"AudioPlayer initialized with playlist: {self.playlist}")

        # Initialisatie van controls
        self.seek_bar = ft.ProgressBar(width=self.width)
        self.times_row = ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        self.play_controls = ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.icons.SKIP_PREVIOUS_SHARP,
                                data="prev",
                                on_click=self.prev_next_music,
                            ),
                            play_pause_btn := ft.IconButton(
                                icon=ft.icons.PLAY_ARROW, on_click=self.play_pause
                            ),
                            ft.IconButton(
                                icon=ft.icons.SKIP_NEXT_SHARP,
                                data="next",
                                on_click=self.prev_next_music,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=0,
                    ),
                ],
                spacing=0,
            ),
            width=page.width,
            alignment=ft.alignment.center,
            margin=0,
        )

        self.contents = [self.seek_bar, self.times_row, self.play_controls]
        self.content = ft.Column(
            self.contents,
            alignment=controls_vertical_alignment,
            horizontal_alignment=controls_horizontal_alignment,
        )

        self.audio = ft.Audio(
            src=self.src_dir_contents[self.curr_idx],
            volume=1,
            on_loaded=self._show_controls,
            on_state_changed=self._on_audio_state_changed,
            on_position_changed=self._update_controls,
        )
        self.page_.overlay.append(self.audio)
        self.page_.update()

        self.play_pause_btn = play_pause_btn
        self.playing = False  # Keep the status of playing

    def prev_next_music(self, e):
        if self.is_request_pending:
            print("Action ignored: Another action is pending.")
            return
    
        self.is_request_pending = True
    
        if e.control.data == "next":
            # Next track
            self.curr_idx = (self.curr_idx + 1) % len(self.playlist)
        elif e.control.data == "prev":
            # Reset the progress to 0 before proceeding tot the next track
            self.seek_bar.value = 0
            print(f"Resetting progress to 0 for the current track")
            
            # Check if there's a previous  track and go back to that track
            if self.curr_idx > 0:
                self.curr_idx -= 1
            else:
                print("No previous track, staying on current track.")
    
        print(f"Switching to track index: {self.curr_idx}")
        # Update the track after reset of the progress
        self._update_track()


    def _update_track(self):
        new_song = self.playlist[self.curr_idx]
        self.audio.src = new_song["url"]
        self.audio.play()

        print(f"Track updated to: {new_song['url']}")
        self.play_pause_btn.icon = ft.icons.PAUSE
        self.playing = True
        if self.on_track_change:
            self.on_track_change(new_song)
        self.page_.update()

    def play_pause(self, e):
        if self.is_request_pending:
            print("Play/Pause ignored: Another action is pending.")
            return

        self.is_request_pending = True
        if self.playing:
            print("Pausing audio...")
            self.audio.pause()
        else:
            print("Playing audio...")
            self.audio.play()

    def _on_audio_state_changed(self, e):
        print(f"Audio state changed: {e.data}")
        if e.data == "paused":
            self.play_pause_btn.icon = ft.icons.PLAY_ARROW
            self.playing = False
        elif e.data == "playing":
            self.play_pause_btn.icon = ft.icons.PAUSE
            self.playing = True
        else:
            print(f"Unhandled audio state: {e.data}")
        
        self.is_request_pending = False
        self.page_.update()

    def _show_controls(self, e):
        print("Audio loaded; initializing controls.")
        self.seek_bar.value = 0
        self.duration = self.audio.get_duration()

        elapsed_time, duration = self._calculate_formatted_times(0)
        self._update_times_row(elapsed_time, duration)

    def _update_controls(self, e):
        if e.data == "0":  # Audio done
            self.play_pause_btn.icon = ft.icons.PLAY_ARROW
            self.playing = False
            print("Audio completed; resetting play button.")
            self.page_.update()
            return

        curr_time = int(e.data)
        if self.duration > 0:
            self.seek_bar.value = curr_time / self.duration

        elapsed_time, duration = self._calculate_formatted_times(curr_time)
        self._update_times_row(elapsed_time, duration)

    def _calculate_formatted_times(self, elapsed_time: int):
        formatted_elapsed_time = format_timedelta_str_ms(
            str(timedelta(milliseconds=elapsed_time))
        )
        formatted_time_duration = format_timedelta_str_ms(
            str(timedelta(milliseconds=self.duration))
        )
        return formatted_elapsed_time, formatted_time_duration

    def _update_times_row(self, elapsed_time, time_duration):
        self.times_row.controls = [
            ft.Text(elapsed_time, font_family=self.font_family),
            ft.Text(time_duration, font_family=self.font_family),
        ]
        self.page_.update()
