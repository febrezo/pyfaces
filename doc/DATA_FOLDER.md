# Data Folder

The data folder is a structure stored by default in `~/.config/Pyfacefy` folder which stores the following information:

- The `sources` folder contains the original photographs grabbed.
- The `sources` folder contains the original photographs grabbed.
- The `encodings.json` file contains the details of each found face ordered by the unique name given to the photograph:

```
{
  "faces/face-1.png": {
    "original_file": "sources/photo-1.png",
    "encodings": […]
  },
  "faces/face-2.png": {
    "original_file": "sources/photo-1.png",
    "encodings": […]
  },
  "faces/face-3.png": {
    "original_file": "sources/photo-2.png",
    "encodings": […]
  }
}
```

- The `comparisons.json` file contains the details of the comparisons between the different faces. This file will be checked to avoid performing the same check twice.

The following is a sample folder structure.

```
data/
├── encodings.json
├── faces
│   ├── face-1.png
│   ├── face-2.png
│   └── face-3.png
└── sources
    ├── photo-1.png
    └── photo-2.png

2 directories, 6 files
```
