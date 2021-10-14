# imgetr
A command line tool to help download images from a web page.

## Examples

### Download all of the nhl logos from the fox website.

- Output the images into the directory `./nhl_logos` using the `-o` flag.
- Select `img` elements using `-t` flag
- Select `img` elements containing the class `.image-logo` using the `-c` flage.
- The image urls all have a similar format like `Coyotes.vresize.72.72.medium.0.png`, so lets rename them to a format like `Coyotes.png` using the `-r` flag and passing a regex selecting two groups. The first group up to the first "`.`" and the second group selecting the file extension `"([^.]+).+(\\..+$)"`.
- Finally lets pass the `-v` flag to print out each filename to the command line as they download.

```sh
imgetr https://www.foxsports.com/nhl/teams -o ./nhl_logos -t img -c "image-logo" -r "([^.]+).+(\\..+$)" -v
```

running the above produces the following output:

```
[✓] NHL.png
[✓] Ducks.png
[✓] Coyotes.png
[✓] Bruins.png
[✓] Sabres.png
[✓] Flames.png
[✓] Hurricanes.png
[✓] Blackhawks.png
[✓] Avalanche.png
[✓] BlueJackets.png
[✓] Stars.png
[✓] RedWings.png
[✓] Oilers.png
[✓] Panthers.png
[✓] Kings.png
[✓] Wild.png
[✓] Canadiens.png
[✓] Predators.png
[✓] Devils.png
[✓] Islanders.png
[✓] Rangers.png
[✓] Senators.png
[✓] Flyers.png
[✓] Penguins.png
[✓] Sharks.png
[✓] Kraken.png
[✓] Blues.png
[✓] Lightning.png
[✓] MapleLeafs.png
[✓] Canucks.png
[✓] GoldenKnights.png
[✓] Capitals.png
[✓] Jets.png
[====================] 100% Complete.
```



## Help

```
usage: imgetr [-h] [-o [OUTPUT_DIR]]                                                                                                    
                                  [-c class [class ...]] [-t [tag [tag ...]]]
                                  [-q [query_key]] [-u [.ext]] [-r [regex]]
                                  [-v]
                                  website

Download images from a website.

positional arguments:
  website               the website to download images from

optional arguments:
  -h, --help            show this help message and exit
  -o [OUTPUT_DIR], --output_dir [OUTPUT_DIR]
                        the directory to download the files into
  -c class [class ...], --class_list class [class ...]
                        list of css classes the images on the page contains
  -t [tag [tag ...]], --tag [tag [tag ...]]
                        list of html tags where images are contained
  -q [query_key], --query_key [query_key]
                        query key in an img src that contains image filename
  -u [.ext], --unknown_img_ext [.ext]
                        name of ext for images with no ext
  -r [regex], --rename [regex]
                        regex pattern selecting groups of the output image
                        filename to be concat together
  -v, --verbose         print out the name of each file downloaded
```

## TODO

- [] add option for selenium (headless) to download images which load on the page with javascript.
- [] add testing
- [] add more examples

## Working on imgetr 

To create conda environment:

```sh
conda env create -f environment.yml
```

To remove conda environment:

```sh
conda remove --name imgetr --all
```

To update requirements.txt:

```sh
conda env create -f environment.yml
pip freeze > requirements.txt
```

Before publishing anything

```sh
python -m pip install --upgrade pip setuptools wheel
python3 setup.py sdist bdist_wheel
```