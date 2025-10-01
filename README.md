# MP4 ➜ MP3 Converter

A tiny Python helper that batch-converts videos to compressed MP3 files using [`ffmpeg`](https://ffmpeg.org/).

## Prerequisites

- Python 3.8 or newer
- `ffmpeg` installed and available on your system `PATH`

On Windows you can install ffmpeg via [gyan.dev builds](https://www.gyan.dev/ffmpeg/builds/) or through a package manager such as [Chocolatey](https://community.chocolatey.org/packages/ffmpeg).

## Folder layout

```
mp4 to mp3/
├── convert_mp4_to_mp3.py
├── input mp4/      # place your source .mp4, .m4v, or .mov files here
└── output mp3/     # converted .mp3 files are written here
```

## Usage

1. Copy your video files into the `input mp4` directory.
2. Run the converter script from the project root:

```powershell
python .\convert_mp4_to_mp3.py
```

Converted MP3 files are written to `output mp3` with the same relative structure as the inputs.

### Command-line options

| Option | Description | Default |
| ------ | ----------- | ------- |
| `--input-dir` | Folder containing source videos | `input mp4` |
| `--output-dir` | Folder for MP3 output | `output mp3` |
| `--bitrate` | Target audio bitrate (e.g. `128k`, `192k`) | `192k` |
| `--overwrite` | Overwrite existing MP3 files instead of skipping | off |
| `--recursive` | Scan sub-folders inside the input directory | off |
| `--extensions` | Space-separated list of extensions to process | `.mp4 .m4v .mov` |

Example using custom settings:

```powershell
python .\convert_mp4_to_mp3.py --bitrate 160k --recursive --overwrite
```

## Troubleshooting

- **`RuntimeError: ffmpeg is not installed`** – Install ffmpeg and ensure `ffmpeg.exe` is on your `PATH`.
- **Conversion skipped** – Existing MP3 files are skipped unless you pass `--overwrite`.
- **Slow conversions** – Lower the target bitrate (e.g. `128k`) or process fewer files at once.

## License

This project is provided without warranty; feel free to adapt it to your needs.
