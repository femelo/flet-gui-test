# based on Flet.dev audio player example https://github.com/flet-dev/flet-contrib/tree/main/flet_contrib/audio_player

import flet as ft
from audio_player import AudioPlayer

def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Playlist (lijst van audio URL's met bijbehorende metadata)
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
            "image": "https://atomageindustries.com/cdn/shop/products/PHFront.jpg",
        },
        {
            "url": "https://github.com/mdn/webaudio-examples/blob/main/audio-analyser/viper.mp3?raw=true",
            "title": "Viper",
            "artist": "Unknown Artist",
            "image": "https://images.squarespace-cdn.com/content/v1/5d2e2c5ef24531000113c2a4/1564770283101-36J6KM8EIK71FOCGGDM2/album-placeholder.png",
        },
    ]

    # Huidige track index
    current_track_index = 0
    current_track = playlist[current_track_index]

    # Fallback afbeelding
    cover_image = current_track["image"] or "https://via.placeholder.com/200?text=No+Cover"

    # Container voor songinformatie
    song_info = ft.Container(
        content=ft.Column(
            [
                ft.Container(  # Gebruik een container om de afbeelding te centreren
                    content=ft.Image(
                        src=cover_image,
                        width=200,
                        height=200,
                        fit=ft.ImageFit.COVER,
                    ),
                    alignment=ft.alignment.center,
                ),
                ft.Text(
                    f"Artiest: {current_track['artist']}",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    width=300,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    f"Titel: {current_track['title']}",
                    size=14,
                    width=300,
                    text_align=ft.TextAlign.CENTER,
                    italic=False,  # Titel niet cursief
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,  # Centreer alles verticaal in de kolom
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centreer alles horizontaal
            spacing=10,
        ),
        padding=10,
        margin=10,
        alignment=ft.alignment.center,
    )

    # Container voor de achtergrond met transparantie (dit wordt eenmaal ingesteld)
    background_container = ft.Container(
        content=ft.Image(
            src=current_track["image"],  # Begin met de afbeelding van de eerste track
            width=page.width,
            height=page.height,
            fit=ft.ImageFit.COVER,
        ),
        width=page.width,
        height=page.height,
        alignment=ft.alignment.center,
        opacity=0.2,
    )

    # Functie om de achtergrond en songinformatie bij te werken
    def update_song_info(new_song):
        # Gebruik de afbeelding van de nieuwe track
        cover_image = new_song.get("image", "https://via.placeholder.com/300?text=No+Cover")

        # Update de songinfo container
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
                    f"Artiest: {new_song.get('artist', 'Onbekend')}",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    width=300,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    f"Titel: {new_song.get('title', 'Geen Titel')}",
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

        # Update de achtergrond met de afbeelding van de nieuwe track
        background_container.content = ft.Image(
            src=cover_image,  # Gebruik de afbeelding van de nieuwe track
            width=page.width,
            height=page.height,
            fit=ft.ImageFit.COVER,
        )

        # Update de pagina
        page.update()

    # AudioPlayer toevoegen met de callback
    audio_player = AudioPlayer(
        page=page,
        src=playlist[current_track_index]["url"],
        width=page.width / 2,
        playlist=playlist,
        on_track_change=update_song_info,  # Callback bij wisselen van track
    )

    # Voeg de stack toe met achtergrond en inhoud
    page.add(
        ft.Stack(
            controls=[
                background_container,  # Voeg de achtergrond eerst toe
                ft.Column(  # Voeg de overige inhoud bovenop
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

    # Dynamisch aanpassen van de achtergrond bij wijziging van de pagina-grootte
    def on_resize(e):
        # Zorg ervoor dat de achtergrond altijd dezelfde grootte heeft als de pagina
        background_container.width = page.width
        background_container.height = page.height

        # Alleen de grootte van de achtergrond aanpassen, maar niet opnieuw laden
        background_container.content.width = page.width
        background_container.content.height = page.height

        # Werk de pagina bij
        page.update()

    page.on_resize = on_resize  # Koppel de resize-handler

ft.app(main)
