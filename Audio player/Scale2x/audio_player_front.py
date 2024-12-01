# Based on Flet.dev audio player example https://github.com/flet-dev/flet-contrib/tree/main/flet_contrib/audio_player

import flet as ft
from audio_player2x import AudioPlayer

def main(page: ft.Page):
    page.window.width = 1100
    page.window.height = 900
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Playlist (list of audio URLs with associated metadata)
    playlist = [
        {
            "url": "https://samplesongs.netlify.app/Bad%20Liar.mp3",
            "title": "Bad Liar",
            "artist": "Imagine Dragons",
            "image": "https://i1.sndcdn.com/artworks-000527091948-ykpqq9-t500x500.jpg",
        },
        {
            "url": "https://samplesongs.netlify.app/Death%20Bed.mp3",
            "title": "Death Bed",
            "artist": "Powfu ft. Beabadoobee",
            "image": "https://cdn-images.dzcdn.net/images/cover/85380bbb010f1b675c29ac06c6e343ea/0x1900-000000-80-0-0.jpg",
        },
        {
            "url": "https://github.com/mdn/webaudio-examples/blob/main/audio-analyser/viper.mp3?raw=true",
            "title": "Viper",
            "artist": "Unknown Artist",
            "image": "https://images.squarespace-cdn.com/content/v1/5d2e2c5ef24531000113c2a4/1564770283101-36J6KM8EIK71FOCGGDM2/album-placeholder.png",
        },
    ]

    # Current track index
    current_track_index = 0
    current_track = playlist[current_track_index]

    # Fallback image
    cover_image = current_track["image"] or "https://via.placeholder.com/200?text=No+Cover"

    # Scaling factor
    scale_factor = 2.0

    # Container for song information
    song_info = ft.Container(
        content=ft.Column(
            [
                ft.Container(  # Album cover
                    content=ft.Image(
                        src=cover_image,
                        width=200 * scale_factor,  # Schaal de breedte
                        height=200 * scale_factor,  # Schaal de hoogte
                        fit=ft.ImageFit.COVER,
                    ),
                    alignment=ft.alignment.center,
                ),
                ft.Text(
                    f"Artist: {current_track['artist']}",
                    size=16 * scale_factor,  # Schaal de tekstgrootte
                    weight=ft.FontWeight.BOLD,
                    width=300 * scale_factor,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    f"Title: {current_track['title']}",
                    size=14 * scale_factor,  # Schaal de tekstgrootte
                    width=300 * scale_factor,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10 * scale_factor,  # Schaal de spacing
        ),
        padding=10 * scale_factor,
        margin=10 * scale_factor,
        alignment=ft.alignment.center,
    )

    # Container for the background with transparency (set once)
    background_container = ft.Container(
        content=ft.Image(
            src=current_track["image"],  # Start with the first track's image
            width=page.width,
            height=page.height,
            fit=ft.ImageFit.COVER,
        ),
        width=page.width,
        height=page.height,
        alignment=ft.alignment.center,
        opacity=0.2,
    )

    # Function to update the background and song information
    def update_song_info(new_song):
        cover_image = new_song.get("image", "https://via.placeholder.com/300?text=No+Cover")

        song_info.content = ft.Column(
            [
                ft.Container(
                    content=ft.Image(
                        src=cover_image,
                        width=200 * scale_factor,
                        height=200 * scale_factor,
                        fit=ft.ImageFit.COVER,
                    ),
                    alignment=ft.alignment.center,
                ),
                ft.Text(
                    f"Artist: {new_song.get('artist', 'Unknown')}",
                    size=16 * scale_factor,
                    weight=ft.FontWeight.BOLD,
                    width=300 * scale_factor,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    f"Title: {new_song.get('title', 'No Title')}",
                    size=14 * scale_factor,
                    width=300 * scale_factor,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10 * scale_factor,
        )

        background_container.content = ft.Image(
            src=cover_image,
            width=page.width,
            height=page.height,
            fit=ft.ImageFit.COVER,
        )

        page.update()

    # Add AudioPlayer with the callback
    audio_player = AudioPlayer(
        page=page,
        src=playlist[current_track_index]["url"],
        width=page.width / 2,
        playlist=playlist,
        on_track_change=update_song_info,
    )

    # Vergroot de schaal van de AudioPlayer
    audio_player.scale = ft.Scale(scale_factor, scale_factor)

    # Add the stack with background and content
    page.add(
        ft.Stack(
            controls=[
                background_container,
                ft.Column(
                    [
                        song_info,
                        ft.Container(
                            content=audio_player,
                            padding=ft.padding.Padding(top=20 * scale_factor, left=0, right=0, bottom=0),  # Correct alle parameters opgegeven
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ]
        )
    )

    # Dynamically adjust the background when the page size changes
    def on_resize(e):
        background_container.width = page.width
        background_container.height = page.height
        background_container.content.width = page.width
        background_container.content.height = page.height
        page.update()

    page.on_resized = on_resize

ft.app(main)

