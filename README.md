## To launch
```bash
git clone https://github.com/slavikyd/simple_autometeo.git
cd simple_autometeo/webapp
pip install -r ../tests/requirements.txt
flask run
```

## To setup your own api
You are going to need your own external server And Rpi. Schematics will be released later

To launch api:
```bash
cd api
flask run --host=0.0.0.0
```
