# STL File Splitter

Split an STL mesh into a grid of smaller pieces along the X and Y axes. Choose the number of divisions or specify a printer's maximum X/Y dimensions so the tool calculates them.

This fork includes a Streamlit interface as well as the original command-line script.

[Hosted app](https://stl-file-splitter.streamlit.app/)

## Terminal demo

![Recorded terminal usage](docs/images/cli-demo.gif)

Recorded with [VHS](https://github.com/charmbracelet/vhs). [Recording source and instructions](docs/demo/README.md).

## Install

Use a Python version compatible with the dependencies in `requirements.txt`.

```bash
git clone https://github.com/SpyC0der77/stl-file-splitter.git
cd stl-file-splitter
python -m pip install -r requirements.txt
```

## Web interface

```bash
streamlit run streamlit_app.py
```

Upload an STL, choose the split settings, and download the resulting parts as a ZIP file. The interface displays model and segment dimensions.

## Command line

```bash
python split-file.py model.stl --xsplit 4 --ysplit 3
python split-file.py model.stl --max-x 200 --max-y 200
python split-file.py model.stl --xsplit 3 --max-y 150 --flip
```

| Option | Behavior |
| --- | --- |
| `--xsplit N` | Number of X divisions |
| `--ysplit N` | Number of Y divisions |
| `--max-x N` or `-mx N` | Maximum X dimension used to calculate divisions |
| `--max-y N` or `-my N` | Maximum Y dimension used to calculate divisions |
| `--flip` | Rotate the model 180 degrees around the X axis before splitting |

Explicit split counts take precedence over maximum dimensions on the same axis. With no settings, both axes default to one division. The CLI writes non-empty parts beside the input file as `model_splt-01.stl`, `model_splt-02.stl`, and so on.

## Limitations

Splitting uses Trimesh boolean intersections and the `manifold3d` backend. Mesh validity affects whether intersections succeed. STL files have no standard unit metadata; the dimension settings assume the input coordinates represent millimeters. The tool does not add alignment pins or connectors to the pieces.

## License

[MIT](LICENSE). The fork is based on [joeatbayes/stl-file-splitter](https://github.com/joeatbayes/stl-file-splitter).
