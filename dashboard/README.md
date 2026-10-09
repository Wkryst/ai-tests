# Linux News Radar

Dashboard z `youtube_videos.json`: newsy tygodniowo wg kanału, rozkład ważności, najczęstsze encje i tematy, tabela kanałów, lista newsów z filtrami i tabela filmów.

```bash
python3 dashboard/build.py   # generuje dashboard/index.html z danymi wbudowanymi w plik
```

`index.html` działa offline: wystarczy otworzyć go w przeglądarce (w Codespace: prawy klik → *Open with Live Server* / *Show Preview* albo `python3 -m http.server`). Transkrypcje nie trafiają do strony, więc ma ok. 330 KB zamiast 1,6 MB.

Nazwy kanałów nie są zapisane w JSON, dlatego dashboard pokazuje skrócone ID. Żeby je podmienić, uzupełnij `CHANNEL_NAMES` w `build.py` i zbuduj stronę ponownie.
