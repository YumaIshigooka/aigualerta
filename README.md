<p align="center">
<img src="https://i.imgur.com/u9FsL85.png" alt="drawing" width="200" align="center"/>
</p>

---

This is a project being developed with the purpose taking one of the data challenges from Aigües de Barcelona.

## Installation
### Create a Virtual Environment
Create the Virtual Environment (venv) with:
```bash
# You may need to run `sudo apt-get install python3-venv` first on Debian-based OSs
python3 -m venv .venv
```
And activate with:
| Platform |    Shell   | Command to activate virtual environment |
|----------|------------|-----------------------------------------|
| POSIX    | bash/zsh   | `source .venv/bin/activate`            |
|          | fish       | `source .venv/bin/activate.fish`       |
|          | csh/tcsh   | `source .venv/bin/activate.csh`        |
|          | pwsh       | `.venv/bin/Activate.ps1`               |
| Windows  | cmd.exe    | `.venv\Scripts\activate.bat`        |
|          | PowerShell | `.venv\Scripts\Activate.ps1`     |
> Extracted from the [VSC](https://code.visualstudio.com/docs/python/environments) and [venv](https://docs.python.org/3/library/venv.html) documentation.


### Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Add your data
In order to use your own data, add it to the `\data` directory. Any files inside this directory will not be detected by git and therefore will not be pushed to the repository. This is ideal if your data is confidential.
> [!CAUTION]  
> * Do not confuse the directory `\data` with `\src\data`. You will publish your datasets if the data is located there.
> * Always remember to delete all notebook outputs before pushing.

## Authors
* Yuma Ishigooka (Project Manager)
* Adrià León
* Marc Gutiérrez
* Jinsong Liu
* Suleyman Hasanov

## Acknowledgements

 - [Miquel Oliver](https://www.upf.edu/web/miquel-oliver)
 - [Aigües de Barcelona](https://www.aiguesdebarcelona.cat/ca/web/guest/)


## Feedback

If you have any feedback, please reach out to us at yuma.ishigooka01@estudiant.upf.edu