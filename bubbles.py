import sys
import marimo

__generated_with = "0.13.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import PIL
    from PIL import Image, ImageDraw
    import io
    import pathlib
    import argparse
    from typing import Optional
    return Image, ImageDraw, Optional, PIL, argparse, io, mo, pathlib


@app.cell
def _(Optional, argparse, mo):
    class MoFile:
        def __init__(self, name, contents):
            self._name = name
            self._contents = contents

        def contents(self) -> Optional[bytes]:
            return self._contents

        def name(self) -> str:
            return self._name

    if mo.running_in_notebook():
        file = mo.ui.file(filetypes=[".png", ".jpg", ".webp", ".gif"])
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("path")
        parser.add_argument("-o", "--output")
        args = parser.parse_args()

        with open(args.path, "rb") as f:
            contents = f.read()

        file = MoFile(args.path, contents)
    
    file
    return args, file


@app.cell
def _(PIL, file, io, mo):
    if mo.running_in_notebook():
        mo.stop(file.contents() is None, mo.md("**Select a file to continue!**"))
    
    img = PIL.Image.open(io.BytesIO(file.contents())).convert("RGBA")
    img
    return (img,)


@app.cell
def _(Image, ImageDraw, img):
    res = Image.new("RGBA", (img.width, img.height + img.width // 12))
    res.paste(img, (0, img.width // 12))
    draw = ImageDraw.Draw(res)

    draw.ellipse([(-img.width // 2, -img.width * 3/4), (img.width * 1.5, img.width // 7)], fill=(0, 0, 0, 0))
    draw.polygon([(49/64 * img.width, img.width // 4), (.82 * img.width, 0), (img.width, .0445 * img.width)], fill=(0, 0, 0, 0))
    return (res,)


@app.cell
def _(args, file, io, mo, pathlib, res):
    def save():
        path = pathlib.Path(file.name())

        if not mo.running_in_notebook():
            if args.output:
                out_path = args.output
            else:
                out_path = path.with_stem(path.stem + "_bubble")

            try:
                res.save(out_path)
                print(f"Saved result to {out_path}")
            except (ValueError, OSError) as e:
                print(f"Unable to save: {e}")
                sys.exit(1)
        else:
            bin = io.BytesIO()
            res.save(bin, format="png")

            return mo.vstack(
                [
                    mo.image(res, height=400),
                    mo.download(
                        bin,
                        filename=str(path.with_stem(path.stem + "_bubble")),
                        mimetype="image/png",
                    ),
                ],
                align="center",
                justify="space-around",
            )


    save()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
