# Based on Flet.dev audio player example https://github.com/flet-dev/flet-contrib/tree/main/flet_contrib/audio_player

import flet as ft
from audio_player import AudioPlayer

def main(page: ft.Page):
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

    # Container for song information
    song_info = ft.Container(
        content=ft.Column(
            [
                ft.Container(  # Use a container to center the image
                    content=ft.Image(
                        src=cover_image,
                        width=200,
                        height=200,
                        fit=ft.ImageFit.COVER,
                    ),
                    alignment=ft.alignment.center,
                ),
                ft.Text(
                    f"Artist: {current_track['artist']}",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    width=300,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    f"Title: {current_track['title']}",
                    size=14,
                    width=300,
                    text_align=ft.TextAlign.CENTER,
                    italic=False,  # Title not italicized
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Center everything vertically in the column
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Center everything horizontally
            spacing=10,
        ),
        padding=10,
        margin=10,
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
        # Use the image of the new track
        cover_image = new_song.get("image", "https://via.placeholder.com/300?text=No+Cover")

        # Update the song info container
        song_info.content = ft.Column(
            [
                ft.Container(
                    content=ft.Image(
                        src=cover_image,
                        width=200,
                        height=200,
                        fit=ft.ImageFit.COVER,
                    ),
                    alignment=ft.alignment.center,
                ),
                ft.Text(
                    f"Artist: {new_song.get('artist', 'Unknown')}",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    width=300,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    f"Title: {new_song.get('title', 'No Title')}",
                    size=14,
                    width=300,
                    text_align=ft.TextAlign.CENTER,
                    italic=False,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )

        # Update the background with the new track's image
        background_container.content = ft.Image(
            src=cover_image,  # Use the new track's image
            width=page.width,
            height=page.height,
            fit=ft.ImageFit.COVER,
        )

        # Refresh the page
        page.update()

    # Add AudioPlayer with the callback
    audio_player = AudioPlayer(
        page=page,
        src=playlist[current_track_index]["url"],
        width=page.width / 2,
        playlist=playlist,
        on_track_change=update_song_info,  # Callback when track changes
    )

    # Add the stack with background and content
    page.add(
        ft.Stack(
            controls=[
                background_container,  # Add the background first
                ft.Column(  # Add the remaining content on top
                    [
                        song_info,
                        audio_player,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ]
        )
    )

    # Dynamically adjust the background when the page size changes
    def on_resize(e):
        # Ensure the background always matches the page size
        background_container.width = page.width
        background_container.height = page.height

        # Adjust only the size of the background without reloading
        background_container.content.width = page.width
        background_container.content.height = page.height

        # Refresh the page
        page.update()

    page.on_resize = on_resize  # Bind the resize handler

ft.app(main)
