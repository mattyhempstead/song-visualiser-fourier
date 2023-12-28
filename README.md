# Song Visualiser Fourier

A simple song fourier transform visualiser made while in high school (2018).

Inspired by those [YouTube music videos](https://www.youtube.com/@TrapNation).

Fourier transform code was written from scratch based on my understanding of the Fourier transform described in [this wonderful 3Blue1Brown video](https://www.youtube.com/watch?v=spUNpyF58BY).



## Usage

### Song Transformation

To run a song, you first need to generate the fourier transform file (stored as a `.txt` of numbers) from the `.wav` file.

Run `song_full_converter.py` and it will prompt you for the path to the `.wav` file.

As of 2023, it's been ~5 years since this was written and so the `sndhdr` dependency is set to be deprecated/removed in Python 3.13.


### Song Visualising

Use `song_visualise_circle.py` to visualise the song after you have generated the Fourier file.



### Example
I've added a single example (the first 60 seconds of the Kevin MacLeod song "Exit the Premises").

Run `example_1.sh` from project root to start the viz.

Or check out [this YouTube video](https://www.youtube.com/watch?v=XZR_UIu4kRw).
